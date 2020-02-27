# -*- coding: utf-8 -*-

"""basemap instalation: 
sudo apt-get install libgeos-dev
pip3 install --user https://github.com/matplotlib/basemap/archive/master.zip
"""

import shapefile as shp  # Requires the pyshp package
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

extent = [-76.0, -35.0, -30.0, 8.0]

fig, ax = plt.subplots(figsize=(7, 5))

lon = [-60.75, -70.75, -68.25, -50]
lat = [5.75,-2.25, -1.75, -1.69]

ax = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[1], urcrnrlon=extent[2], urcrnrlat=extent[3], epsg=4326, ax=ax)
ax.bluemarble() # se comentar esta linha ele fica sem preenchimento, com fundo branco
ax.readshapefile('/home/wanabb/Documents/map_plot/shapefile/BRA_adm1','BRA_adm1',color='k', linewidth=1.5)
ax.scatter(lon, lat, c='r', s=100)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Visualization of iCMbio data')
plt.show()


