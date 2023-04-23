# my_blockchain/wallet.py
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1


class Wallet:
    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()

    @staticmethod
    def generate_private_key():
        """
        Generate a private key using the ECDSA SECP256k1 curve.
        """
        return SigningKey.generate(curve=SECP256k1)

    def generate_public_key(self):
        """
        Generate the corresponding public key for the private key.
        """
        return self.private_key.get_verifying_key()

    def generate_address(self):
        """
        Generate the wallet address from the public key.
        """
        public_key_bytes = self.public_key.to_string()
        hashed_key = hashlib.sha256(public_key_bytes).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashed_key)
        hashed_public_key = ripemd160.digest()
        version = b'\x00'
        versioned_key = version + hashed_public_key
        checksum = hashlib.sha256(hashlib.sha256(versioned_key).digest()).digest()[:4]
        address = base58.b58encode(versioned_key + checksum)
        return address

    def __repr__(self):
        """
        A string representation of the wallet.
        """
        return f"Wallet(address={self.address})"


class WalletRegistry:
    def __init__(self):
        self.address_to_customer = {}

    def register_customer(self, customer):
        self.address_to_customer[customer.wallet.address] = customer

    def get_customers(self):
        return self.address_to_customer.values()

    def get_customer_by_name(self, name):
        for customer in self.get_customers():
            if customer.name == name:
                return customer
        return None

    def get_customer_name_by_public_key(self, public_key):
        for customer in self.get_customers():
            if customer.wallet.public_key == public_key:
                return customer.name
        return None

    def __repr__(self):
        return f"WalletRegistry(customers={list(self.address_to_customer.values())})"
