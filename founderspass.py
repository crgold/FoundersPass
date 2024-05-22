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
            # Define the NFT metadata
            nft_metadata = {
                "" : sp.bytes("0x697066733a2f2f6261666b726569726666667464676d68727771636136686b6a786d376d356b6d7462616f676c6b7a3332747432746c657075377a786963373271")
            }
            
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
                    token_id=token_id, token_info=nft_metadata
                )
                self.data.ledger[token_id] = action.to_
                self.data.next_token_id += 1

@sp.add_test()
def test():
    scenario = sp.test_scenario("NFT", [fa2.t, fa2.main, m])
    
    owner = sp.address("tz1Pierff89sbvsAveJgghkLHxHSLq74xRPA")
    ledger = {}
    
    # Contract metadata (make sure to update this as I think it's for the crystal contract)
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
        token_metadata=[]
    )

    scenario.h2("Contract")
    scenario += c1

    # Create a single minting action for one NFT
    batch = sp.list([sp.record(to_=owner)])

    scenario.h2("Mint 1 NFT to the owner")

    # Call the mint entry point with the single action
    c1.mint(batch, _sender=owner)

    # Log the value of the ledger to verify it is correct
    scenario.h3("Ledger after minting")
    scenario.show(c1.data.ledger)

    # Create a batch of minting actions for 300 NFTs
    batch = sp.list([sp.record(to_=owner) for _ in range(300)])

    scenario.h4("Mint 300 NFTs to the owner")

    # Call the mint entry point with the batch
    c1.mint(batch, _sender=owner)
    scenario.show(c1.data.ledger)
