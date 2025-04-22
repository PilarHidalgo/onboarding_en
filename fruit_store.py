class FruitStore:
    def __init__(self):
        self.fruits = {}
        self.next_id = 1

    # Create
    def add_fruit(self, name, price, quantity):
        from models.fruit import Fruit
        fruit = Fruit(self.next_id, name, price, quantity)
        self.fruits[self.next_id] = fruit
        self.next_id += 1
        return fruit

    # Read
    def get_all_fruits(self):
        return list(self.fruits.values())

    def get_fruit_by_id(self, id):
        return self.fruits.get(id)

    # Update
    def update_fruit(self, id, name=None, price=None, quantity=None):
        fruit = self.fruits.get(id)
        if fruit:
            if name:
                fruit.name = name
            if price is not None:
                fruit.price = price
            if quantity is not None:
                fruit.quantity = quantity
            return fruit
        return None

    # Delete
    def delete_fruit(self, id):
        if id in self.fruits:
            del self.fruits[id]
            return True
        return False