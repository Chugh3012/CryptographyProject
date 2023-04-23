# my_blockchain/wallet.py

from ecdsa import SigningKey, SECP256k1


def generate_private_key():
    """
    Generate a private key using the ECDSA SECP256k1 curve.
    """
    return SigningKey.generate(curve=SECP256k1)


class Wallet:
    def __init__(self):
        self.private_key = generate_private_key()
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()

    def generate_public_key(self):
        """
        Generate the corresponding public key for the private key.
        """
        return self.private_key.get_verifying_key()

    def generate_address(self):
        """
        Generate a simplified wallet address from the public key.
        """
        public_key_bytes = self.public_key.to_string()
        return public_key_bytes.hex()

    # def generate_address(self):
    #     """
    #     Generate the wallet address from the public key.
    #     """
    #     public_key_bytes = self.public_key.to_string()
    #     hashed_key = hashlib.sha256(public_key_bytes).digest()
    #     ripemd160 = hashlib.new('ripemd160')
    #     ripemd160.update(hashed_key)
    #     hashed_public_key = ripemd160.digest()
    #     version = b'\x00'
    #     versioned_key = version + hashed_public_key
    #     checksum = hashlib.sha256(hashlib.sha256(versioned_key).digest()).digest()[:4]
    #     address = base58.b58encode(versioned_key + checksum)
    #     return address

    def __repr__(self):
        """
        A string representation of the wallet.
        """
        return f"Wallet(address={self.address})"


class WalletRegistry:
    def __init__(self):
        self.wallets = {}

    def add_wallet(self, wallet):
        self.wallets[wallet.address] = wallet

    def get_wallet_by_address(self, address):
        return self.wallets.get(address)

    def get_public_key_by_address(self, address):
        wallet = self.get_wallet_by_address(address)
        return wallet.public_key if wallet else None

    def get_private_key_by_address(self, address):
        wallet = self.get_wallet_by_address(address)
        return wallet.private_key if wallet else None

    def __str__(self):
        wallet_list = [str(wallet) for wallet in self.wallets.values()]
        return "\n".join(wallet_list)
