import hashlib
import uuid

class Transaction:
    def __init__(self, sender, receiver, amount, fee):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.tx_id = self.calculate_hash()

    def calculate_hash(self):
        tx_data = f"{self.sender}{self.receiver}{self.amount}{self.fee}{uuid.uuid4()}"
        return hashlib.sha256(tx_data.encode()).hexdigest()

    def __repr__(self):
        return f"Tx({self.sender} → {self.receiver}, {self.amount} монета, {self.fee} комиссия, ID: {self.tx_id})"

class UTXOModel:
    def __init__(self):
        self.utxo = {}

    def update_balance(self, sender, amount):
        if sender not in self.utxo:
            self.utxo[sender] = 100
        self.utxo[sender] -= amount
        if self.utxo[sender] < 0:
            raise ValueError("Баланс жеткіліксіз")

    def validate_transaction(self, sender, amount):
        if sender not in self.utxo or self.utxo[sender] < amount:
            return False
        return True

    def get_balance(self, account):
        return self.utxo.get(account, 100)

def hash_function(data):
    return hashlib.sha256(data.encode()).hexdigest()


def merkle_root(transactions):
    if not transactions:
        return None

    hashed_transactions = [hash_function(tx.tx_id) for tx in transactions]

    while len(hashed_transactions) > 1:
        if len(hashed_transactions) % 2 == 1:
            hashed_transactions.append(hashed_transactions[-1])

        hashed_transactions = [
            hash_function(hashed_transactions[i] + hashed_transactions[i + 1])
            for i in range(0, len(hashed_transactions), 2)
        ]

    return hashed_transactions[0]

class Block:
    def __init__(self, previous_hash):
        self.transactions = []
        self.previous_hash = previous_hash
        self.block_hash = None
        self.merkle_root = None

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def finalize_block(self):
        self.merkle_root = merkle_root(self.transactions)
        block_data = f"{self.previous_hash}{self.merkle_root}"
        self.block_hash = hash_function(block_data)

    def __repr__(self):
        return f"Block(Previous Hash: {self.previous_hash}, Merkle Root: {self.merkle_root}, Block Hash: {self.block_hash})"

class BlockExplorer:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def display_block_info(self, block_index):
        block = self.blocks[block_index]
        print(f"Блок #{block_index}:")
        print(f"Алдыңғы хэш: {block.previous_hash}")
        print(f"Меркле түбірі: {block.merkle_root}")
        print(f"Блок хэші: {block.block_hash}")
        print("Транзакциялар:")
        for tx in block.transactions:
            print(f"  {tx}")


def validate_transaction_and_update(utxo_model, sender, receiver, amount, fee):
    if utxo_model.validate_transaction(sender, amount):
        utxo_model.update_balance(sender, amount + fee)
        return True
    return False

utxo_model = UTXOModel()
explorer = BlockExplorer()

tx1 = Transaction("Alice", "Bob", 10, 0.1)
tx2 = Transaction("Bob", "Charlie", 5, 0.05)

if validate_transaction_and_update(utxo_model, "Alice", "Bob", 10, 0.1):
    print(f"Транзакция орындалды: {tx1}")
else:
    print("Транзакция орындалмады!")

if validate_transaction_and_update(utxo_model, "Bob", "Charlie", 5, 0.05):
    print(f"Транзакция орындалды: {tx2}")
else:
    print("Транзакция орындалмады!")

block = Block("0" * 64)
block.add_transaction(tx1)
block.add_transaction(tx2)
block.finalize_block()

explorer.add_block(block)
explorer.display_block_info(0)
