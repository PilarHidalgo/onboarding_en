"""Database package initialization"""
from .connection import DatabaseConnection
from .base_repository import BaseRepository
from .fruit_repository import FruitRepository

__all__ = [
    'DatabaseConnection',
    'BaseRepository',
    'FruitRepository',
    'initialize_database'
]

# Version of the database package
__version__ = '1.0.0'

# Package metadata
__author__ = 'Your Name'
__email__ = 'your.email@example.com'
__description__ = 'Database access layer for the Fruit Store Management System'

def initialize_database(db_path: str) -> tuple:
    """Initialize database connection and repositories
    
    This function creates a database connection and initializes
    all repositories needed by the application.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Tuple containing all initialized repositories
    """
    # Create database connection
    db_connection = DatabaseConnection(db_path)
    
    # Create database tables if they don't exist
    db_connection.create_tables()
    
    # Initialize repositories
    fruit_repository = FruitRepository(db_connection)
    
    # Return all repositories
    return (fruit_repository,)