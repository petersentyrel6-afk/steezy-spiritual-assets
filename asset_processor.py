import os
import json
import hashlib

class AssetProcessor:
    def __init__(self, asset_name: str, image_path: str):
        self.asset_name = asset_name
        self.image_path = image_path

    def compress_and_extract_metadata(self) -> dict:
        """Simulates reading image binary, generating hash, and creating overlapping JSON backing metadata."""
        if os.path.exists(self.image_path):
            with open(self.image_path, "rb") as f:
                binary_data = f.read()
                file_size = len(binary_data)
                image_hash = hashlib.sha256(binary_data).hexdigest()
        else:
            file_size = 1048576 
            image_hash = hashlib.sha256(self.asset_name.encode('utf-8')).hexdigest()

        metadata = {
            "asset": self.asset_name,
            "file_size_bytes": file_size,
            "image_sha256": image_hash,
            "compression_ratio": "0.85_lossless",
            "layer_depth": 7,
            "expansion_status": "Ready for Ledger Binding"
        }
        return metadata

    def export_overlapping_json(self, output_dir: str = ".") -> str:
        os.makedirs(output_dir, exist_ok=True)
        meta = self.compress_and_extract_metadata()
        filename = os.path.join(output_dir, f"{self.asset_name.lower().replace(' ', '_')}_backing.json")
        with open(filename, "w") as f:
            json.dump(meta, f, indent=4)
        return filename
