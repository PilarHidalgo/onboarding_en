"""Base repository implementation for database operations"""
import sqlite3
from typing import TypeVar, Generic, Optional, List, Type, Tuple, Dict, Any
import logging

from models.base import DataTransferable
from .connection import DatabaseConnection

T = TypeVar('T', bound=DataTransferable)

class BaseRepository(Generic[T]):
    """Base repository class for database operations
    
    Generic repository pattern implementation for database operations
    on model objects that implement the DataTransferable interface.
    
    Attributes:
        db_connection: Database connection manager
        table_name: Name of the database table
        model_class: Class of the model this repository handles
    """
    
    def __init__(
        self, 
        db_connection: DatabaseConnection, 
        table_name: str,
        model_class: Type[T]
    ):
        """Initialize the repository
        
        Args:
            db_connection: Database connection manager
            table_name: Name of the database table
            model_class: Class of the model this repository handles
        """
        self.db_connection = db_connection
        self.table_name = table_name
        self.model_class = model_class
        self.logger = logging.getLogger(__name__)
    
    def find_by_id(self, id_value: int) -> Optional[T]:
        """Find a record by its ID
        
        Args:
            id_value: ID of the record to find
            
        Returns:
            Model instance or None if not found
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        try:
            results = self.db_connection.execute_query(query, (id_value,))
            if results and len(results) > 0:
                # Convert row to tuple and create model instance
                data_tuple = tuple(results[0])
                return self.model_class.from_tuple(data_tuple)
            return None
        except sqlite3.Error as e:
            self.logger.error(f"Error finding record by ID {id_value}: {e}")
            raise
    
    def find_all(self) -> List[T]:
        """Find all records in the table
        
        Returns:
            List of model instances
        """
        query = f"SELECT * FROM {self.table_name}"
        try:
            results = self.db_connection.execute_query(query)
            if not results:
                return []
                
            models = []
            for row in results:
                data_tuple = tuple(row)
                model = self.model_class.from_tuple(data_tuple)
                if model:
                    models.append(model)
            return models
        except sqlite3.Error as e:
            self.logger.error(f"Error finding all records: {e}")
            raise
    
    def create(self, model: T) -> Optional[T]:
        """Create a new record in the database
        
        Args:
            model: Model instance to create
            
        Returns:
            Created model with ID or None on failure
        """
        # Get column names from table info
        columns_info = self.db_connection.get_table_info(self.table_name)
        # Filter out id, created_at, updated_at columns which are auto-generated
        columns = [col['name'] for col in columns_info 
                  if col['name'] not in ('id', 'created_at', 'updated_at')]
        
        # Create placeholders for SQL query
        placeholders = ', '.join(['?' for _ in columns])
        columns_str = ', '.join(columns)
        
        query = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"
        
        try:
            # Convert model to tuple for database insertion
            data_tuple = model.to_tuple()
            
            # Execute the query
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, data_tuple)
                
                # Get the ID of the inserted record
                last_id = cursor.lastrowid
                
                # Return the created model with ID
                return self.find_by_id(last_id)
        except sqlite3.Error as e:
            self.logger.error(f"Error creating record: {e}")
            raise
    
    def update(self, model: T) -> Optional[T]:
        """Update an existing record in the database
        
        Args:
            model: Model instance to update
            
        Returns:
            Updated model or None on failure
        """
        if not hasattr(model, 'id') or model.id is None:
            raise ValueError("Model must have an ID to be updated")
        
        # Get column names from table info
        columns_info = self.db_connection.get_table_info(self.table_name)
        # Filter out id, created_at, updated_at columns
        columns = [col['name'] for col in columns_info 
                  if col['name'] not in ('id', 'created_at', 'updated_at')]
        
        # Create SET clause for SQL query
        set_clause = ', '.join([f"{col} = ?" for col in columns])
        
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        
        try:
            # Convert model to tuple and add ID at the end for WHERE clause
            data_tuple = model.to_tuple() + (model.id,)
            
            # Execute the query
            self.db_connection.execute_query(query, data_tuple)
            
            # Return the updated model
            return self.find_by_id(model.id)
        except sqlite3.Error as e:
            self.logger.error(f"Error updating record with ID {model.id}: {e}")
            raise
    
    def delete(self, id_value: int) -> bool:
        """Delete a record from the database
        
        Args:
            id_value: ID of the record to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (id_value,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error deleting record with ID {id_value}: {e}")
            raise
    
    def count(self) -> int:
        """Count the number of records in the table
        
        Returns:
            Number of records
        """
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        
        try:
            results = self.db_connection.execute_query(query)
            if results and len(results) > 0:
                return results[0][0]
            return 0
        except sqlite3.Error as e:
            self.logger.error(f"Error counting records: {e}")
            raise
    
    def find_by_field(self, field_name: str, value: Any) -> List[T]:
        """Find records by a specific field value
        
        Args:
            field_name: Name of the field to search by
            value: Value to search for
            
        Returns:
            List of matching model instances
        """
        query = f"SELECT * FROM {self.table_name} WHERE {field_name} = ?"
        
        try:
            results = self.db_connection.execute_query(query, (value,))
            if not results:
                return []
                
            models = []
            for row in results:
                data_tuple = tuple(row)
                model = self.model_class.from_tuple(data_tuple)
                if model:
                    models.append(model)
            return models
        except sqlite3.Error as e:
            self.logger.error(f"Error finding records by {field_name}={value}: {e}")
            raise
    
    def exists(self, id_value: int) -> bool:
        """Check if a record exists by ID
        
        Args:
            id_value: ID to check
            
        Returns:
            True if record exists, False otherwise
        """
        query = f"SELECT 1 FROM {self.table_name} WHERE id = ? LIMIT 1"
        
        try:
            results = self.db_connection.execute_query(query, (id_value,))
            return results is not None and len(results) > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error checking if record exists with ID {id_value}: {e}")
            raise