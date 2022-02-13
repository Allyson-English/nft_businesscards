from curses import meta
from gc import collect
from brownie import CallingCard, network
from scripts.helpful_scrits import get_card_details, get_account, OPENSEA_URL
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests 
import json
import os

def main():
    hire_me = CallingCard[-1]
    number_of_business_cards = hire_me.tokenCounter()
    print(f"You have created {number_of_business_cards} business cards.")

    for token_id in range(number_of_business_cards):
        card_design = get_card_details(hire_me.tokenIdToCard(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{card_design}.json"

        collectible_metadata = metadata_template

        print("Current Metadata: ", collectible_metadata)

        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            if not os.path.exists(os.path.dirname(metadata_file_name)):
                os.makedirs(os.path.dirname(metadata_file_name))
            collectible_metadata['name'] = "Allyson English"
            collectible_metadata['description'] = "Software Engineer. I believe that tomorrow will be even better than today. I like building tools to help realize this vision."
            collectible_metadata['external_url'] = "https://www.allysonenglish.io/"
            
            image_path = "./img/" + card_design.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            
            collectible_metadata['image'] = image_uri

            with open(metadata_file_name, "w") as file:
                print(f"Creating metadata file: {metadata_file_name}")
                json.dump(collectible_metadata, file)

            token_uri = upload_to_ipfs(metadata_file_name)

            print(f"Image URI: {image_uri}\nToken URI: {token_uri}")
            set_tokenURI(token_id, hire_me, token_uri)
            print("Token URI set.")
            return token_uri

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()

        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        print("Filename from IPFS Hash: ", filename)
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print("Image URI, Information at: ", image_uri)
        return image_uri


def set_tokenURI(token_id, nft_contract, token_URI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_URI, {"from": account})
    tx.wait(1)
    print(f"Awesome! You can view Allyson's business card at {OPENSEA_URL.format(nft_contract.address, token_id)}")
