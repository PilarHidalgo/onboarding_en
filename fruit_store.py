import sys
import os
from controllers.fruit_controller import FruitController

class FruitStore:
    def __init__(self):
        self.controller = FruitController()
        self.commands = {
            "list": self.list_fruits,
            "add": self.add_fruit,
            "update": self.update_fruit,
            "delete": self.delete_fruit,
            "view": self.view_fruit,
            "help": self.show_help
        }

    def run(self):
        if len(sys.argv) < 2:
            self.show_help()
            return

        command = sys.argv[1].lower()
        if command in self.commands:
            self.commands[command]()
        else:
            print(f"Unknown command: {command}")
            self.show_help()

    def list_fruits(self):
        fruits = self.controller.get_all_fruits()
        if not fruits:
            print("No fruits in inventory.")
            return

        print("\nFruit Inventory:")
        print("-" * 70)
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Quantity':<10} {'Category':<15}")
        print("-" * 70)
        
        for fruit in fruits:
            print(f"{fruit.id:<5} {fruit.name:<20} ${fruit.price:<9.2f} {fruit.quantity:<10} {fruit.category:<15}")
        print()

    def add_fruit(self):
        if len(sys.argv) < 6:
            print("Usage: python fruit_store.py add <name> <price> <quantity> <category>")
            return

        try:
            name = sys.argv[2]
            price = float(sys.argv[3])
            quantity = int(sys.argv[4])
            category = sys.argv[5]

            fruit_data = {
                "name": name,
                "price": price,
                "quantity": quantity,
                "category": category
            }

            new_fruit = self.controller.create_fruit(fruit_data)
            print(f"Added new fruit: {new_fruit.name} (ID: {new_fruit.id})")
        except ValueError:
            print("Error: Price must be a number and quantity must be an integer.")

    def update_fruit(self):
        if len(sys.argv) < 7:
            print("Usage: python fruit_store.py update <id> <name> <price> <quantity> <category>")
            return

        try:
            fruit_id = int(sys.argv[2])
            name = sys.argv[3]
            price = float(sys.argv[4])
            quantity = int(sys.argv[5])
            category = sys.argv[6]

            fruit_data = {
                "name": name,
                "price": price,
                "quantity": quantity,
                "category": category
            }

            updated_fruit = self.controller.update_fruit(fruit_id, fruit_data)
            if updated_fruit:
                print(f"Updated fruit: {updated_fruit.name} (ID: {updated_fruit.id})")
            else:
                print(f"No fruit found with ID: {fruit_id}")
        except ValueError:
            print("Error: ID must be an integer, price must be a number, and quantity must be an integer.")

    def delete_fruit(self):
        if len(sys.argv) < 3:
            print("Usage: python fruit_store.py delete <id>")
            return

        try:
            fruit_id = int(sys.argv[2])
            success = self.controller.delete_fruit(fruit_id)
            if success:
                print(f"Deleted fruit with ID: {fruit_id}")
            else:
                print(f"No fruit found with ID: {fruit_id}")
        except ValueError:
            print("Error: ID must be an integer.")

    def view_fruit(self):
        if len(sys.argv) < 3:
            print("Usage: python fruit_store.py view <id>")
            return

        try:
            fruit_id = int(sys.argv[2])
            fruit = self.controller.get_fruit_by_id(fruit_id)
            if fruit:
                print("\nFruit Details:")
                print("-" * 30)
                print(f"ID:       {fruit.id}")
                print(f"Name:     {fruit.name}")
                print(f"Price:    ${fruit.price:.2f}")
                print(f"Quantity: {fruit.quantity}")
                print(f"Category: {fruit.category}")
                print("-" * 30)
            else:
                print(f"No fruit found with ID: {fruit_id}")
        except ValueError:
            print("Error: ID must be an integer.")

    def show_help(self):
        print("\nFruit Store - Command Line Interface")
        print("=" * 40)
        print("Available commands:")
        print("  list                        - List all fruits")
        print("  add <name> <price> <qty> <category>  - Add a new fruit")
        print("  update <id> <name> <price> <qty> <category> - Update a fruit")
        print("  delete <id>                 - Delete a fruit")
        print("  view <id>                   - View details of a fruit")
        print("  help                        - Show this help message")
        print("\nExample:")
        print("  python fruit_store.py add Apple 1.99 100 Fresh")
        print("  python fruit_store.py list")
        print("=" * 40)

if __name__ == "__main__":
    app = FruitStore()
    app.run()