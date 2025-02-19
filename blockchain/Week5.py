import time
import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = int(time.time())
        self.signature = signature


class Block:
    def __init__(self, transactions, previous_hash="0"):
        self.timestamp = time.ctime()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.timestamp}{self.previous_hash}{[tx.sender + tx.receiver + str(tx.amount) for tx in self.transactions]}"
        return hash(data)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.utxo = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transactions = [Transaction("System", "User1", 100), Transaction("System", "User2", 100)]
        genesis_block = Block(transactions=genesis_transactions)
        self.chain.append(genesis_block)
        self.update_utxo(genesis_transactions)

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(transactions=transactions, previous_hash=previous_block.hash)
        self.chain.append(new_block)
        self.update_utxo(transactions)

    def update_utxo(self, transactions):
        for tx in transactions:
            self.utxo[tx.receiver] = self.utxo.get(tx.receiver, 0) + tx.amount
            if tx.sender != "System":
                self.utxo[tx.sender] = self.utxo.get(tx.sender, 0) - tx.amount


blockchain = Blockchain()
private_keys = {}


def generate_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def add_transaction_gui():
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    amount = amount_entry.get()
    if not sender or not receiver or not amount.isdigit():
        messagebox.showwarning("Ошибка", "Заполните все поля!")
        return
    amount = int(amount)
    if blockchain.utxo.get(sender, 0) < amount:
        messagebox.showwarning("Ошибка", "Недостаточно средств!")
        return
    private_key = private_keys.get(sender)
    if not private_key:
        messagebox.showwarning("Ошибка", "Приватный ключ не найден!")
        return
    transaction = Transaction(sender, receiver, amount)
    blockchain.add_block([transaction])
    update_gui()
    clear_inputs()


def generate_keys_gui():
    user = user_entry.get()
    if not user:
        messagebox.showwarning("Ошибка", "Введите имя пользователя!")
        return
    private_key, public_key = generate_key_pair()
    private_keys[user] = private_key
    messagebox.showinfo("Успех", f"Ключи для {user} созданы!")


def clear_inputs():
    sender_entry.delete(0, tk.END)
    receiver_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    user_entry.delete(0, tk.END)


def update_gui():
    for widget in block_list_frame.winfo_children():
        widget.destroy()
    for block in blockchain.chain:
        block_label = tk.Label(block_list_frame,
                               text=f"Хэш: {block.hash}\nПредыдущий: {block.previous_hash}\nТранзакции: {[tx.sender + ' -> ' + tx.receiver + ': ' + str(tx.amount) for tx in block.transactions]}")
        block_label.pack()


def check_balances():
    balances = "\n".join([f"{user}: {balance}" for user, balance in blockchain.utxo.items()])
    messagebox.showinfo("Балансы", balances)


root = tk.Tk()
root.title("Блокчейн Эксплорер")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Отправитель:").grid(row=0, column=0)
sender_entry = tk.Entry(input_frame)
sender_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Получатель:").grid(row=1, column=0)
receiver_entry = tk.Entry(input_frame)
receiver_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Сумма:").grid(row=2, column=0)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=2, column=1)

tk.Label(input_frame, text="Пользователь:").grid(row=3, column=0)
user_entry = tk.Entry(input_frame)
user_entry.grid(row=3, column=1)

add_block_button = tk.Button(root, text="Добавить блок", command=add_transaction_gui)
add_block_button.pack()

generate_keys_button = tk.Button(root, text="Создать ключи", command=generate_keys_gui)
generate_keys_button.pack()

check_balance_button = tk.Button(root, text="Проверить балансы", command=check_balances)
check_balance_button.pack()

block_list_frame = tk.Frame(root)
block_list_frame.pack(pady=20, fill=tk.BOTH, expand=True)

update_gui()
root.mainloop()
