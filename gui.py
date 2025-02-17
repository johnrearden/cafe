import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv

coffees = {
    'Espresso': 1.50,
    'Latte': 2.50,
    'Cappuccino': 3.00,
    'Mocha': 4.00,
    'Americano': 2.00,
    'Macchiato': 3.00,
    'Affogato': 4.50,
    'Cortado': 3.00,
    'Ristretto': 2.00,
    'Doppio': 2.50,
    'Lungo': 2.50
}

quantity_terms = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10
}

class Order:
    def __init__(self, order_string, customer_name):
        self.customer_name = customer_name
        self.timestamp = datetime.now()
        self.product = None
        self.quantity = None
        self.order_string = order_string
        self.price = 0

        string_list = order_string.split(' ')
        self.order_words = [word.lower() for word in string_list]

    def get_quantity_from_order(self):
        for term, number in quantity_terms.items():
            if term in self.order_words or str(number) in self.order_words:
                self.quantity = number
                break

        if not self.quantity:
            self.quantity = 1

        for coffee in coffees.keys():
            for word in self.order_words:
                if coffee.lower() in word:
                    self.product = coffee
        if not self.product:
            self.product = 'unknown'

    def calculate_price(self):
        if self.product == 'unknown':
            price = 6
            self.price = price
        else:
            price = coffees.get(self.product) * self.quantity
            self.price = price

    def write_to_file(self):
        with open('orders.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.customer_name,
                self.product,
                self.quantity,
                self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                self.order_string,
                self.price
            ])

def submit_order():
    order_string = order_entry.get()
    name = name_entry.get()
    if not order_string or not name:
        messagebox.showerror("Error", "Please enter both your name and order.")
        return
    order = Order(order_string, name)
    order.get_quantity_from_order()
    order.calculate_price()
    order.write_to_file()
    messagebox.showinfo("Order Submitted", f"Order for {name} has been submitted.")
    order_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Cafe Order System")

tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Order:").grid(row=1, column=0, padx=10, pady=10)
order_entry = tk.Entry(root)
order_entry.grid(row=1, column=1, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit Order", command=submit_order)
submit_button.grid(row=2, columnspan=2, pady=10)

root.mainloop()
