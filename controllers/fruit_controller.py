class FruitController:
    def __init__(self, fruit_store):
        self.fruit_store = fruit_store

    def create_fruit(self, name, price, quantity):
        try:
            price = float(price)
            quantity = int(quantity)
            if not name or price < 0 or quantity < 0:
                return False, "Invalid input. Name cannot be empty, price and quantity must be non-negative."
            fruit = self.fruit_store.add_fruit(name, price, quantity)
            return True, fruit
        except ValueError:
            return False, "Price must be a number and quantity must be an integer."

    def get_all_fruits(self):
        fruits = self.fruit_store.get_all_fruits()
        return fruits

    def get_fruit_by_id(self, id):
        try:
            id = int(id)
            fruit = self.fruit_store.get_fruit_by_id(id)
            if fruit:
                return True, fruit
            return False, "Fruit not found."
        except ValueError:
            return False, "ID must be an integer."

    def update_fruit(self, id, name=None, price=None, quantity=None):
        try:
            id = int(id)
            if price is not None:
                price = float(price)
                if price < 0:
                    return False, "Price must be non-negative."
            if quantity is not None:
                quantity = int(quantity)
                if quantity < 0:
                    return False, "Quantity must be non-negative."
            
            fruit = self.fruit_store.update_fruit(id, name, price, quantity)
            if fruit:
                return True, fruit
            return False, "Fruit not found."
        except ValueError:
            return False, "ID must be an integer, price must be a number, and quantity must be an integer."

    def delete_fruit(self, id):
        try:
            id = int(id)
            if self.fruit_store.delete_fruit(id):
                return True, "Fruit deleted successfully."
            return False, "Fruit not found."
        except ValueError:
            return False, "ID must be an integer."