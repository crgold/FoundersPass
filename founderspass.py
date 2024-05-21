import smartpy as sp

# Importing the FA2 library from SmartPy
from smartpy.templates import fa2_lib as fa2

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

        @sp.entrypoint
        def mint(self, batch):
            """Admin can mint new or existing tokens."""
            sp.cast(
                batch,
                sp.list[
                    sp.record(
                        to_=sp.address,
                    ).layout(("to_"))
                ],
            )
            assert self.is_administrator_(), "FA2_NOT_ADMIN"
            for action in batch:
                token_id = self.data.next_token_id
                self.data.token_metadata[token_id] = sp.record(
                    token_id=token_id, token_info=sp.map({
                "" : sp.scenario_utils.bytes_of_string("ipfs://bafkreierffftgdmhrwqca6hkjxm7m5kmtbaoglkz32tt2tlepu7zxic72q")
                    }, key=sp.TString, value=sp.TBytes)
                )
                self.data.ledger[token_id] = action.to_
                self.data.next_token_id += 1

@sp.add_test()
def test():
    scenario = sp.test_scenario("NFT", [fa2.t, fa2.main, m])
    
    owner = sp.address("tz1Pierff89sbvsAveJgghkLHxHSLq74xRPA")
    ledger = {}
    
    # Contract metadata

    contract_metadata = sp.big_map({
        "" : sp.scenario_utils.bytes_of_string(
            "ipfs://bafkreibmshgnjeolxwnjhoxtbr6gq5lxwi3aexmytg677hdu67ljmk6ylq")
    })

    scenario.h1("Initialize contract")

    # Initialize the contract
    c1 = m.FoundersPass(
        administrator=owner,
        metadata=contract_metadata,
        ledger=ledger,
        token_metadata=[sp.list([
            sp.map({})
        ])]
    )

    scenario.h2("Contract")
    scenario += c1
