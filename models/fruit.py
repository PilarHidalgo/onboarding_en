class Fruit:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Price: ${self.price:.2f}, Quantity: {self.quantity}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }