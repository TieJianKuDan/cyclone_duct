# Download hsa files from https://www.aoml.noaa.gov/ftp/hrd/data/dropsonde/s

import requests

def download_file(url, file_path):
    print(f"download {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'a') as f:
            for chunk in response.iter_content(chunk_size=8192):
                text = chunk.decode("utf-8")
                f.write(text)
                print("=", end="")
        print("> " + file_path)
    else:
        print(f"fail and response code is {response.status_code}")


if __name__ == "__main__":
    urls = ["https://www.aoml.noaa.gov/ftp/hrd/data/dropsonde/HURR19/transmit/20191018H1.hsa",
            "https://www.aoml.noaa.gov/ftp/hrd/data/dropsonde/HURR19/transmit/20191018I1.hsa"]
    file_path = 'data/sondes/nestor_2019 .hsa'

    for url in urls:
        download_file(url, file_path)