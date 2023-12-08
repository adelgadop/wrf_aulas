import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import re

# Specify the path to your namelist.wps file
file_path = 'namelist.wps'

# Read the namelist.wps file
with open(file_path, 'r') as file:
    content = file.read()

# Extract values from the geogrid section using regular expressions
match = re.search(r'&geogrid(.+?)&', content, re.DOTALL)


if match:
    geogrid_content = match.group(1)
    e_we = int(re.search(r'e_we\s*=\s*(\d+)', geogrid_content).group(1))
    e_sn = int(re.search(r'e_sn\s*=\s*(\d+)', geogrid_content).group(1))
    dx = int(re.search(r'dx\s*=\s*(\d+)', geogrid_content).group(1))
    dy = int(re.search(r'dy\s*=\s*(\d+)', geogrid_content).group(1))
    map_proj = re.search(r'map_proj\s*=\s*\'(\w+)\'', geogrid_content).group(1)
    ref_lat = float(re.search(r'ref_lat\s*=\s*([-+]?\d*\.\d+|\d+)', geogrid_content).group(1))
    ref_lon = float(re.search(r'ref_lon\s*=\s*([-+]?\d*\.\d+|\d+)', geogrid_content).group(1))
    stand_lon = float(re.search(r'stand_lon\s*=\s*([-+]?\d*\.\d+|\d+)', geogrid_content).group(1))

    # Create a Cartopy GeoAxes instance
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([ref_lon - e_we * dx / 2, ref_lon + e_we * dx / 2, ref_lat - e_sn * dy / 2, ref_lat + e_sn * dy / 2])

    # Plot features
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', color='gray')

    # Plot domains
    for i in range(1, 4):  # Assuming there are 3 domains
        ax.plot([-180, -180], [-90, 90], color='red', linewidth=2)

    plt.title('WRF Domains')
    plt.show()
else:
    print("No geogrid section found in the namelist.wps file.")

