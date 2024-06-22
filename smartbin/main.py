import tkinter as tk
from tkinter import simpledialog, ttk
import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block",
                     self.calculate_hash(0, "0", int(time.time()), "Genesis Block"))

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def add_new_transaction(self, transaction):
        last_block = self.chain[-1]
        new_index = len(self.chain)
        new_timestamp = int(time.time())
        new_hash = self.calculate_hash(new_index, last_block.hash, new_timestamp, transaction)
        self.chain.append(Block(new_index, last_block.hash, new_timestamp, transaction, new_hash))


class SimulatedSmartBin:
    def __init__(self, blockchain, threshold, customer_wallet_balance, supplier_wallet_balance):
        self.blockchain = blockchain
        self.threshold = threshold
        self.stock_level = 100
        self.customer_wallet_balance = customer_wallet_balance
        self.supplier_wallet_balance = supplier_wallet_balance

    def add_screws(self, quantity):
        self.stock_level += quantity
        print(f"Added {quantity} screws. New stock level: {self.stock_level}")

    def remove_screws(self, quantity):
        if self.stock_level >= quantity:
            self.stock_level -= quantity
            print(f"Removed {quantity} screws. New stock level: {self.stock_level}")
            if self.stock_level < self.threshold:
                self.trigger_reorder()

    def trigger_reorder(self):
        transaction = f"Reorder triggered for screws at {time.ctime()}"
        self.blockchain.add_new_transaction(transaction)
        print(transaction)

    def buy_coins(self, amount):
        if amount > 0:
            self.customer_wallet_balance += amount
            transaction = f"{amount} Bossard Coins added to customer's wallet."
            self.blockchain.add_new_transaction(transaction)
            print(transaction)
        else:
            print("Invalid amount entered.")

    def sell_coins(self, amount):
        if amount > 0 and self.supplier_wallet_balance >= amount:
            self.supplier_wallet_balance -= amount
            transaction = f"{amount} Bossard Coins deducted from supplier's wallet."
            self.blockchain.add_new_transaction(transaction)
            print(transaction)
            return True
        else:
            print("Invalid amount or insufficient balance.")
            return False

    def detect_low_inventory(self):
        if self.stock_level < self.threshold:
            print("Low inventory detected.")
            self.handle_low_inventory()

    def handle_low_inventory(self):
        if self.customer_wallet_balance >= 100:
            if self.reserve_coins(100):
                if self.accept_order():
                    if self.confirm_shipment():
                        if self.confirm_stock_increase():
                            print("Transaction completed successfully.")
        else:
            print("Insufficient balance to handle low inventory.")

    def reserve_coins(self, amount):
        self.customer_wallet_balance -= amount
        transaction = f"{amount} coins reserved from customer wallet at {time.ctime()}"
        self.blockchain.add_new_transaction(transaction)
        print(transaction)
        return True

    def accept_order(self):
        transaction = f"Order accepted by supplier at {time.ctime()}"
        self.blockchain.add_new_transaction(transaction)
        print(transaction)
        return True

    def confirm_shipment(self):
        self.supplier_wallet_balance += 100
        transaction = f"Shipment confirmed by supplier at {time.ctime()}"
        self.blockchain.add_new_transaction(transaction)
        print(transaction)
        return True

    def confirm_stock_increase(self):
        self.stock_level += 100
        transaction = f"Stock increase confirmed at {time.ctime()}"
        self.blockchain.add_new_transaction(transaction)
        print("Stock replenished and coins transferred.")
        return True


class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartBin Inventory and Blockchain Integration")
        self.configure(bg='lightblue')
        self.geometry("400x500")

        self.blockchain = Blockchain()
        self.smart_bin = SimulatedSmartBin(self.blockchain, threshold=20, customer_wallet_balance=100,
                                           supplier_wallet_balance=50)

        self.create_widgets()
        self.update_stock_display()
        self.check_inventory()

    def create_widgets(self):
        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10), padding=6)
        style.configure("TLabel", font=("Helvetica", 12), padding=6, background='lightblue')
        style.configure("TEntry", padding=6)
        style.configure("TProgressbar", thickness=20)

        # Stock label
        self.stock_label = ttk.Label(self, text="")
        self.stock_label.pack(pady=10)

        # Stock progress bar
        self.stock_progress = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate')
        self.stock_progress.pack(pady=10)

        # Add screws button
        self.add_screws_button = ttk.Button(self, text="Add Screws", command=self.add_screws)
        self.add_screws_button.pack(pady=5)

        # Remove screws button
        self.remove_screws_button = ttk.Button(self, text="Remove Screws", command=self.remove_screws)
        self.remove_screws_button.pack(pady=5)

        # Buy coins entry and button
        self.buy_coins_entry = ttk.Entry(self)
        self.buy_coins_entry.pack(pady=5)

        self.buy_coins_button = ttk.Button(self, text="Buy Bossard Coins", command=self.buy_coins)
        self.buy_coins_button.pack(pady=5)

        # Wallet info label
        self.wallet_info_label = ttk.Label(self, text="")
        self.wallet_info_label.pack(pady=5)

        # Sell coins entry and button
        self.sell_coins_entry = ttk.Entry(self)
        self.sell_coins_entry.pack(pady=5)

        self.sell_coins_button = ttk.Button(self, text="Sell Bossard Coins", command=self.sell_coins)
        self.sell_coins_button.pack(pady=5)

    def sell_coins(self):
        try:
            amount = int(self.sell_coins_entry.get())
            if self.smart_bin.sell_coins(amount):
                self.update_stock_display()
            else:
                print("Failed to sell coins.")
        except ValueError:
            print("Please enter a valid integer amount.")

    def add_screws(self):
        quantity = simpledialog.askinteger("Input", "Enter quantity of screws to add:", parent=self)
        if quantity and quantity > 0:
            self.smart_bin.add_screws(quantity)
            self.update_stock_display()

    def remove_screws(self):
        quantity = simpledialog.askinteger("Input", "Enter quantity of screws to remove:", parent=self)
        if quantity and quantity > 0:
            self.smart_bin.remove_screws(quantity)
            self.update_stock_display()

    def buy_coins(self):
        try:
            amount = int(self.buy_coins_entry.get())
            self.smart_bin.buy_coins(amount)
            self.update_stock_display()
        except ValueError:
            print("Please enter a valid integer amount.")

    def detect_low_inventory(self):
        if self.smart_bin.handle_low_inventory():
            self.update_stock_display()
        else:
            print("Failed to handle low inventory due to insufficient funds.")

    def check_inventory(self):
        self.smart_bin.detect_low_inventory()
        self.update_stock_display()
        self.after(5000, self.check_inventory)  # Schedule to check every 5 seconds

    def animate_stock_warning(self):
        # Flashing label as a warning
        current_color = self.stock_label.cget("background")
        next_color = "red" if current_color == "lightblue" else "lightblue"
        self.stock_label.config(background=next_color)
        self.after(500, self.animate_stock_warning)

    def update_stock_display(self):
        stock_text = f"Current Stock Levels: {self.smart_bin.stock_level} screws"
        wallet_text = f"Customer Wallet Balance: {self.smart_bin.customer_wallet_balance} Coins\nSupplier Wallet Balance: {self.smart_bin.supplier_wallet_balance} Coins"
        self.stock_label.config(text=stock_text)
        self.wallet_info_label.config(text=wallet_text)

        # Update progress bar
        self.stock_progress['value'] = self.smart_bin.stock_level  # Assume max stock is 100 for simplicity
        self.stock_progress['maximum'] = 100

        # Animation for low stock
        if self.smart_bin.stock_level < self.smart_bin.threshold:
            self.animate_stock_warning()


if __name__ == '__main__':
    app = InventoryApp()
    app.mainloop()
