"""Fruit repository implementation for database operations"""
from typing import List, Optional
import sqlite3
import logging
from datetime import datetime

from models import Fruit
from .base_repository import BaseRepository
from .connection import DatabaseConnection

class FruitRepository(BaseRepository[Fruit]):
    """Repository for Fruit model database operations"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """Initialize the fruit repository
        
        Args:
            db_connection: Database connection manager
        """
        super().__init__(db_connection, "fruits", Fruit)
        self.logger = logging.getLogger(__name__)
    
    def find_by_category(self, category: str) -> List[Fruit]:
        """Find all fruits in a specific category
        
        Args:
            category: Category to search for
            
        Returns:
            List of fruits in the category
        """
        return self.find_by_field("category", category)
    
    def find_by_name(self, name: str) -> List[Fruit]:
        """Find fruits by name (exact match)
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching fruits
        """
        return self.find_by_field("name", name)
    
    def search_by_name(self, name_pattern: str) -> List[Fruit]:
        """Search fruits by name pattern
        
        Args:
            name_pattern: Name pattern to search for
            
        Returns:
            List of fruits matching the pattern
        """
        query = "SELECT * FROM fruits WHERE name LIKE ?"
        try:
            results = self.db_connection.execute_query(query, (f"%{name_pattern}%",))
            if not results:
                return []
            
            return [Fruit.from_tuple(tuple(row)) for row in results if row]
        except sqlite3.Error as e:
            self.logger.error(f"Error searching fruits by name pattern '{name_pattern}': {e}")
            raise
    
    def find_low_stock(self, threshold: int = 10) -> List[Fruit]:
        """Find fruits with stock below threshold
        
        Args:
            threshold: Stock threshold (default: 10)
            
        Returns:
            List of fruits with low stock
        """
        query = "SELECT * FROM fruits WHERE quantity < ?"
        try:
            results = self.db_connection.execute_query(query, (threshold,))
            if not results:
                return []
            
            return [Fruit.from_tuple(tuple(row)) for row in results if row]
        except sqlite3.Error as e:
            self.logger.error(f"Error finding low stock fruits: {e}")
            raise
    
    def find_by_price_range(self, min_price: float, max_price: float) -> List[Fruit]:
        """Find fruits within a price range
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            List of fruits in the price range
        """
        query = "SELECT * FROM fruits WHERE price BETWEEN ? AND ?"
        try:
            results = self.db_connection.execute_query(query, (min_price, max_price))
            if not results:
                return []
            
            return [Fruit.from_tuple(tuple(row)) for row in results if row]
        except sqlite3.Error as e:
            self.logger.error(f"Error finding fruits in price range {min_price}-{max_price}: {e}")
            raise
    
    def update_stock(self, fruit_id: int, new_quantity: int) -> Optional[Fruit]:
        """Update fruit stock quantity
        
        Args:
            fruit_id: ID of the fruit to update
            new_quantity: New stock quantity
            
        Returns:
            Updated fruit or None if not found
        """
        query = "UPDATE fruits SET quantity = ? WHERE id = ?"
        try:
            self.db_connection.execute_query(query, (new_quantity, fruit_id))
            return self.find_by_id(fruit_id)
        except sqlite3.Error as e:
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
            ValueError: If adjustment would result in negative stock
        """
        fruit = self.find_by_id(fruit_id)
        if not fruit:
            return None
            
        new_quantity = fruit.quantity + adjustment
        if new_quantity < 0:
            raise ValueError(f"Stock adjustment would result in negative quantity: {new_quantity}")
            
        return self.update_stock(fruit_id, new_quantity)
    
    def get_total_inventory_value(self) -> float:
        """Calculate total value of all fruits in inventory
        
        Returns:
            Total inventory value
        """
        query = "SELECT SUM(price * quantity) as total_value FROM fruits"
        try:
            results = self.db_connection.execute_query(query)
            if results and results[0][0] is not None:
                return float(results[0][0])
            return 0.0
        except sqlite3.Error as e:
            self.logger.error("Error calculating total inventory value: {e}")
            raise
    
    def get_category_summary(self) -> List[dict]:
        """Get summary of fruits by category
        
        Returns:
            List of dictionaries containing category summaries
        """
        query = """
        SELECT 
            category,
            COUNT(*) as fruit_count,
            SUM(quantity) as total_quantity,
            SUM(price * quantity) as total_value
        FROM fruits
        GROUP BY category
        """
        try:
            results = self.db_connection.execute_query(query)
            if not results:
                return []
            
            return [
                {
                    "category": row[0],
                    "fruit_count": row[1],
                    "total_quantity": row[2],
                    "total_value": row[3]
                }
                for row in results
            ]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting category summary: {e}")
            raise