# =============================================================================
#
# Author:       Alejandro D. Peralta
# Last update:  February 2024
#
# conda activate wrf
# import libraries ============================================================

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import ConnectionPatch
import matplotlib.patheffects as pe
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from netCDF4 import Dataset

print("\nEste script é para dois dominios, precisa de geo_em_d01, geo_em_d02.")
# Stations --------------------------------------------------------------------
red = pd.read_csv('../namelists/pm25_stations.csv')
reg = red.loc[red.type=='Regional urban',]
urb = red.loc[red.type=='Urban',]
urp = red.loc[red.type=='Urban park',]
fpr = red.loc[red.type=='Forest preservation',]
coa = red.loc[red.type=='Coastal urban',]
idt = red.loc[red.type=='Industry',]

path_loc = '../data/geo/' #input('geo_em path location: ')

# We create a function to read elevation and lon, lat coordinates--------------
def mapa(path='../data/geo/geo_em.d01.nc'):
    da = xr.open_dataset(path)

    # Coordinates
    lon = da.XLONG_M[0,:].values[0]
    lat = da.XLAT_M[0,:][:,0].values

    # Change coordinates
    ds = (da.assign_coords({'longitude':lon,'latitude': lat})
          .rename({'south_north':'latitude', 'west_east':'longitude'}))

    return ds, lon, lat

# Making a figure -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1,2,figsize=(14,6.5),
                               gridspec_kw={'wspace':.2,'hspace':.05},
                               subplot_kw={'projection': ccrs.PlateCarree()})

#gs = gridspec.GridSpec(4, 4)
#ax1 = plt.subplot(gs[0:4, :2], projection=ccrs.PlateCarree())
#ax2 = plt.subplot(gs[0:4, 2:], projection=ccrs.PlateCarree())

geos = ['geo_em.d01.nc', 'geo_em.d02.nc']

# Color scales for terrain ----------------------------------------------------
cores_map = plt.cm.terrain  # gist_earth, turbo
colors_undersea = cores_map(np.linspace(-2, 0.05, 0))
colors_land = cores_map(np.linspace(0.20, 1, 2000))
all_colors = np.vstack((colors_undersea, colors_land))
terrain_map = mpl.colors.LinearSegmentedColormap.from_list(cores_map, all_colors)
ocean_color = (173/255, 216/255, 230/255)  # Light blue color
# End colors for terrain elevations -------------------------------------------

cborde = "k"

for ax, geo in zip([ax1, ax2], geos):
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.2, color='k', alpha=.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 9, 'color': 'k'}
    gl.ylabel_style = {'size': 9, 'color': 'k'}

    ds, _ , _   = mapa(path_loc+'/'+geo)
    _, lon, lat = mapa(path_loc+'/'+geos[1])
    xlim   = [lon[0],lon[-1]] 
    ylim   = [lat[0],lat[-1]] 

    # Add box for second domain
    if geo == geos[0]:
        ds.HGT_M.plot(cmap=terrain_map, ax=ax,
                      cbar_kwargs={'label': 'Height ground terrain [m]', 
                                   'spacing':'proportional',
                                   'location':'bottom',
                                   'pad':0.05,
                                   'shrink':0.8, 'aspect':25})
        ax.add_patch(mpl.patches.Rectangle((xlim[0], ylim[0]),
                                            xlim[1] - xlim[0],
                                            ylim[1] - ylim[0],
                                            fill=None, lw=3, 
                                            edgecolor=cborde, zorder=10))
        #ax.text(xlim[0]+(xlim[1]-xlim[0])*.05, ylim[1]+(ylim[1]-ylim[0])*.05, 'MASP', size=8, color='m', zorder=10)
        ax.set_title('Domain '+geo[7:10]+ ' (9 km x 9 km)', loc='left')
        # States of Southeastern of Brazil
        estados = {'Santa\nCatarina':[-51,-27.5],'Paraná':[-51,-25.25], 
                   'São Paulo':[-50,-21.5],'Minas Gerais':[-46,-20.0],
                   'Rio de\nJaneiro':[-43, -22.5], 'Espíritu\nSanto':[-41,-20]}
        for estado, coord in estados.items():
            txt = ax.text(coord[0], coord[1], estado, transform=ccrs.Geodetic(),
                          fontsize=8)
            txt.set_path_effects([pe.withStroke(linewidth=4, foreground='w', alpha=.5)])
        ax.plot(reg.lon.values, reg.lat.values,'o',markersize=4, color = 'b', 
                label='Regional Urban',transform=ccrs.Geodetic())
        ax.plot(idt.lon.values, idt.lat.values,'d', label='Industry', 
                markersize=4, color = '#c51b8a', mec='k',alpha=0.5,
                transform=ccrs.Geodetic())
        ax.legend(loc='lower right',ncol=2)

    else: # second domain
        ds.HGT_M.plot(cmap=terrain_map, ax=ax,
                      cbar_kwargs={'label': 'Height ground terrain [m]', 
                                   'spacing':'proportional',
                                   'location':'right',
                                   'pad':0.025,
                                   'shrink':0.3, 'aspect':25})
        # Adding MASP shapefile
        fname = '../data/shapefile/MunRM07.shp'
        shape_feature = cfeature.ShapelyFeature(Reader(fname).geometries(),
                                                ccrs.PlateCarree(), edgecolor='black')
        ax.add_feature(shape_feature, linewidth=.5, edgecolor = 'black', facecolor='none')
        ax.text(-47.5, -23.25, 'MASP', transform=ccrs.Geodetic(),fontsize=8,fontweight='bold')
        #ax.set_title('MASP', loc='left')

        # Adding domain 02
        ax.add_patch(mpl.patches.Rectangle((xlim[0], ylim[0]),
                                            xlim[1] - xlim[0],
                                            ylim[1] - ylim[0],
                                            fill=None, lw=3, edgecolor=cborde,
                                            zorder=5))
        ax.plot(urb.lon.values, urb.lat.values,'.', label='Urban', markersize=4, color = 'r', 
                transform=ccrs.Geodetic())
        ax.plot(urp.lon.values, urp.lat.values,'^', label='Urban Park', 
                markersize=5, color = '#99d8c9', mec='k',transform=ccrs.Geodetic())
        ax.plot(fpr.lon.values, fpr.lat.values,'s', label='Forest Preservation',
                markersize=5, color = '#31a354', mec='k',alpha=0.5,transform=ccrs.Geodetic())
        ax.plot(coa.lon.values, coa.lat.values,'.', label='Coastal urban', 
                markersize=7, color = 'm', alpha=0.7,transform=ccrs.Geodetic())
        ax.legend(loc='lower right', ncol=2)

    # Add map features with Cartopy 
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '10m',
                                                facecolor='lightblue'))
    ax.coastlines(linewidth=.5)
    states = cfeature.STATES.with_scale('10m')
    ax.add_feature(states, linewidth=.5, edgecolor="black")

# Adding zoom region inset axes using ConnectionPatch
# > Fazer zoom de uma area maior para outra menor
con1 = ConnectionPatch(xyA=(lon[0], lat[-1]), xyB=(lon[-1], lat[-1]), 
                       coordsA="data", coordsB="data", axesA=ax2, axesB=ax1, color=cborde)
con2 = ConnectionPatch(xyA=(lon[0], lat[0 ]), xyB=(lon[-1], lat[ 0]), 
                       coordsA="data", coordsB="data", axesA=ax2, axesB=ax1, color=cborde)
ax2.add_artist(con1)
ax2.add_artist(con2)
# termina o zoom

#plt.show()
fig.savefig("../figs/map_domain.png",dpi=300,bbox_inches='tight', facecolor='white')
