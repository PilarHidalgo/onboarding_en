from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Fruit:
    """
    Represents a fruit in the inventory.
    
    Attributes:
        id: Unique identifier for the fruit
        name: Name of the fruit
        price: Price per unit
        quantity: Available quantity in stock
        category: Category of the fruit (e.g., Fresh Fruits, Dried Fruits)
        created_at: Timestamp when the fruit was added to inventory
        updated_at: Timestamp when the fruit was last updated
    """
    id: Optional[int] = None
    name: str = ""
    price: float = 0.0
    quantity: int = 0
    category: str = "Fresh Fruits"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def total_value(self) -> float:
        """Calculate the total value of this fruit in inventory"""
        return self.price * self.quantity
    
    def to_dict(self) -> dict:
        """Convert the fruit object to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "total_value": self.total_value
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Fruit':
        """Create a Fruit object from a database row"""
        if len(row) >= 7:
            return cls(
                id=row[0],
                name=row[1],
                price=row[2],
                quantity=row[3],
                category=row[4],
                created_at=datetime.fromisoformat(row[5]) if row[5] else None,
                updated_at=datetime.fromisoformat(row[6]) if row[6] else None
            )
        elif len(row) >= 5:
            return cls(
                id=row[0],
                name=row[1],
                price=row[2],
                quantity=row[3],
                category=row[4]
            )
        else:
            raise ValueError("Invalid database row format")


@dataclass
class FruitCategory:
    """
    Represents a category of fruits.
    
    Attributes:
        name: Name of the category
        description: Description of the category
    """
    name: str
    description: str = ""
    
    @staticmethod
    def get_all_categories() -> list[str]:
        """Get a list of all available fruit categories"""
        return [
            "Fresh Fruits",
            "Dried Fruits",
            "Exotic Fruits",
            "Berries",
            "Citrus",
            "Other"
        ]
    
    @staticmethod
    def get_category_description(category: str) -> str:
        """Get the description for a specific category"""
        descriptions = {
            "Fresh Fruits": "Common fruits that are consumed fresh",
            "Dried Fruits": "Fruits that have been dried to remove moisture",
            "Exotic Fruits": "Uncommon or tropical fruits",
            "Berries": "Small, pulpy, and often edible fruits",
            "Citrus": "Fruits with a high citric acid content",
            "Other": "Miscellaneous fruits that don't fit other categories"
        }
        return descriptions.get(category, "No description available")