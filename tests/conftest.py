import pytest
from brownie import (
    accounts,
    config,
    PhotographyNFT
)

@pytest.fixture
def get_account():
    return accounts.from_mnemonic(config["wallets"]["from_mnemonic"])

@pytest.fixture
def get_contract():
    account = accounts.from_mnemonic(config["wallets"]["from_mnemonic"])
    return PhotographyNFT.deploy({"from": account})

