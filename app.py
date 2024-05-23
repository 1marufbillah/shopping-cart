from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

class Item:
    def __init__(self, name, price, quantity=1):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Item({self.name}, {self.price}, {self.quantity})"

    def __str__(self):
        return f"{self.name} - ${self.price} x {self.quantity}"

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

class ShoppingCart:
    def __init__(self):
        self.items = []

    def __add__(self, item):
        for cart_item in self.items:
            if cart_item == item:
                cart_item.quantity += item.quantity
                break
        else:
            self.items.append(item)
        return self

    def __sub__(self, item):
        for cart_item in self.items:
            if cart_item == item:
                cart_item.quantity -= item.quantity
                if cart_item.quantity <= 0:
                    self.items.remove(cart_item)
                break
        return self

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items)

    def __str__(self):
        cart_contents = "\n".join(str(item) for item in self.items)
        return f"Shopping Cart:\n{cart_contents}\nTotal: ${self.total_price():.2f}"

cart = ShoppingCart()

@app.route('/')
def index():
    return render_template('index.html', cart=cart)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    cart + Item(name, price, quantity)
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove_item():
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    cart - Item(name, price, quantity)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
