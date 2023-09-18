# Download the raw data of dropsondes from https://www.aoml.noaa.gov/ftp/hrd/data/dropsonde/
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import re
import libs.tools as tools
import sys
from datetime import datetime

url = "https://www.aoml.noaa.gov/ftp/hrd/data/dropsonde/"

# Record log
sys.stdout = tools.Logger(
    "logs/download_raw_" + datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S") + ".log")

if __name__ == "__main__":
    # Get download urls
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{response.status_code}: Failed to obtain {url}")
        exit(-1)
    soup = BeautifulSoup(response.text, "html.parser")
    response.close()
    ul_tag = soup.ul
    li_tags = ul_tag.find_all('li')
    li_tags.pop(0)
    li_urls = [li_tag.a["href"] for li_tag in li_tags]
    raw_urls = [url + li_url + "raw/" for li_url in li_urls]
    save_paths = ["./data/sondes/" + li_url for li_url in li_urls]

    for i in range(75, len(raw_urls)):
        print("========================>")
        print(f"Downloading folder {i+1}")
        response = requests.get(raw_urls[i])
        if response.status_code != 200:
            print(
                f"{response.status_code}: Failed to obtain urls from {raw_urls[i]}")
            print("<========================")
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        response.close()
        ul_tag = soup.ul
        li_tags = ul_tag.find_all('li')
        li_tags.pop(0)
        li_urls = [li_tag.a["href"] for li_tag in li_tags]
        # Only get *avp.tar.gz or *.avp.tgz package
        pat1 = r'.*avp\.tar\.gz$'
        pat2 = r'.*AVP\.tar\.gz$'
        pat3 = r'.*avp\.tgz$'
        pat4 = r'.*AVP\.tgz$'
        li_urls = [li_url for li_url in li_urls if re.search(
            pat1, li_url) or re.search(pat2, li_url) or re.search(pat3, li_url) or re.search(pat4, li_url)]
        if len(li_urls) == 0:
            print(f"{response.status_code}: Got nothing from {raw_urls[i]}")
            print("<========================")
            continue
        package_urls = [raw_urls[i] + li_url for li_url in li_urls]
        if not os.path.isdir(save_paths[i]):
            os.mkdir(save_paths[i])
        for url in package_urls:
            tools.download_package(url, save_paths[i])
        print("<========================")
