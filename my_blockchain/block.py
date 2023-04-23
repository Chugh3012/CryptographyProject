# my_blockchain/block.py

import hashlib
import time


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = int(time.time())
        self.previous_hash = previous_hash
        self.nonce = 0

    def hash(self):
        """
        Compute the hash of the block's content.
        """
        content = str(self.index) + str(self.transactions) + str(self.timestamp) + str(self.previous_hash) + str(
            self.nonce)
        block_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        return block_hash

    def to_dict(self, wallet_registry):
        return {
            "index": self.index,
            "transactions": [transaction.to_dict(wallet_registry) for transaction in self.transactions],
        }

