# Plot the trajectory of cyclones and dropsondes
from os import system
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

IBTrACS_path = "data/cyclones/IBTrACS.ALL.v04r00.nc"

if __name__ == "__main__":
    cyclones = xr.open_dataset(IBTrACS_path)
    sids = cyclones["sid"]
    names = cyclones["name"]
    lons = cyclones["usa_lon"]
    lats = cyclones["usa_lat"]
    seasons = cyclones["season"]
    status = cyclones["usa_status"]
    basins = cyclones["basin"]
    dates = cyclones["iso_time"]

    mask = np.where(((seasons >= 2020) & (seasons <= 2020)) &
                    ((basins[:, 0] == b"EP") | (basins[:, 0] == b"NA")))

    sids_s = sids[mask]
    names_s = names[mask]
    lons_s = lons[mask]
    lats_s = lats[mask]
    seasons_s = seasons[mask]
    dates_s = dates[mask]
    dates_s = np.array(dates_s)
    lons_s = np.array(lons_s)
    lats_s = np.array(lats_s)

    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines()
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    ax.set_extent([-180, -180, -90, 90])
    ax.add_feature(cfeature.OCEAN)
    ax.set_title('TCs from 2020 to 2020'+' ('+str(len(seasons_s))+')',
                 fontsize=15, loc='center')
    ax.add_feature(cfeature.LAND, edgecolor='b')
    for i in range(0, len(seasons_s)):
        lon = lons_s[i, :]
        mask = ~np.isnan(lon)
        lon = lon[mask]
        lat = lats_s[i, :]
        mask = ~np.isnan(lat)
        lat = lat[mask]
        # ax.plot(lon, lat, color='k', linewidth=0.5,
        #         transform=ccrs.PlateCarree())
        cb = ax.scatter(lon, lat, s=5, transform=ccrs.PlateCarree())
        plt.pause(0.001)

    if os.path.isfile("/imgs/temp.jpg"):
        os.remove("/imgs/temp.jpg")
    fig.savefig("./imgs/temp.jpg", dpi=300)
