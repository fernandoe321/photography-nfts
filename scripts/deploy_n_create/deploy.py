#!/usr/bin/python
from brownie import PhotographyNFT, accounts, network, config
from scripts.util import get_publish_source

def main():
    account = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    photography_nft = PhotographyNFT.deploy({"from": account}, publish_source=get_publish_source())
    return photography_nft
