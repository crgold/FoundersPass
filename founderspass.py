import smartpy as sp

# Importing the FA2 library from SmartPy
from smartpy.templates import fa2_lib as fa2

administrator = sp.test_account("Administrator")
alice = sp.test_account("Alice")

# Define the main module
main = fa2.main

@sp.module
def m():
    class FoundersPass(
        main.Admin,
        main.Nft,
        main.ChangeMetadata,
        main.WithdrawMutez,
        main.MintNft,
        main.BurnNft,
        main.OffchainviewTokenMetadata,
        main.OnchainviewBalanceOf,
    ):
        def __init__(self, administrator, metadata, ledger, token_metadata):
            main.OnchainviewBalanceOf.__init__(self)
            main.OffchainviewTokenMetadata.__init__(self)
            main.BurnNft.__init__(self)
            main.MintNft.__init__(self)
            main.WithdrawMutez.__init__(self)
            main.ChangeMetadata.__init__(self)
            main.Nft.__init__(self, metadata, ledger, token_metadata)
            main.Admin.__init__(self, administrator)

@sp.add_test()
def test():
    scenario = sp.test_scenario("NFT", [fa2.t, fa2.main, m])
    
    owner = sp.address("tz1Pierff89sbvsAveJgghkLHxHSLq74xRPA")
    ledger = {0: alice.address, 1: alice.address, 2: alice.address}
    
    # Contract metadata

    contract_metadata = sp.big_map({
        "" : sp.scenario_utils.bytes_of_string(
            "ipfs://bafkreibmshgnjeolxwnjhoxtbr6gq5lxwi3aexmytg677hdu67ljmk6ylq")
    })

    # Token metadata
    token_metadata = sp.list([
        sp.map({
            "" : sp.scenario_utils.bytes_of_string("ipfs://bafkreierffftgdmhrwqca6hkjxm7m5kmtbaoglkz32tt2tlepu7zxic72q")
        })
    ])


    scenario.h1("Initialize contract")

    # Initialize the contract
    c1 = m.FoundersPass(
        administrator=owner,
        metadata=contract_metadata,
        ledger={0: owner},
        token_metadata=token_metadata
    )

    scenario.h2("Contract")
    scenario += c1
    
    # Example minting action
    #c1.mintNft(sp.record(address=owner, metadata=token_metadata)).run(sender=owner)
