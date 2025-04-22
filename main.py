#!/usr/bin/env python3
from controllers.fruit_controller import FruitController
import sys

def display_menu():
    """Display the main menu options"""
    print("\n===== Fruit Inventory Management System =====")
    print("1. View all fruits")
    print("2. Add a new fruit")
    print("3. Update a fruit")
    print("4. Delete a fruit")
    print("5. Search for a fruit")
    print("6. Exit")
    print("===========================================")

def view_all_fruits(controller):
    """Display all fruits in the inventory"""
    fruits = controller.get_all_fruits()
    if not fruits:
        print("\nNo fruits in inventory.")
        return

    print("\nFruit Inventory:")
    print("-" * 70)
    print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Quantity':<10} {'Category':<15}")
    print("-" * 70)
    
    for fruit in fruits:
        print(f"{fruit.id:<5} {fruit.name:<20} ${fruit.price:<9.2f} {fruit.quantity:<10} {fruit.category:<15}")

def add_fruit(controller):
    """Add a new fruit to the inventory"""
    print("\n--- Add New Fruit ---")
    try:
        name = input("Enter fruit name: ")
        price = float(input("Enter price: $"))
        quantity = int(input("Enter quantity: "))
        category = input("Enter category: ")
        
        fruit_data = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "category": category
        }
        
        new_fruit = controller.create_fruit(fruit_data)
        print(f"\nSuccess! Added {new_fruit.name} to inventory with ID: {new_fruit.id}")
    except ValueError as e:
        print(f"\nError: {e}. Please enter valid numeric values for price and quantity.")

def update_fruit(controller):
    """Update an existing fruit in the inventory"""
    print("\n--- Update Fruit ---")
    try:
        fruit_id = int(input("Enter fruit ID to update: "))
        fruit = controller.get_fruit_by_id(fruit_id)
        
        if not fruit:
            print(f"No fruit found with ID: {fruit_id}")
            return
        
        print(f"\nUpdating fruit: {fruit.name} (ID: {fruit.id})")
        name = input(f"Enter new name [{fruit.name}]: ") or fruit.name
        price_str = input(f"Enter new price [${fruit.price:.2f}]: ") or str(fruit.price)
        quantity_str = input(f"Enter new quantity [{fruit.quantity}]: ") or str(fruit.quantity)
        category = input(f"Enter new category [{fruit.category}]: ") or fruit.category
        
        fruit_data = {
            "name": name,
            "price": float(price_str),
            "quantity": int(quantity_str),
            "category": category
        }
        
        updated_fruit = controller.update_fruit(fruit_id, fruit_data)
        print(f"\nSuccess! Updated {updated_fruit.name}")
    except ValueError as e:
        print(f"\nError: {e}. Please enter valid numeric values.")

def delete_fruit(controller):
    """Delete a fruit from the inventory"""
    print("\n--- Delete Fruit ---")
    try:
        fruit_id = int(input("Enter fruit ID to delete: "))
        fruit = controller.get_fruit_by_id(fruit_id)
        
        if not fruit:
            print(f"No fruit found with ID: {fruit_id}")
            return
        
        confirm = input(f"Are you sure you want to delete {fruit.name}? (y/n): ")
        if confirm.lower() == 'y':
            controller.delete_fruit(fruit_id)
            print(f"\nSuccess! Deleted fruit with ID: {fruit_id}")
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Error: ID must be an integer.")

def search_fruit(controller):
    """Search for fruits by name or category"""
    print("\n--- Search Fruits ---")
    print("1. Search by name")
    print("2. Search by category")
    
    try:
        choice = int(input("Enter your choice (1-2): "))
        
        if choice == 1:
            search_term = input("Enter fruit name to search: ").lower()
            results = [f for f in controller.get_all_fruits() if search_term in f.name.lower()]
        elif choice == 2:
            search_term = input("Enter category to search: ").lower()
            results = [f for f in controller.get_all_fruits() if search_term in f.category.lower()]
        else:
            print("Invalid choice.")
            return
        
        if not results:
            print(f"No fruits found matching: '{search_term}'")
            return
            
        print(f"\nFound {len(results)} matching fruits:")
        print("-" * 70)
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Quantity':<10} {'Category':<15}")
        print("-" * 70)
        
        for fruit in results:
            print(f"{fruit.id:<5} {fruit.name:<20} ${fruit.price:<9.2f} {fruit.quantity:<10} {fruit.category:<15}")
            
    except ValueError:
        print("Error: Please enter a valid number.")

def main():
    """Main application function"""
    controller = FruitController()
    
    while True:
        display_menu()
        try:
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                view_all_fruits(controller)
            elif choice == '2':
                add_fruit(controller)
            elif choice == '3':
                update_fruit(controller)
            elif choice == '4':
                delete_fruit(controller)
            elif choice == '5':
                search_fruit(controller)
            elif choice == '6':
                print("\nThank you for using the Fruit Inventory Management System. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()