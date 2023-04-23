# my_blockchain/transaction.py

import hashlib
import ecdsa


class Transaction:
    def __init__(self, sender_wallet, receiver_public_key, amount):
        self.sender_public_key = sender_wallet.public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.signature = self.sign_transaction(sender_wallet)

    def hash(self):
        """
        Compute the hash of the transaction's content.
        """
        content = str(self.sender_public_key) + str(self.receiver_public_key) + str(self.amount)
        transaction_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        return transaction_hash

    def sign_transaction(self, sender_wallet):
        """
        Sign a transaction using the sender's wallet.
        """
        transaction_hash = self.hash()
        signature = sender_wallet.private_key.sign(transaction_hash.encode('utf-8'))
        return signature

    @staticmethod
    def verify_signature(transaction, signature, public_key):
        """
        Verify the signature of a transaction.
        """
        transaction_hash = transaction.hash()
        try:
            return public_key.verify(signature, transaction_hash.encode('utf-8'))
        except ecdsa.BadSignatureError:
            return False

    def to_dict(self, wallet_registry):
        return {
            "sender": wallet_registry.get_customer_name_by_public_key(self.sender_public_key),
            "recipient": wallet_registry.get_customer_name_by_public_key(self.receiver_public_key),
            "amount": self.amount,
        }
