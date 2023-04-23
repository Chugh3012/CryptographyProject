from my_blockchain import Wallet


class Customer:
    def __init__(self, name):
        self.name = name
        self.wallet = Wallet()

    def __repr__(self):
        return f"Customer(name={self.name}, wallet={self.wallet})"
