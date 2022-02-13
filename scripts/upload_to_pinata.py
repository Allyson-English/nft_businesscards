from pathlib import Path
import requests 
import os

PINATA_BASE_URL = "https://app.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"

filepath = "./img/wagmi-astro.png"
filename = filepath.split("/")[-1:][0]

headers = {"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")}

def main():
    with Path(filepath).open("rb") as fp:

        img_binary = fp.read()
        response = requests.post(PINATA_BASE_URL, + endpoint, files={"file": (filename, img_binary)}, headers = headers 
        )

        print(response.json())

