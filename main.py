from models.fruit import Fruit
from controllers.fruit_controller import FruitController
from store.fruit_store import FruitStore

def display_menu():
    print("\n===== Fruit Inventory Management System =====")
    print("1. Add new fruit")
    print("2. View all fruits")
    print("3. View fruit by ID")
    print("4. Update fruit")
    print("5. Delete fruit")
    print("6. Exit")
    return input("Enter your choice (1-6): ")

def add_fruit(controller):
    print("\n----- Add New Fruit -----")
    name = input("Enter fruit name: ")
    price = input("Enter price: ")
    quantity = input("Enter quantity: ")
    
    success, result = controller.create_fruit(name, price, quantity)
    if success:
        print(f"Fruit added successfully: {result}")
    else:
        print(f"Error: {result}")

def view_all_fruits(controller):
    print("\n----- All Fruits -----")
    fruits = controller.get_all_fruits()
    if not fruits:
        print("No fruits in inventory.")
    else:
        for fruit in fruits:
            print(fruit)

def view_fruit_by_id(controller):
    print("\n----- View Fruit by ID -----")
    id = input("Enter fruit ID: ")
    success, result = controller.get_fruit_by_id(id)
    if success:
        print(result)
    else:
        print(f"Error: {result}")

def update_fruit(controller):
    print("\n----- Update Fruit -----")
    id = input("Enter fruit ID: ")
    
    # First check if the fruit exists
    success, result = controller.get_fruit_by_id(id)
    if not success:
        print(f"Error: {result}")
        return
    
    print("Leave blank if you don't want to update a field")
    name = input("Enter new name (or press Enter to skip): ")
    price = input("Enter new price (or press Enter to skip): ")
    quantity = input("Enter new quantity (or press Enter to skip): ")
    
    # Convert empty strings to None
    name = name if name else None
    price = price if price else None
    quantity = quantity if quantity else None
    
    success, result = controller.update_fruit(id, name, price, quantity)
    if success:
        print(f"Fruit updated successfully: {result}")
    else:
        print(f"Error: {result}")

def delete_fruit(controller):
    print("\n----- Delete Fruit -----")
    id = input("Enter fruit ID: ")
    success, result = controller.delete_fruit(id)
    if success:
        print(result)
    else:
        print(f"Error: {result}")

def main():
    # Initialize the store and controller
    fruit_store = FruitStore()
    fruit_controller = FruitController(fruit_store)
    
    # Add some sample data
    fruit_controller.create_fruit("Apple", 1.99, 100)
    fruit_controller.create_fruit("Banana", 0.99, 150)
    fruit_controller.create_fruit("Orange", 1.49, 75)
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            add_fruit(fruit_controller)
        elif choice == '2':
            view_all_fruits(fruit_controller)
        elif choice == '3':
            view_fruit_by_id(fruit_controller)
        elif choice == '4':
            update_fruit(fruit_controller)
        elif choice == '5':
            delete_fruit(fruit_controller)
        elif choice == '6':
            print("Thank you for using the Fruit Inventory Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()