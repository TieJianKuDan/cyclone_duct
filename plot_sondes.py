# Plot sondes and the according cyclone
import xarray as xr
import numpy as np
import pandas as pd
import cartopy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
from datetime import datetime

sonde_path = "data/sondes/AFRES15/20150605A1/g103115071QC.nc"
sonde = xr.open_dataset(sonde_path)
IBTrACS_path = "data/cyclones/IBTrACS.ALL.v04r00.nc"
cyclones = xr.open_dataset(IBTrACS_path)

# The longitude and latitude of dropsonde
lon_s = sonde.reference_lon.data[0]
lat_s = sonde.reference_lat.data[0]

# The longitude and latitude of cyclones
lons_c = cyclones.usa_lon.data
lats_c = cyclones.usa_lat.data

# Find the corresponding cyclone
# According to season
date_s = sonde.reference_time.data[0]  # numpy.datetime64
season = pd.to_datetime(date_s).to_pydatetime().year
mask = np.where(cyclones.season.data == season)
lons_c = lons_c[mask]
lats_c = lats_c[mask]
# According to date
dates_c = cyclones.iso_time.data[mask]  # numpy.bytes
starts_c = dates_c[:, 0]
starts_c = np.array([np.datetime64(start)
                    for start in starts_c])  # numpy.datetime64
mask = np.where(starts_c <= date_s)
lons_c = lons_c[mask]
lats_c = lats_c[mask]
dates_c = dates_c[mask]
ends_c = np.array([date[np.where(date != b"")][-1]
                  for date in dates_c])  # numpy.bytes
ends_c = np.array([np.datetime64(end)
                   for end in ends_c])  # numpy.datetime64
mask = np.where(ends_c >= date_s)
lons_c = lons_c[mask]
lats_c = lats_c[mask]
dates_c = dates_c[mask]
# According to site
date_s = pd.to_datetime(date_s).timestamp()
site_index = [0]*len(dates_c)
for i in range(0, len(dates_c)):
    gap = np.Inf
    for j in range(0, len(dates_c[i, :])):
        temp = abs(date_s - datetime.strptime(
            bytes(dates_c[i, j]).decode("utf-8"), r"%Y-%m-%d %H:%M:%S").timestamp())
        if (gap > temp):
            gap = temp
        else:
            site_index[i] = j - 1
            break
distance = np.Inf
nearest = 0
for i in range(0, len(site_index)):
    temp = (lons_c[i, site_index[i]] - lon_s)**2 + \
        (lats_c[i, site_index[i]] - lat_s)**2
    if temp < distance:
        distance = temp
        nearest = i
lon_c = lons_c[nearest, :]
lat_c = lats_c[nearest, :]

fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
# ax.set_extent([-120, -100, 10, 20])
ax.add_feature(cfeature.OCEAN)
ax.set_title('Dropsonde and Cyclones', fontsize=15, loc='center')
ax.scatter(lon_s, lat_s, s=50, transform=ccrs.PlateCarree(
    central_longitude=0))
mask = ~np.isnan(lon_c)
lon_c = lon_c[mask]
lat_c = lat_c[mask]
ax.scatter(lon_c, lat_c, s=50, transform=ccrs.PlateCarree(
    central_longitude=0))

if os.path.isfile("/imgs/temp.jpg"):
    os.remove("/imgs/temp.jpg")
fig.savefig("./imgs/temp.jpg", dpi=300)
