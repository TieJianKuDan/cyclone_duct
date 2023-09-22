# Plot sondes and the according cyclone
import libs.banner
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import libs.tools as tools

if __name__ == "__main__":
    sonde_path = "data/sondes/qc/HURR1_/g062839207QC.nc"
    sonde = xr.open_dataset(sonde_path)
    IBTrACS_path = "data/cyclones/IBTrACS.ALL.v04r00.nc"
    cyclones = xr.open_dataset(IBTrACS_path)

    # The longitude and latitude of dropsonde
    lon_s = sonde.reference_lon.data[0]
    lat_s = sonde.reference_lat.data[0]

    # The longitude and latitude of cyclones
    sid = tools.find_cyclone(sonde, cyclones)
    mask = np.where(cyclones.sid.data == sid)
    lon_c = cyclones.usa_lon.data[mask]
    lat_c = cyclones.usa_lat.data[mask]

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
