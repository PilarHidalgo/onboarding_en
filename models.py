"""
Fruit model representing a fruit entity with data mapping capabilities
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, ClassVar, Type, TypeVar

# Type variable for the generic factory method
T = TypeVar('T', bound='DataTransferable')

class DataTransferable:
    """Interface for objects that can be converted to/from data structures"""
    
    @classmethod
    def from_tuple(cls: Type[T], data_tuple: Optional[Tuple]) -> Optional[T]:
        """Create an object from a tuple representation"""
        raise NotImplementedError("Subclasses must implement from_tuple")
    
    def to_tuple(self) -> Tuple:
        """Convert object to a tuple representation"""
        raise NotImplementedError("Subclasses must implement to_tuple")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert object to a dictionary representation"""
        raise NotImplementedError("Subclasses must implement to_dict")


@dataclass
class Fruit(DataTransferable):
    """
    Fruit entity class representing a fruit in inventory
    
    Attributes:
        id: Unique identifier for the fruit
        name: Name of the fruit
        price: Price per unit
        quantity: Available quantity in stock
        category: Category of the fruit
        image_path: Optional path to the fruit's image
        created_at: Timestamp when the fruit was added to inventory
        updated_at: Timestamp when the fruit was last updated
    """
    name: str
    price: float
    quantity: int
    category: str
    id: Optional[int] = None
    image_path: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Class constants for tuple indices
    ID_INDEX: ClassVar[int] = 0
    NAME_INDEX: ClassVar[int] = 1
    PRICE_INDEX: ClassVar[int] = 2
    QUANTITY_INDEX: ClassVar[int] = 3
    CATEGORY_INDEX: ClassVar[int] = 4
    IMAGE_PATH_INDEX: ClassVar[int] = 5
    
    @property
    def total_value(self) -> float:
        """Calculate the total value of this fruit in inventory"""
        return self.price * self.quantity
    
    @classmethod
    def from_tuple(cls, data_tuple: Optional[Tuple]) -> Optional['Fruit']:
        """
        Create a Fruit object from a database tuple
        
        Args:
            data_tuple: Tuple containing fruit data from database
            
        Returns:
            Fruit object or None if data_tuple is None
        """
        if not data_tuple:
            return None
            
        # Create a dictionary with default values
        fruit_data = {
            "id": data_tuple[cls.ID_INDEX] if len(data_tuple) > cls.ID_INDEX else None,
            "name": data_tuple[cls.NAME_INDEX] if len(data_tuple) > cls.NAME_INDEX else "",
            "price": data_tuple[cls.PRICE_INDEX] if len(data_tuple) > cls.PRICE_INDEX else 0.0,
            "quantity": data_tuple[cls.QUANTITY_INDEX] if len(data_tuple) > cls.QUANTITY_INDEX else 0,
            "category": data_tuple[cls.CATEGORY_INDEX] if len(data_tuple) > cls.CATEGORY_INDEX else "Fresh Fruits",
        }
        
        # Add optional fields if they exist in the tuple
        if len(data_tuple) > cls.IMAGE_PATH_INDEX:
            fruit_data["image_path"] = data_tuple[cls.IMAGE_PATH_INDEX]
            
        return cls(**fruit_data)
    
    def to_tuple(self) -> Tuple:
        """
        Convert Fruit object to a tuple for database operations
        
        Returns:
            Tuple containing the fruit's data for database operations
        """
        return (
            self.name,
            self.price,
            self.quantity,
            self.category,
            self.image_path
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the fruit object to a dictionary
        
        Returns:
            Dictionary representation of the fruit
        """
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category,
            "image_path": self.image_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "total_value": self.total_value
        }
