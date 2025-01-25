import time

class Block:
    def __init__(self, data, previous_hash=""):
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.timestamp}{self.data}{self.previous_hash}"
        hash_value = 0
        for char in block_string:
            hash_value = (hash_value * 31 + ord(char)) % 1000000007
        return hash_value

def create_genesis_block():
    return Block("This is the Genesis Block", "0")

genesis_block = create_genesis_block()

print("Genesis Block:")
print(f"Timestamp: {genesis_block.timestamp}")
print(f"Data: {genesis_block.data}")
print(f"Previous Hash: {genesis_block.previous_hash}")
print(f"Hash: {genesis_block.hash}")
