import time
import tkinter as tk
from tkinter import messagebox

def simple_hash(data):
    result = 0
    for char in data:
        result = (result * 31 + ord(char)) % (2**16)
    return hex(result)[2:]

class Block:
    def __init__(self, data, previous_hash="0"):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.timestamp}{self.data}{self.previous_hash}"
        return simple_hash(block_content)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Генезис-блок")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(data, previous_block.hash)
        self.chain.append(new_block)

    def remove_block(self, index):
        if index > 0 and index < len(self.chain):
            del self.chain[index]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
class BlockExplorer:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.window = tk.Tk()
        self.window.title("Блокчейн-обозреватель")

        self.listbox = tk.Listbox(self.window, width=100, height=20)
        self.listbox.pack(pady=10)

        self.add_block_button = tk.Button(self.window, text="Добавить блок", command=self.add_block)
        self.add_block_button.pack(pady=5)

        self.remove_block_button = tk.Button(self.window, text="Удалить блок", command=self.remove_block)
        self.remove_block_button.pack(pady=5)

        self.validate_button = tk.Button(self.window, text="Проверить блокчейн", command=self.validate_chain)
        self.validate_button.pack(pady=5)

        self.refresh_blockchain()

        self.window.mainloop()

    def refresh_blockchain(self):
        self.listbox.delete(0, tk.END)
        for i, block in enumerate(self.blockchain.chain):
            block_info = f"{i}: Хэш: {block.hash} | Время: {block.timestamp} | Данные: {block.data}"
            self.listbox.insert(tk.END, block_info)

    def add_block(self):
        data = f"Блок #{len(self.blockchain.chain)}"  # Для примера
        self.blockchain.add_block(data)
        self.refresh_blockchain()

    def remove_block(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите блок для удаления!")
            return

        index = selected[0]
        if index == 0:
            messagebox.showerror("Ошибка", "Удаление генезис-блока невозможно!")
            return

        self.blockchain.remove_block(index)
        self.refresh_blockchain()

    def validate_chain(self):
        is_valid = self.blockchain.is_chain_valid()
        if is_valid:
            messagebox.showinfo("Результат проверки", "Блокчейн действителен!")
        else:
            messagebox.showerror("Результат проверки", "Блокчейн недействителен!")

if __name__ == "__main__":
    my_blockchain = Blockchain()
    explorer = BlockExplorer(my_blockchain)
