#!/usr/bin/python
from brownie import PhotographyNFT, accounts, config, network
from scripts.util import OPENSEA_FORMAT
from metadata import sample_metadata
from pathlib import Path
from dotenv import load_dotenv
import yaml
import os
import requests
import json

PINATA_BASE_URL='https://api.pinata.cloud/'
PINATA_FILE_ENDPOINT = 'pinning/pinFileToIPFS'

load_dotenv()

def write_metadata(token_id, nft_contract):
    with open("./nft_info.yaml", "rb") as nft_info:
        nft_metadata = yaml.safe_load(nft_info)
    name = nft_metadata["name"]
    photo_metadata = sample_metadata.metadata_template
    metadata_file_name = (
        "./metadata/{}/".format(network.show_active())
        + name
        + "-"
        + str(token_id)
        + ".json"
    )
    print("Creating Metadata file: " + metadata_file_name)
    photo_metadata["name"] = nft_metadata["name"]
    photo_metadata["description"] = nft_metadata["description"]
    photo_metadata["external_url"] = nft_metadata["external_url"]
    image_path = nft_metadata["image_path"]
    image_uri = None
    if os.getenv("UPLOAD_PINATA") == "true":
        image_uri = upload_to_pinata(image_path, "jpg")
    photo_metadata["image"] = image_uri
    with open(metadata_file_name, "w") as file:
        json.dump(photo_metadata, file)
    if os.getenv("UPLOAD_PINATA") == "true":
        return upload_to_pinata(metadata_file_name, "json")

def upload_to_pinata(filepath, file_type):
    headers = {
        'pinata_api_key': os.getenv('PINATA_API_KEY'),
        'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')
    }
    filename = filepath.split("/")[-1:][0]
    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + PINATA_FILE_ENDPOINT,
            files={"file": (filename, file_binary)},
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]
        file_uri = "ipfs://{}?filename={}".format(
            ipfs_hash, filename)
        print(file_uri) 
    return file_uri

def set_tokenURI(token_id, nft_contract, tokenURI):
    account = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": account})

def main():
    print("Working on " + network.show_active())
    account = accounts.add(config["wallets"]["from_key"])
    contract = PhotographyNFT[-1]
    num_of_tokens = contract.currentTokenId()

    # CREATE METADATA
    print(
        "The number of tokens you've deployed is: "
        + str(num_of_tokens)
    )
    token_id = num_of_tokens + 1
    token_uri = write_metadata(token_id, contract)

    # CREATE NFT TOKEN
    with open("./nft_info.yaml", "rb") as nft_info:
        info = yaml.safe_load(nft_info)
    nft_name = info["name"]
    transaction = contract.createCollectible(nft_name, token_uri, {"from": account})
    transaction.wait(1)
    token_id = contract.currentTokenId()
    print("New PhotographyNFT tokenId is {} with name {}".format(token_id, nft_name))
    print(
        "Done! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(contract.address, token_id)
        )
    )
    print('Give up to 20 minutes, and hit the "refresh metadata" button')
