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

    def __repr__(self):
        """
        A string representation of the block.
        """
        return f"Block(index={self.index}, transactions={self.transactions}, timestamp={self.timestamp}, previous_hash={self.previous_hash}, nonce={self.nonce})"

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [transaction.to_dict() for transaction in self.transactions],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
        }

