# QC all sondes from all folders
import libs.banner
import os
import sys
import libs.tools as tools
from datetime import datetime

source = "data/sondes/raw"
target = "data/sondes/qc/HURR1_"

if __name__ == "__main__":
    config = "aspen.xml"
    # Record log
    sys.stdout = tools.Logger(
        "logs/QC_sondes_" + datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S") + ".log")

    if not os.path.exists(target):
        os.mkdir(target)

    for folder in os.listdir(source):
        if folder.startswith("HURR1"):
            folder_path = os.path.join(source, folder)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".avp"):
                        source_file = os.path.join(root, file)
                        file = os.path.splitext(file)[0] + "QC.nc"
                        target_file = os.path.join(target, file)
                        # check whether it has appeared
                        index = 1
                        while os.path.isfile(target_file):
                            target_file = os.path.splitext(
                                target_file)[0] + str(index) + ".nc"
                            index += 1
                        print(f"{source_file} ==QC==> {target_file}")
                        os.system(f"Aspen-QC -i {source_file} -s {config} -n {target_file}")
                        if os.path.isfile(target_file) and os.path.getsize(target_file) == 0:
                            os.remove(target_file)
                            print(f"error: cannot process {source_file}")
