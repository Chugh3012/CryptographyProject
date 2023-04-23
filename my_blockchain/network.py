# my_blockchain/network.py

from flask import Flask, request, jsonify

from .customer import Customer
from .transaction import Transaction
from .blockchain import Blockchain
from .wallet import WalletRegistry


class Network:
    def __init__(self, port, difficulty=4):
        self.app = Flask(__name__)
        self.blockchain = Blockchain(difficulty)
        self.wallet_registry = WalletRegistry()
        self.port = port

        # Initialise wallet registry
        for name in ('Alice', 'Bob', 'Carl', 'Dyna', 'Ela'):
            self.wallet_registry.register_customer(Customer(name))

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
            'chain': [block.to_dict(self.wallet_registry) for block in self.blockchain.chain],
            'length': len(self.blockchain.chain)
        }
        return jsonify(response), 200

    def new_transaction(self):
        transaction_details = request.form
        sender_name = transaction_details['sender']
        recipient_name = transaction_details['recipient']

        sender = self.wallet_registry.get_customer_by_name(sender_name)
        recipient = self.wallet_registry.get_customer_by_name(recipient_name)

        if not sender or not recipient:
            return jsonify({"error": "Invalid sender or recipient name"}), 400

        sender_wallet = sender.wallet
        recipient_wallet = recipient.wallet

        transaction = Transaction(
            sender_wallet,
            recipient_wallet.public_key,
            float(transaction_details['amount'])
        )

        self.blockchain.add_transaction(transaction)
        response = {'message': f'Transaction added to Block'}
        return jsonify(response), 201

    def mine(self):
        miner_name = request.form['miner']
        miner_customer = self.wallet_registry.get_customer_by_name(miner_name)

        if not miner_customer:
            return jsonify({"error": "Invalid miner name"}), 400

        miner_wallet = miner_customer.wallet

        self.blockchain.mine_pending_transactions(miner_wallet.public_key)
        response = {'message': 'New Block Mined'}
        return jsonify(response), 200

    def run(self):
        self.app.run(host='0.0.0.0', port=self.port)
