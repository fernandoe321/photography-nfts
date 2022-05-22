import pytest
from brownie import network, PhotographyNFT
from scripts.util import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

def test_can_create_photography_nft(get_account, get_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account
    contract = get_contract
    # Act
    transaction_receipt = contract.createCollectible(
        "test_name", "None", {"from": account}
    )
    # Assert
    assert isinstance(transaction_receipt.txid, str)
    assert contract.currentTokenId() > 0
    assert isinstance(contract.currentTokenId(), int)

def test_set_token_uri(get_account, get_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account
    contract = get_contract
    # Act
    contract.createCollectible("test_name", "None", {"from": account})
    contract.setTokenURI(1, "test_uri", {"from": account})
    # Assert
    assert contract.tokenURI(1, {"from": account}) == "test_uri"
