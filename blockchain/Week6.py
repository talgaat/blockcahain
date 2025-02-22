import time
import random

class Block:
    def __init__(self, index, previous_hash, transactions, difficulty):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return str(sum(ord(char) for char in block_string) % 10000000)

class Blockchain:
    def __init__(self, difficulty=5000000, mining_reward=50, tx_fee=1):
        self.chain = []
        self.transactions = []
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.tx_fee = tx_fee
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", "Genesis Block", self.difficulty)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def resolve_conflict(self, block1, block2):
        return block1 if int(block1.hash) < int(block2.hash) else block2

    def mine_pending_transactions(self, miner_address, miner_name):
        new_block = Block(len(self.chain), self.get_last_block().hash, self.transactions, self.difficulty)
        print(f"{miner_name} начал майнинг блока #{new_block.index}")
        new_block = self.proof_of_work(new_block, miner_name)
        return new_block

    def proof_of_work(self, block, miner_name):
        attempts = 0
        while True:
            block.nonce = random.randint(0, 1000000)
            computed_hash = int(block.compute_hash())
            attempts += 1
            if computed_hash < self.difficulty:
                block.hash = str(computed_hash)
                print(f"{miner_name} нашел блок #{block.index} за {attempts} попыток. Хэш: {block.hash}")
                return block

    def add_block(self, block, miner_address):
        self.chain.append(block)
        self.transactions = []
        self.add_transaction({"from": "system", "to": miner_address, "amount": self.mining_reward + self.tx_fee})

class Miner:
    def __init__(self, name, blockchain):
        self.name = name
        self.blockchain = blockchain
        self.balance = 0

    def mine(self):
        return self.blockchain.mine_pending_transactions(self.name, self.name)

blockchain = Blockchain()
miner1 = Miner("Miner1", blockchain)
miner2 = Miner("Miner2", blockchain)

blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 10})

start_time = time.time()
block1 = miner1.mine()
block2 = miner2.mine()
end_time = time.time()

winner_block = blockchain.resolve_conflict(block1, block2)
winner_miner = "Miner1" if winner_block == block1 else "Miner2"

blockchain.add_block(winner_block, winner_miner)

print(f"Победил: {winner_miner}")
print(f"Длина цепочки: {len(blockchain.chain)}")

for block in blockchain.chain:
    print(f"Индекс: {block.index}, Хэш: {block.hash}, Нонсе: {block.nonce}, Транзакции: {block.transactions}")
