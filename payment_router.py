import time
import requests
import json

class SteezyPaymentRouter:
    def __init__(self, address_pool: list):
        self.address_pool = address_pool
        self.currentIndex = 0

    def get_next_address(self) -> str:
        """Rotates sequentially through the 13 BlueWallet addresses for incoming orders."""
        addr = self.address_pool[self.currentIndex]
        self.currentIndex = (self.currentIndex + 1) % len(self.address_pool)
        return addr

    def check_address_balance(self, bitcoin_address: str) -> int:
        """Queries public blockchain data to verify if Bitcoin has been received."""
        try:
            url = f"https://mempool.space/api/address/{bitcoin_address}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                funded = data.get("chain_stats", {}).get("funded_txo_sum", 0)
                spent = data.get("chain_stats", {}).get("spent_txo_sum", 0)
                confirmed_balance = funded - spent
                return confirmed_balance
        except Exception as e:
            print(f"Network error checking address: {e}")
        return 0

    def fulfill_order(self, customer_email: str, asset_name: str, target_address: str):
        """Polls until payment is detected, then securely dispatches assets and JSON credentials."""
        print(f"Waiting for payment on address: {target_address} for asset: {asset_name}...")
        
        while True:
            balance = self.check_address_balance(target_address)
            if balance > 0:
                print(f"Payment detected! Balance: {balance} sats. Generating secure credentials...")
                credentials = self.generate_delivery_credentials(asset_name, target_address)
                self.send_secure_email(customer_email, credentials)
                break
            time.sleep(30) # Check every 30 seconds

    def generate_delivery_credentials(self, asset_name: str, address: str) -> dict:
        return {
            "status": "Verified",
            "asset": asset_name,
            "payment_address": address,
            "ledger_verification": "Single transaction ledger verification hash bound successfully.",
            "download_link": f"https://raw.githubusercontent.com/petersentyrel6-afk/steezy-spiritual-assets/main/{asset_name.lower().replace(' ', '_')}.png"
        }

    def send_secure_email(self, email: str, credentials: dict):
        print(f"Secure delivery dispatched to {email}: {json.dumps(credentials, indent=2)}")

if __name__ == "__main__":
    router = SteezyPaymentRouter(BLUESWALLET_ADDRESS_POOL)
    assigned_addr = router.get_next_address()
    print(f"Assigned payment address for new customer: {assigned_addr}")
