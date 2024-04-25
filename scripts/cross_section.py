# Script from
# https://stackoverflow.com/questions/42117049/plotting-wind-vectors-on-vertical-cross-section-with-matplotlib
# Modified by Alejandro Delgado  aperalta@usp.br
# Last update April 2024
# -----------------------------------------------------------------------------

import numpy as np
from matplotlib import pyplot
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
from netCDF4 import Dataset
from wrf import (getvar, to_np, get_cartopy, latlon_coords, vertcross,
                 cartopy_xlim, cartopy_ylim, interpline, CoordPair)

# Namelists -------------------------------------------------------------------
pathdir  = '../data/wrfout/met/'                                  # Your path directory
wrf_file = Dataset(pathdir + "wrfout_d02_2018-05-01_00:00:00")    # wrfout file
ntime    = 15  # Hour UTC of the wrf_file
smooth   = 1   # For quiver (vectors)
nlevels  = 20  # number of vertical levels
nquiver  = 6   # wind vector intervals
v_exag   = 10  # w vector exageration
v_scale  = 50  # scale for wind vectors
fig_t    = "Ilha com vetores zonais"           # Main title of figure
cbar_t   = 'Velocidade vertical (m s$^{-1}$)'  # Bar title
# Define the cross section start and end points
cross_start = CoordPair(lat=-24.0, lon=-47.5)
cross_end   = CoordPair(lat=-24.0, lon=-45.5)

# Get the WRF variables -------------------------------------------------------
ht  = getvar(wrf_file, "z", timeidx=ntime)
ht  = ht[:nlevels,:,:]
ter = getvar(wrf_file, "ter", timeidx=ntime)

w   = getvar(wrf_file, "wa", timeidx=ntime)
w   = w[:nlevels,:,:]

u   = getvar(wrf_file, "ua", timeidx=ntime)
u   = u[:nlevels,:,:]

max_dbz = getvar(wrf_file, "mdbz", timeidx=ntime)

ws = {'W':None,'w_cross':None,'U':None,'u_cross':None}

for WS, wind in zip(['W','U'],[w,u]):
    ws[WS] = 10**(wind/10.) # Use linear Z for interpolation

for WS, ws_cross in zip(['W','U'],['w_cross','u_cross']):
    ws[ws_cross] = vertcross(ws[WS], ht, wrfin=wrf_file,
                             start_point=cross_start,
                             end_point=cross_end,
                             latlon=True, meta=True)

# Convert back to dBz after interpolation
w_cross = 10.0 * np.log10(ws['w_cross'])                  # Apparently that is needed for interpolation
u_cross = 10.0 * np.log10(ws['u_cross'])

# Add back the attributes that xarray dropped from the operations above
w_cross.attrs.update(w_cross.attrs)
w_cross.attrs["description"] = "destaggered w-wind component"
w_cross.attrs["units"] = "m s-1"

# Add back the attributes that xarray dropped from the operations above
u_cross.attrs.update(u_cross.attrs)
u_cross.attrs["description"] = "destaggered u-wind component"
u_cross.attrs["units"] = "m s-1"

# To remove the slight gap between the dbz contours and terrain due to the
# contouring of gridded data, a new vertical grid spacing, and model grid
# staggering, fill in the lower grid cells with the first non-missing value
# for each column.

# Make a copy of the z cross data. Let's use regular numpy arrays for this.
w_cross_filled = np.ma.copy(to_np(w_cross))
u_cross_filled = np.ma.copy(to_np(u_cross))

# For each cross section column, find the first index with non-missing
# values and copy these to the missing elements below.
for i in range(w_cross_filled.shape[-1]):
    column_vals = w_cross_filled[:,i]
    # Let's find the lowest index that isn't filled. The nonzero function
    # finds all unmasked values greater than 0. Since 0 is a valid value
    # for dBZ, let's change that threshold to be -200 dBZ instead.
    first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
    w_cross_filled[0:first_idx, i] = w_cross_filled[first_idx, i]

# For each cross section column, find the first index with non-missing
# values and copy these to the missing elements below.
for i in range(u_cross_filled.shape[-1]):
    column_vals = u_cross_filled[:,i]
    # Let's find the lowest index that isn't filled. The nonzero function
    # finds all unmasked values greater than 0. Since 0 is a valid value
    # for dBZ, let's change that threshold to be -200 dBZ instead.
    first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
    u_cross_filled[0:first_idx, i] = u_cross_filled[first_idx, i]

# Get the terrain heights along the cross section line
ter_line = interpline(ter, wrfin=wrf_file, 
                      start_point=cross_start,
                      end_point=cross_end)

# Get the lat/lon points
lats, lons = latlon_coords(w)

# Get the cartopy projection object
cart_proj = get_cartopy(w)

# Create the figure -----------------------------------------------------------
fig = pyplot.figure(figsize=(8,6))
ax_cross = pyplot.axes()

# Make the cross section plot for dbz
w_levels = np.arange(-4E-1, +4E-1, 5E-2)
xs = np.arange(0, w_cross.shape[-1], 1)
ys = to_np(w_cross.coords["vertical"])
w_contours = ax_cross.contourf(xs,
                               ys,
                               to_np(w_cross_filled),
                               levels=w_levels,
                               cmap='jet',
                               extend="both")
# Add the color bar
cbar = fig.colorbar(w_contours, ax=ax_cross)
cbar.ax.tick_params(labelsize=12)
cbar.set_label(cbar_t, rotation=-270, fontsize=12)
# Fill in the mountain area
ht_fill = ax_cross.fill_between(xs, 0, to_np(ter_line),
                                facecolor="black")

# Tentativa do quiver
ax_cross.quiver(xs[::nquiver], ys[::nquiver],
                to_np(u_cross_filled[::nquiver, ::nquiver]), 
                to_np(w_cross_filled[::nquiver, ::nquiver]*v_exag),  # only for visualizing 
                scale=v_scale)

# Set the x-ticks to use latitude and longitude labels
coord_pairs = to_np(u_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in to_np(coord_pairs)]

# Set the desired number of x ticks below
num_ticks = 5
thin = int((len(x_ticks) / num_ticks) + .5)
ax_cross.set_xticks(x_ticks[::thin])
ax_cross.set_xticklabels(x_labels[::thin], rotation=25, fontsize=8)

# Set the x-axis and  y-axis labels
ax_cross.set_xlabel("Latitude, Longitude", fontsize=12)
ax_cross.set_ylabel("Altura (m)", fontsize=12)

# Add a title
ax_cross.set_title(fig_t, {"fontsize" : 14})

pyplot.show()
