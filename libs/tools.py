import requests
import os
import shutil
import re
import sys
import pandas as pd
import numpy as np
from datetime import datetime


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


class Logger(object):  # Record the log and output to the console
    def __init__(self, filename='Default.log'):
        self.terminal = sys.stdout
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
