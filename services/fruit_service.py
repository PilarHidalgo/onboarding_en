"""Fruit service implementation for business logic operations"""
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from models import Fruit
from database import FruitRepository
from .base_service import BaseService

class FruitService(BaseService[Fruit]):
    """Service for Fruit model business logic operations"""
    
    def __init__(self, repository: FruitRepository):
        """Initialize the fruit service
        
        Args:
            repository: Repository for fruit data access
        """
        super().__init__(repository, Fruit)
        self.logger = logging.getLogger(__name__)
        self.fruit_repository = repository  # Typed reference to the repository
    
    def _get_required_fields(self) -> List[str]:
        """Get required fields for the Fruit model
        
        Returns:
            List of required field names
        """
        return ['name', 'category', 'price', 'quantity']
    
    def _validate_model_data(self, data: Dict[str, Any], update: bool = False) -> None:
        """Validate fruit data
        
        Args:
            data: Dictionary containing fruit data
            update: Whether this is an update operation
            
        Raises:
            ValueError: If data is invalid
        """
        super()._validate_model_data(data, update)
        
        # Validate name
        if 'name' in data and (not isinstance(data['name'], str) or len(data['name']) < 2):
            raise ValueError("Name must be a string with at least 2 characters")
            
        # Validate category
        if 'category' in data and (not isinstance(data['category'], str) or len(data['category']) < 2):
            raise ValueError("Category must be a string with at least 2 characters")
            
        # Validate price
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    raise ValueError("Price cannot be negative")
            except (ValueError, TypeError):
                raise ValueError("Price must be a valid number")
                
        # Validate quantity
        if 'quantity' in data:
            try:
                quantity = int(data['quantity'])
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative")
            except (ValueError, TypeError):
                raise ValueError("Quantity must be a valid integer")
    
    def get_by_category(self, category: str) -> List[Fruit]:
        """Get all fruits in a specific category
        
        Args:
            category: Category to search for
            
        Returns:
            List of fruits in the category
            
        Raises:
            ValueError: If category is invalid
        """
        if not isinstance(category, str) or len(category) < 2:
            raise ValueError("Category must be a string with at least 2 characters")
            
        try:
            return self.fruit_repository.find_by_category(category)
        except Exception as e:
            self.logger.error(f"Error retrieving fruits by category '{category}': {e}")
            raise
    
    def search_by_name(self, name_pattern: str) -> List[Fruit]:
        """Search fruits by name pattern
        
        Args:
            name_pattern: Name pattern to search for
            
        Returns:
            List of fruits matching the pattern
            
        Raises:
            ValueError: If name pattern is invalid
        """
        if not isinstance(name_pattern, str) or len(name_pattern) < 1:
            raise ValueError("Name pattern must be a non-empty string")
            
        try:
            return self.fruit_repository.search_by_name(name_pattern)
        except Exception as e:
            self.logger.error(f"Error searching fruits by name pattern '{name_pattern}': {e}")
            raise
    
    def get_low_stock_fruits(self, threshold: int = 10) -> List[Fruit]:
        """Get fruits with stock below threshold
        
        Args:
            threshold: Stock threshold (default: 10)
            
        Returns:
            List of fruits with low stock
            
        Raises:
            ValueError: If threshold is invalid
        """
        if not isinstance(threshold, int) or threshold < 0:
            raise ValueError("Threshold must be a non-negative integer")
            
        try:
            return self.fruit_repository.find_low_stock(threshold)
        except Exception as e:
            self.logger.error(f"Error retrieving low stock fruits: {e}")
            raise
    
    def get_by_price_range(self, min_price: float, max_price: float) -> List[Fruit]:
        """Get fruits within a price range
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            List of fruits in the price range
            
        Raises:
            ValueError: If price range is invalid
        """
        try:
            min_price = float(min_price)
            max_price = float(max_price)
        except (ValueError, TypeError):
            raise ValueError("Price values must be valid numbers")
            
        if min_price < 0 or max_price < 0:
            raise ValueError("Price values cannot be negative")
            
        if min_price > max_price:
            raise ValueError("Minimum price cannot be greater than maximum price")
            
        try:
            return self.fruit_repository.find_by_price_range(min_price, max_price)
        except Exception as e:
            self.logger.error(f"Error retrieving fruits by price range {min_price}-{max_price}: {e}")
            raise
    
    def update_stock(self, fruit_id: int, new_quantity: int) -> Optional[Fruit]:
        """Update fruit stock quantity
        
        Args:
            fruit_id: ID of the fruit to update
            new_quantity: New stock quantity
            
        Returns:
            Updated fruit or None if not found
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not isinstance(fruit_id, int) or fruit_id <= 0:
            raise ValueError("Fruit ID must be a positive integer")
            
        if not isinstance(new_quantity, int) or new_quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")
            
        try:
            # Check if fruit exists
            fruit = self.get_by_id(fruit_id)
            if not fruit:
                return None
                
            return self.fruit_repository.update_stock(fruit_id, new_quantity)
        except Exception as e:
            self.logger.error(f"Error updating stock for fruit ID {fruit_id}: {e}")
            raise
    
    def adjust_stock(self, fruit_id: int, adjustment: int) -> Optional[Fruit]:
        """Adjust fruit stock by a relative amount
        
        Args:
            fruit_id: ID of the fruit to adjust
            adjustment: Amount to adjust (positive or negative)
            
        Returns:
            Updated fruit or None if not found
            
        Raises:
            ValueError: If parameters are invalid or adjustment would result in negative stock
        """
        if not isinstance(fruit_id, int) or fruit_id <= 0:
            raise ValueError("Fruit ID must be a positive integer")
            
        if not isinstance(adjustment, int):
            raise ValueError("Adjustment must be an integer")
            
        try:
            return self.fruit_repository.adjust_stock(fruit_id, adjustment)
        except ValueError as e:
            # Re-raise validation errors
            raise
        except Exception as e:
            self.logger.error(f"Error adjusting stock for fruit ID {fruit_id}: {e}")
            raise
    
    def get_total_inventory_value(self) -> float:
        """Calculate total value of all fruits in inventory
        
        Returns:
            Total inventory value
        """
        try:
            return self.fruit_repository.get_total_inventory_value()
        except Exception as e:
            self.logger.error(f"Error calculating total inventory value: {e}")
            raise
    
    def get_category_summary(self) -> List[Dict[str, Any]]:
        """Get summary of fruits by category
        
        Returns:
            List of dictionaries containing category summaries
        """
        try:
            return self.fruit_repository.get_category_summary()
        except Exception as e:
            self.logger.error(f"Error getting category summary: {e}")
            raise