# my_blockchain/blockchain.py
from my_blockchain.wallet import Wallet
from my_blockchain.block import Block
from my_blockchain.transaction import Transaction


class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = difficulty
        self.mining_reward_wallet = Wallet()

    @staticmethod
    def create_genesis_block():
        """
        Create the genesis block of the blockchain.
        """
        genesis_wallet = Wallet()
        genesis_transaction = Transaction(genesis_wallet, genesis_wallet.public_key, 0)
        genesis_block = Block(0, [genesis_transaction], "0")
        return genesis_block

    def get_last_block(self):
        """
        Get the last block in the blockchain.
        """
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        Add a new transaction to the list of pending transactions.
        """
        self.pending_transactions.append(transaction)

    def proof_of_work(self, block):
        """
        Implement the Proof of Work algorithm for mining a new block.
        """
        block.nonce = 0
        computed_hash = block.hash()

        while not computed_hash.startswith("0" * self.difficulty):
            block.nonce += 1
            computed_hash = block.hash()

        return computed_hash

    def mine_pending_transactions(self, miner_public_key):
        """
        Mine a new block containing the pending transactions, add it to the blockchain, and clear the pending transactions.
        """
        last_block = self.get_last_block()
        new_block = Block(len(self.chain), self.pending_transactions, last_block.hash())
        proof = self.proof_of_work(new_block)
        self.chain.append(new_block)

        # Add mining reward transaction
        mining_reward_transaction = Transaction(self.mining_reward_wallet, miner_public_key, 10)
        self.pending_transactions = [mining_reward_transaction]

        print(f"Block mined with nonce {new_block.nonce} and hash {proof}")

    def validate_chain(self):
        """
        Validate the integrity of the entire blockchain.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash() != current_block.hash():
                return False
            if current_block.previous_hash != previous_block.hash():
                return False

        return True

    def get_balance(self, public_key):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender_public_key == public_key:
                    balance -= transaction.amount
                if transaction.receiver_public_key == public_key:
                    balance += transaction.amount
        return balance
