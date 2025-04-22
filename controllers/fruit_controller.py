import json
import os
from models.fruit import Fruit

class FruitController:
    def __init__(self, data_file="fruit_data.json"):
        self.data_file = data_file
        self.fruits = []
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    self.fruits = [Fruit.from_dict(item) for item in data]
            except Exception as e:
                print(f"Error loading data: {e}")
                self.fruits = []
        else:
            self.fruits = []
    
    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump([fruit.to_dict() for fruit in self.fruits], file, indent=4)
    
    def get_all_fruits(self):
        return self.fruits
    
    def get_fruit_by_id(self, fruit_id):
        for fruit in self.fruits:
            if fruit.id == fruit_id:
                return fruit
        return None
    
    def create_fruit(self, fruit_data):
        # Generate a new ID (simple approach)
        new_id = 1
        if self.fruits:
            new_id = max(fruit.id for fruit in self.fruits if fruit.id is not None) + 1
        
        fruit_data["id"] = new_id
        new_fruit = Fruit.from_dict(fruit_data)
        self.fruits.append(new_fruit)
        self.save_data()
        return new_fruit
    
    def update_fruit(self, fruit_id, fruit_data):
        fruit = self.get_fruit_by_id(fruit_id)
        if fruit:
            fruit_data["id"] = fruit_id  # Ensure ID remains the same
            updated_fruit = Fruit.from_dict(fruit_data)
            
            # Find and replace the fruit in the list
            for i, f in enumerate(self.fruits):
                if f.id == fruit_id:
                    self.fruits[i] = updated_fruit
                    break
            
            self.save_data()
            return updated_fruit
        return None
    
    def delete_fruit(self, fruit_id):
        fruit = self.get_fruit_by_id(fruit_id)
        if fruit:
            self.fruits = [f for f in self.fruits if f.id != fruit_id]
            self.save_data()
            return True
        return False