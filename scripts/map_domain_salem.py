# conda activate salem
import salem
import matplotlib.pyplot as plt

# Namelist
fpath = '../namelists/namelist.wps.luiza'
fname = '../figs/MunRM07.shp'
g, maps = salem.geogrid_simulator(fpath, map_kwargs={'countries':True})

# Reading a shapefile of the MASP
masp = salem.read_shapefile(fname).set_crs(epsg=4326)

# Plot
fig, ax = plt.subplots()
maps[0].set_rgb(natural_earth='lr')
maps[0].set_scale_bar()
maps[0].set_text(-54, -14, 'd01', color = 'k', fontweight = 'bold',
                 fontsize=10)

maps[0].set_shapefile(masp, lw=0.5, color='k',
                      countries = False,
                      oceans = False,
                      zorder = 2)

maps[0].set_text(-48,-23,'MASP',
                 color = 'k',
                 #fontweight = 'bold',
                 fontsize=7)

maps[0].visualize(ax=ax)
fig.savefig('../figs/map_domain.pdf',
            bbox_inches='tight', format='pdf')
plt.show()

