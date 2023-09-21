
import os
import re
import sys
import pygmt
import shutil
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


def download_package(url, path):  # Download package from url and save to path
    temp_path = path + "temp.tar.gz"
    unpack_path = path + re.split(r"[\._]", url.split("/")[-1])[0]
    response = requests.get(url, stream=True)
    with open(temp_path, 'xb') as fd:
        for chunk in response.iter_content(chunk_size=1024):
            fd.write(chunk)
    if not os.path.isfile(temp_path):
        print(f"Failed to download from {url}")
        return
    shutil.unpack_archive(temp_path, unpack_path)
    os.remove(temp_path)
    print(f"Successfully to download from {url} to {unpack_path}")
    return


def find_cyclone(sonde, cyclones):  # Find the corresponding cyclone
    lons_c = cyclones.usa_lon.data
    lats_c = cyclones.usa_lat.data
    sids = cyclones.sid.data
    # According to season
    date_s = sonde.reference_time.data[0]  # numpy.datetime64
    season = pd.to_datetime(date_s).to_pydatetime().year
    mask = np.where(cyclones.season.data == season)
    lons_c = lons_c[mask]
    lats_c = lats_c[mask]
    sids = sids[mask]
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
    sids = sids[mask]
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
    lon_s = sonde.reference_lon.data[0]
    lat_s = sonde.reference_lat.data[0]
    for i in range(0, len(site_index)):
        temp = (lons_c[i, site_index[i]] - lon_s)**2 + \
            (lats_c[i, site_index[i]] - lat_s)**2
        if temp < distance:
            distance = temp
            nearest = i
    sid = sids[nearest]
    return sid


def calc_e(T, rh):  # Calculate the vapour pressure (hPa)
    # T -> atmospheric temperature (K)
    # rh -> relative temperature
    E = np.exp(np.subtract(np.subtract(
        53.67957, np.divide(6743.769, T)), 4.8451*np.log(T)))
    return np.multiply(E, rh)


def calc_N(P, T, e):  # Calculate the atmospheric refraction index
    # P -> atmospheric pressure (hPa)
    # T -> atmospheric temperature (K)
    # e -> vapour pressure (hPa)
    return np.multiply(np.divide(77.6, T), np.add(P, np.divide(np.multiply(4810, e), T)))


def get_alt(lon, lat):  # Get the altitude according to longitude and latitude
    region = [lon - 1, lon + 1, lat - 1, lat + 1]
    points = pd.DataFrame(data={"lon": [lon], "lat": [lat]})

    grid = pygmt.grdlandmask(region=region, resolution="auto", spacing="0.05")
    df = pygmt.grdtrack(points=points, grid=grid, newcolname="is_land")
    if df.is_land[0] != 1:
        return 0

    grid = pygmt.datasets.load_earth_relief(
        resolution="15s", region=region, data_source="synbath")
    df = pygmt.grdtrack(points=points, grid=grid, newcolname="alt")
    return df.alt[0]


def is_duct(sonde, plot=False):  # Judge whether it is duct
    is_duct = False
    start = np.Inf
    end = np.Inf
    M_min = np.Inf
    M_max = np.Inf
    detaM = 0
    duct_type = "none"
    d = 0
    C = 0
    lamda = 0

    lon = sonde.reference_lon.data[0]
    lat = sonde.reference_lat.data[0]
    if np.isnan(lon) or np.isnan(lat):
        print("(+_+)?: error==>longitude or latitude is NaN ↓")
        duct_type = "error"
        return (is_duct, duct_type)
    alt_g = get_alt(lon, lat)

    Ps = sonde.pres.data
    s = pd.Series(Ps)
    Ps = s.interpolate()

    Ts = np.add(sonde.dp.data, 273.15)
    s = pd.Series(Ts)
    Ts = s.interpolate()

    rhs = np.divide(sonde.rh.data, 100)
    s = pd.Series(rhs)
    rhs = s.interpolate()

    alts = sonde.alt.data
    s = pd.Series(alts)
    alts = s.interpolate()
    if abs(alts[len(alts) - 1] - alts[0]) < 10:
        print("(+_+)?: error==>error: data is not normal! Always at same altitude ↓")
        duct_type = "error"
        return (is_duct, duct_type)

    es = calc_e(Ts, rhs)
    Ns = calc_N(Ps, Ts, es)
    zs = np.subtract(alts, alt_g)
    Ms = np.add(Ns, np.multiply(0.157, zs))

    if len(zs[np.isnan(zs)]) > 0 or len(Ms[np.isnan(Ms)]) > 0:
        print("(+_+)?: error==>error: data is so bad that failed to interpolate ↓")
        duct_type = "error"
        return (is_duct, duct_type)

    dMs = np.diff(Ms)
    dzs = np.diff(zs)
    # Avoid nan for dividing zero
    mask = np.where(np.abs(dzs) > 1e-10)
    dMs = dMs[mask]
    dzs = dzs[mask]
    Ms = np.array(Ms)[mask]
    zs = np.array(zs)[mask]
    dM_dx = dMs/dzs

    if plot:
        fig = plt.figure(figsize=(10, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_xlabel("M")
        ax1.set_ylabel("z")
        ax1.plot(Ms, zs, "-*")

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.set_xlabel("dM/dz")
        ax2.set_ylabel("z")
        ax2.plot(dM_dx, zs, "-*")

        if os.path.isfile("/imgs/temp.jpg"):
            os.remove("/imgs/temp.jpg")
        plt.savefig("./imgs/temp.jpg", dpi=300)

    index = 0
    while index < len(dM_dx):
        if (dM_dx[index] < 0):
            start = index
            M_max = Ms[start]
            for j in range(start, len(dM_dx)):
                if (dM_dx[j] >= 0):
                    end = j
                    M_min = Ms[end]
                    break
            if (end == np.Inf):
                duct_type = "error"
                break
            detaM = M_max - M_min
            duct_type = "suspend"
            d = zs[end] - zs[0]
            C = 5.66e-3
            for j in range(start, -1, -1):
                if (Ms[j] <= M_min):
                    duct_type = "surface"
                    d = zs[end] - zs[j]
                    C = 3.773e-3
                    break
            lamda = 2*C*d*np.sqrt(detaM)/3
            if (lamda >= 0.5):
                is_duct = True
                break
            index = end
            duct_type = "none"
            end = np.Inf
        else:
            index += 1
    return (is_duct, duct_type)


class Logger(object):  # Record the log and output to the console
    def __init__(self, filename='Default.log'):
        self.terminal = sys.stdout
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
