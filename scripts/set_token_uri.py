from brownie import CallingCard, network
from pathlib import Path
import json
from scripts.helpful_scrits import OPENSEA_URL, get_card_details, get_account, OPENSEA_URL

def main():
    print(f"Working on {network.show_active()}")
    hire_me = CallingCard[-1]

    number_of_collectibles = hire_me.tokenCounter() 
    print(f"You  have {number_of_collectibles} business cards.")
    token_URI = None

    for token_id in range(number_of_collectibles):
        card = get_card_details(hire_me.tokenIdToCard(token_id))

        # if not hire_me.tokenURI(token_id).startswith("https://"):
        print(f"Setting token URI of {token_id}")
        card_design = get_card_details(hire_me.tokenIdToCard(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{card_design}.json"

        # if  Path(metadata_file_name).exists():
        with open(metadata_file_name) as file:
            metadata = json.load(file)

            token_URI = # uri for meta data

            # set_tokenURI(token_id, hire_me, token_URI)
            print("Token URI: ", token_URI)
            print("Done!")

def set_tokenURI(token_id, nft_contract, token_URI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_URI, {"from": account})
    tx.wait(1)
    print(f"Awesome! You can view Allyson's business card at {OPENSEA_URL.format(nft_contract.address, token_id)}")