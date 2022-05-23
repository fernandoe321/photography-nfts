#!/usr/bin/python
from brownie import PhotographyNFT, accounts, config, network
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

def write_metadata(token_id):
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
        image_uri = upload_to_pinata(image_path)
    photo_metadata["image"] = image_uri
    with open(metadata_file_name, "w") as file:
        json.dump(photo_metadata, file)
    if os.getenv("UPLOAD_PINATA") == "true":
        return upload_to_pinata(metadata_file_name)

def upload_to_pinata(filepath):
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

def set_tokenURI(token_id, contract, tokenURI):
    account = accounts.add(config["wallets"]["from_key"])
    transaction = contract.setTokenURI(token_id, tokenURI, {"from": account})
    transaction.wait(1)
    return

def main():
    print("Working on " + network.show_active())
    contract = PhotographyNFT[-1]

    # CREATE METADATA
    token_id = int(input("Enter token id you would like to change the token URI for: "))
    print("Creating new metadata for tokenId #{}".format(token_id))
    token_uri = write_metadata(token_id)

    # SET TOKEN URI
    set_tokenURI(token_id, contract, token_uri)
    print("You've successfully changed the URI of token #{} to: {}".format(token_id, token_uri))
    