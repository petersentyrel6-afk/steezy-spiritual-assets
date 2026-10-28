import json
from coin_architecture import SpiritualCoinArchitecture
from asset_processor import AssetProcessor

def build_complete_genesis_suite():
    assets = [
        ("SteezyBTC Derivative 001", "STZ-BTC-01", "Foundational monetary anchor."),
        ("Ethos", "ETHOS", "Moral and spiritual character backing."),
        ("Pathos", "PATHOS", "Psychedelic experience and emotional resonance."),
        ("Logos", "LOGOS", "Divine reason, structural order, and code perfection.")
    ]

    master_ledger = []

    for name, symbol, desc in assets:
        arch = SpiritualCoinArchitecture(name, symbol, desc)
        processor = AssetProcessor(name, f"{name.lower().replace(' ', '_')}.png")
        metadata = processor.compress_and_extract_metadata()
        
        valuation = arch.compute_valuation(15.42, 100.0)
        genesis = arch.generate_genesis_block(metadata["image_sha256"])

        coin_record = {
            "coin_details": valuation,
            "genesis_block": genesis,
            "backing_metadata": metadata
        }
        master_ledger.append(coin_record)

    with open("master_steezy_genesis_ledger.json", "w") as f:
        json.dump(master_ledger, f, indent=4)
    print("Master Genesis Ledger successfully generated: master_steezy_genesis_ledger.json")

if __name__ == "__main__":
    build_complete_genesis_suite()
