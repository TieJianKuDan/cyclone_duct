# Gather all sondes from all folders
import os
import sys
import shutil
import libs.tools as tools
from datetime import datetime

source = "data/sondes/raw"
target = "data/sondes/all/"

if __name__ == "__main__":
    # Record log
    sys.stdout = tools.Logger(
        "logs/gather_sondes_" + datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S") + ".log")

    if not os.path.exists(target):
        os.mkdir(target)

    for folder in os.listdir(source):
        if folder.startswith("HURR1"):
            folder_path = os.path.join(source, folder)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".avp"):
                        source_file = os.path.join(root, file)
                        target_file = os.path.join(target, file)
                        print(f"{source_file} ==> {target_file}")
                        shutil.copy(source_file, target_file)