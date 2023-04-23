# my_blockchain/network.py

from flask import Flask, request, jsonify

from .transaction import Transaction
from .blockchain import Blockchain
from .wallet import Wallet, WalletRegistry


class Network:
    def __init__(self, port, difficulty=4):
        self.app = Flask(__name__)
        self.blockchain = Blockchain(difficulty)
        self.wallet_registry = WalletRegistry()
        self.port = port

        # Initialise wallet registry
        for w in range(5):
            self.wallet_registry.add_wallet(Wallet())

        # Register routes
        self.app.add_url_rule('/wallets', 'wallets', self.wallets, methods=['GET'])
        self.app.add_url_rule('/chain', 'chain', self.chain, methods=['GET'])
        self.app.add_url_rule('/transactions/new', 'new_transaction', self.new_transaction, methods=['POST'])
        self.app.add_url_rule('/mine', 'mine', self.mine, methods=['POST'])

    def wallets(self):
        response = {'wallets': str(self.wallet_registry)}
        return jsonify(response), 200

    def chain(self):
        response = {
            'chain': [block.to_dict() for block in self.blockchain.chain],
            'length': len(self.blockchain.chain)
        }
        return jsonify(response), 200

    def new_transaction(self):
        transaction_details = request.form
        sender_address = transaction_details['sender']
        recipient_address = transaction_details['recipient']

        sender_public_key = self.wallet_registry.get_public_key_by_address(sender_address)
        recipient_public_key = self.wallet_registry.get_public_key_by_address(recipient_address)

        sender_wallet = self.wallet_registry.get_wallet_by_address(sender_address)

        if not sender_public_key or not recipient_public_key:
            return jsonify({"error": "Invalid sender or recipient address"}), 400

        transaction = Transaction(
            sender_wallet,  # Pass the sender's wallet instead of sender_public_key
            recipient_public_key,
            float(transaction_details['amount'])
        )

        self.blockchain.add_transaction(transaction)
        response = {'message': f'Transaction added to Block'}
        return jsonify(response), 201

    def mine(self):
        miner_address = request.form['miner_address']

        miner_public_key = self.wallet_registry.get_public_key_by_address(miner_address)

        if not miner_public_key:
            return jsonify({"error": "Invalid miner address"}), 400

        self.blockchain.mine_pending_transactions(miner_public_key)
        response = {'message': 'New Block Mined'}
        return jsonify(response), 200

    def run(self):
        self.app.run(host='0.0.0.0', port=self.port)
