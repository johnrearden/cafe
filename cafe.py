from datetime import datetime
import csv


coffees = {
    'espresso': 1.50,
    'latte': 2.50,
    'cappuccino': 3.00,
    'mocha': 4.00,
    'americano': 2.00,
    'macchiato': 3.00,
    'affogato': 4.50,
    'cortado': 3.00,
    'ristretto': 2.00,
    'doppio': 2.50,
    'lungo': 2.50
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

        # Convert the order_string to a list of lowercase words and
        # remove 's' from plurals
        string_list = order_string.split(' ')
        self.order_words = [word.lower() for word in string_list]

    def get_quantity_from_order(self):
        for term, number in quantity_terms.items():
            # Extract the quantity from the order_string
            if term in self.order_words or str(number) in self.order_words:
                self.quantity = number
                break

            if not self.quantity:
                self.quantity = 1

        # Extract the product from the order_string
        for coffee in coffees.keys():
            for word in self.order_words:
                if coffee in word:
                    self.product = coffee
        if not self.product:
            self.product = 'unknown'

    def calculate_price(self):
        if self.product == 'unknown':
            price = 6
            print(f'The price of your weird custom order is {price}')
            self.price = price
        else:
            price = coffees.get(self.product) * self.quantity
            print(f'The price of your order is {price}')
            self.price = price

    # Save the order to a csv file
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

    def __str__(self):
        return f'{self.customer_name} ordered {self.order_items}'


def get_order_from_customer():
    print('We have the following coffees available:')
    print()
    print(f'{"Coffee":<15} {"Price":<10}')
    print('-' * 25)
    for coffee, price in coffees.items():
        print(f'{coffee.capitalize():<15} ${price:.2f}')
    print()
    order_string = input('What would you like to order? ')
    name = input('What is your name? ')
    order = Order(order_string, name)
    order.get_quantity_from_order()
    order.calculate_price()
    order.write_to_file()


if __name__ == '__main__':
    while True:
        get_order_from_customer()
        another = input('Would you like to place another order? (y/n) ')
        if another.lower() != 'y':
            print('Have a nice day!')
            break