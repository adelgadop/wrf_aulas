# conda activate salem
import salem
import matplotlib.pyplot as plt
import geobr
import cartopy.feature as cfeature

# Namelist
fpath = '../namelists/namelist.wps.luiza'
fname = '../figs/MunRM07.shp'
g, maps = salem.geogrid_simulator(fpath, 
                                  map_kwargs={'countries':False})

# Reading a shapefile of the MASP
masp = salem.read_shapefile(fname).set_crs(epsg=4326)

# Reading a shapefile of São Paulo state
sp = geobr.read_state(code_state='SP', year=2019)

# Plot
fig, ax = plt.subplots()
maps[0].set_rgb(natural_earth='hr')
maps[0].set_scale_bar()
maps[0].set_text(-48.8, -21.9, 'd01', color = 'k', fontweight = 'bold',   fontsize=10)
maps[0].set_text(-47.05, -23.25, 'd02', color = 'k', fontweight = 'bold',    fontsize=8)
#maps[0].set_text(-47.2, -23.3, 'd03', color = 'k', #fontweight = #                 fontsize=5)

maps[0].set_shapefile(masp, lw=0.25, color='r',
                      countries = False,
                      oceans = False,
                      zorder = 2)

maps[0].set_shapefile(sp, lw=0.5, color='k',
                      countries = False,
                      oceans = False,
                      zorder = 1)

maps[0].set_text(-48.0,-22.5,'São Paulo state',
                 color = 'k',
                 #fontweight = 'bold',
                 fontsize=7)

#maps[0].set_text(-47.2, -24,'MASP',
#                 color = 'tab:red',
                 #fontweight = 'bold',
#                 fontsize=5)

maps[0].visualize(ax=ax)
fig.savefig('../figs/map_domain_luiza.png', dpi=300,
            bbox_inches='tight', format='png')
#plt.show()

