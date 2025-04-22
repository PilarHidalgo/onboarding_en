"""File service implementation for file operations"""
import os
import csv
import json
import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import shutil
import tempfile

from models import Fruit
from .base_service import BaseService
from database import FruitRepository

class FileService:
    """Service for file operations
    
    Handles import/export operations for various file formats
    and manages file-based data operations.
    """
    
    def __init__(self, fruit_repository: FruitRepository):
        """Initialize the file service
        
        Args:
            fruit_repository: Repository for fruit data access
        """
        self.fruit_repository = fruit_repository
        self.logger = logging.getLogger(__name__)
    
    def export_to_csv(self, filepath: str, fruits: Optional[List[Fruit]] = None) -> bool:
        """Export fruits to CSV file
        
        Args:
            filepath: Path to save the CSV file
            fruits: List of fruits to export (if None, exports all fruits)
            
        Returns:
            True if export was successful, False otherwise
            
        Raises:
            ValueError: If filepath is invalid
            IOError: If file cannot be written
        """
        if not filepath or not isinstance(filepath, str):
            raise ValueError("Invalid filepath")
            
        try:
            # If no fruits provided, get all fruits
            if fruits is None:
                fruits = self.fruit_repository.find_all()
                
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            # Write to temporary file first to avoid corrupting existing file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as temp_file:
                writer = csv.writer(temp_file)
                
                # Write header
                writer.writerow(['id', 'name', 'category', 'price', 'quantity', 'created_at', 'updated_at'])
                
                # Write data
                for fruit in fruits:
                    writer.writerow([
                        fruit.id,
                        fruit.name,
                        fruit.category,
                        fruit.price,
                        fruit.quantity,
                        fruit.created_at.isoformat() if fruit.created_at else '',
                        fruit.updated_at.isoformat() if fruit.updated_at else ''
                    ])
                
                temp_filename = temp_file.name
                
            # Move temporary file to destination
            shutil.move(temp_filename, filepath)
            
            self.logger.info(f"Successfully exported {len(fruits)} fruits to CSV: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting fruits to CSV: {e}")
            # Clean up temporary file if it exists
            if 'temp_filename' in locals() and os.path.exists(temp_filename):
                os.unlink(temp_filename)
            raise
    
    def import_from_csv(self, filepath: str) -> List[Fruit]:
        """Import fruits from CSV file
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            List of imported fruits
            
        Raises:
            ValueError: If filepath is invalid or file format is incorrect
            FileNotFoundError: If file does not exist
            IOError: If file cannot be read
        """
        if not filepath or not isinstance(filepath, str):
            raise ValueError("Invalid filepath")
            
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        try:
            imported_fruits = []
            
            with open(filepath, 'r', newline='') as file:
                reader = csv.reader(file)
                
                # Read header
                header = next(reader, None)
                if not header or 'name' not in header and 'category' not in header:
                    raise ValueError("Invalid CSV format: missing required headers")
                
                # Get column indices
                try:
                    id_idx = header.index('id') if 'id' in header else None
                    name_idx = header.index('name')
                    category_idx = header.index('category')
                    price_idx = header.index('price')
                    quantity_idx = header.index('quantity')
                    created_at_idx = header.index('created_at') if 'created_at' in header else None
                    updated_at_idx = header.index('updated_at') if 'updated_at' in header else None
                except ValueError as e:
                    raise ValueError(f"Invalid CSV format: {e}")
                
                # Read data
                for row in reader:
                    if len(row) < 4:  # At minimum need name, category, price, quantity
                        continue
                    
                    try:
                        # Create fruit data dictionary
                        fruit_data = {
                            'name': row[name_idx],
                            'category': row[category_idx],
                            'price': float(row[price_idx]),
                            'quantity': int(row[quantity_idx])
                        }
                        
                        # Add ID if present
                        if id_idx is not None and row[id_idx]:
                            fruit_data['id'] = int(row[id_idx])
                        
                        # Add timestamps if present
                        if created_at_idx is not None and row[created_at_idx]:
                            fruit_data['created_at'] = datetime.fromisoformat(row[created_at_idx])
                        if updated_at_idx is not None and row[updated_at_idx]:
                            fruit_data['updated_at'] = datetime.fromisoformat(row[updated_at_idx])
                        
                        # Create or update fruit
                        if 'id' in fruit_data:
                            # Check if fruit exists
                            existing_fruit = self.fruit_repository.find_by_id(fruit_data['id'])
                            if existing_fruit:
                                # Update existing fruit
                                for key, value in fruit_data.items():
                                    if key != 'id':
                                        setattr(existing_fruit, key, value)
                                fruit = self.fruit_repository.update(existing_fruit)
                            else:
                                # Create new fruit with specified ID
                                fruit = Fruit.from_dict(fruit_data)
                                fruit = self.fruit_repository.create(fruit)
                        else:
                            # Create new fruit
                            fruit = Fruit.from_dict(fruit_data)
                            fruit = self.fruit_repository.create(fruit)
                        
                        if fruit:
                            imported_fruits.append(fruit)
                            
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"Skipping invalid row: {e}")
                        continue
            
            self.logger.info(f"Successfully imported {len(imported_fruits)} fruits from CSV: {filepath}")
            return imported_fruits
            
        except Exception as e:
            self.logger.error(f"Error importing fruits from CSV: {e}")
            raise
    
    def export_to_json(self, filepath: str, fruits: Optional[List[Fruit]] = None) -> bool:
        """Export fruits to JSON file
        
        Args:
            filepath: Path to save the JSON file
            fruits: List of fruits to export (if None, exports all fruits)
            
        Returns:
            True if export was successful, False otherwise
            
        Raises:
            ValueError: If filepath is invalid
            IOError: If file cannot be written
        """
        if not filepath or not isinstance(filepath, str):
            raise ValueError("Invalid filepath")
            
        try:
            # If no fruits provided, get all fruits
            if fruits is None:
                fruits = self.fruit_repository.find_all()
                
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            # Convert fruits to dictionaries
            fruit_dicts = []
            for fruit in fruits:
                fruit_dict = fruit.to_dict()
                # Convert datetime objects to ISO format strings
                if fruit_dict.get('created_at'):
                    fruit_dict['created_at'] = fruit_dict['created_at'].isoformat()
                if fruit_dict.get('updated_at'):
                    fruit_dict['updated_at'] = fruit_dict['updated_at'].isoformat()
                fruit_dicts.append(fruit_dict)
            
            # Write to temporary file first
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                json.dump(fruit_dicts, temp_file, indent=2)
                temp_filename = temp_file.name
            
            # Move temporary file to destination
            shutil.move(temp_filename, filepath)
            
            self.logger.info(f"Successfully exported {len(fruits)} fruits to JSON: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting fruits to JSON: {e}")
            # Clean up temporary file if it exists
            if 'temp_filename' in locals() and os.path.exists(temp_filename):
                os.unlink(temp_filename)
            raise
    
    def import_from_json(self, filepath: str) -> List[Fruit]:
        """Import fruits from JSON file
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            List of imported fruits
            
        Raises:
            ValueError: If filepath is invalid or file format is incorrect
            FileNotFoundError: If file does not exist
            IOError: If file cannot be read
        """
        if not filepath or not isinstance(filepath, str):
            raise ValueError("Invalid filepath")
            
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        try:
            imported_fruits = []
            
            with open(filepath, 'r') as file:
                fruit_dicts = json.load(file)
                
                if not isinstance(fruit_dicts, list):
                    raise ValueError("Invalid JSON format: expected a list of fruits")
                
                for fruit_dict in fruit_dicts:
                    try:
                        # Convert ISO format strings to datetime objects
                        if 'created_at' in fruit_dict and fruit_dict['created_at']:
                            fruit_dict['created_at'] = datetime.fromisoformat(fruit_dict['created_at'])
                        if 'updated_at' in fruit_dict and fruit_dict['updated_at']:
                            fruit_dict['updated_at'] = datetime.fromisoformat(fruit_dict['updated_at'])
                        
                        # Create or update fruit
                        if 'id' in fruit_dict:
                            # Check if fruit exists
                            existing_fruit = self.fruit_repository.find_by_id(fruit_dict['id'])
                            if existing_fruit:
                                # Update existing fruit
                                for key, value in fruit_dict.items():
                                    if key != 'id':
                                        setattr(existing_fruit, key, value)
                                fruit = self.fruit_repository.update(existing_fruit)
                            else:
                                # Create new fruit with specified ID
                                fruit = Fruit.from_dict(fruit_dict)
                                fruit = self.fruit_repository.create(fruit)
                        else:
                            # Create new fruit
                            fruit = Fruit.from_dict(fruit_dict)
                            fruit = self.fruit_repository.create(fruit)
                        
                        if fruit:
                            imported_fruits.append(fruit)
                            
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"Skipping invalid fruit data: {e}")
                        continue
            
            self.logger.info(f"Successfully imported {len(imported_fruits)} fruits from JSON: {filepath}")
            return imported_fruits
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format: {e}")
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            self.logger.error(f"Error importing fruits from JSON: {e}")
            raise
    
    def backup_database(self, backup_dir: str) -> str:
        """Backup the database to a file
        
        Args:
            backup_dir: Directory to save the backup
            
        Returns:
            Path to the backup file
            
        Raises:
            ValueError: If backup_dir is invalid
            IOError: If backup cannot be created
        """
        if not backup_dir or not isinstance(backup_dir, str):
            raise ValueError("Invalid backup directory")
            
        try:
            # Create backup directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"fruit_db_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Export all fruits to JSON
            self.export_to_json(backup_path)
            
            self.logger.info(f"Database backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Error creating database backup: {e}")
            raise
    
    def restore_database(self, backup_path: str) -> int:
        """Restore the database from a backup file
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            Number of restored fruits
            
        Raises:
            ValueError: If backup_path is invalid
            FileNotFoundError: If backup file does not exist
            IOError: If backup cannot be read
        """
        if not backup_path or not isinstance(backup_path, str):
            raise ValueError("Invalid backup path")
            
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
        try:
            # Import fruits from backup
            imported_fruits = self.import_from_json(backup_path)
            
            self.logger.info(f"Database restored from backup: {backup_path}")
            return len(imported_fruits)
            
        except Exception as e:
            self.logger.error(f"Error restoring database from backup: {e}")
            raise