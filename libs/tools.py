from datetime import datetime
import numpy as np
import requests
import os
import shutil
import re
import sys

# Data entry of the sonde
sonde_info = {"time": 0, "lat": 1, "lon": 2, "press": 3,
              "temp": 4, "humid": 5, "height": 6, "ZW": 7, "MW": 8}


def read_hsa(file_path):  # Read the .hsa file
    records = []
    with open(file_path, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.split()
            if len(line[2]) == 1:
                line[2] = "000" + line[2]
            elif len(line[2]) == 3:
                line[2] = "0" + line[2]
            time = datetime.strptime("20" + line[1] + line[2], r"%Y%m%d.%H%M")
            records.append([time, float(line[3]), -float(line[4]), float(line[5]), float(
                line[6]), float(line[7]), float(line[8]), float(line[9]), float(line[10])])
    return np.array(records)


def is_normal(record):  # Judge whether the record is normal
    if -99.0 in record:
        return False
    else:
        return True


def select_record(records):  # Select the normal record closest to the time of release
    selected = []
    flag = records[0, :]
    if is_normal(flag):
        selected.append(flag)
    for record in records:
        if record[1] != flag[1] or record[2] != flag[2]:
            flag = record
            if is_normal(flag):
                selected.append(flag)
        else:
            if is_normal(record):
                if (len(selected) == 0) \
                    or (selected[-1][1] != flag[1]) \
                        or (selected[-1][2] != flag[2]):
                    selected.append(record)
                else:
                    selected[-1] = record
    return np.array(selected)


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


class Logger(object):
    def __init__(self, filename='Default.log'):
        self.terminal = sys.stdout
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
