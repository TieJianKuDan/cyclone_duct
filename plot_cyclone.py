# Plot the trajectory of cyclones and dropsondes

from os import system
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import libs.tools as tools

IBTrACS_path = "data/cyclones/IBTrACS.ALL.v04r00.nc"
cyclones = xr.open_dataset(IBTrACS_path)

sids = cyclones["sid"]
names = cyclones["name"]
lons = cyclones["usa_lon"]
lats = cyclones["usa_lat"]
seasons = cyclones["season"]
status = cyclones["usa_status"]
basins = cyclones["basin"]
dates = cyclones["iso_time"]

# mask = np.where(((seasons >= 2020) & (seasons <= 2020)) &
#                 ((basins[:, 0] == b"EP") | (basins[:, 0] == b"NA")))

mask = np.where((names == b"NESTOR") & (seasons == 2019))

sids_s = sids[mask]
names_s = names[mask]
lons_s = lons[mask]
lats_s = lats[mask]
seasons_s = seasons[mask]
dates_s = dates[mask]
dates_s = np.array(dates_s)
lons_s = np.array(lons_s)
lats_s = np.array(lats_s)
num = len(seasons_s)
print(num)

fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
# ax.set_extent([-120, -60, 20, 30])
ax.add_feature(cfeature.OCEAN)
ax.set_title('TCs from 1996 to 2020'+' ('+str(num)+')',
             fontsize=20, loc='center')
ax.add_feature(cfeature.LAND, edgecolor='b')
for i in range(0, num):
    lon = lons_s[i, :]
    mask = ~np.isnan(lon)
    lon = lon[mask]
    lat = lats_s[i, :]
    mask = ~np.isnan(lat)
    lat = lat[mask]
    # ax.plot(lon, lat, color='k', linewidth=0.5,
    #         transform=ccrs.PlateCarree())
    cb = ax.scatter(lon, lat, s=5, transform=ccrs.PlateCarree())
    # plt.pause(0.001)

file_path = "data/sondes/nestor_2019.hsa"
records = tools.read_hsa(file_path)
selected = tools.select_record(records)
info = tools.sonde_info
lons = selected[:, info["lon"]]
lats = selected[:, info["lat"]]
cb = ax.scatter(lons, lats, s=5, transform=ccrs.PlateCarree())

plt.show()
system("pause")
