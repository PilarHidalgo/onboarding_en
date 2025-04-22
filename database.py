# File: services/database_service.py
"""Database service for handling database connections and operations"""
import os
import sqlite3
from sqlite3 import Connection
from typing import Optional

from config import AppConfig

class DatabaseService:
    """Service for database operations implementing Repository pattern"""
    
    def __init__(self):
        """Initialize the database connection"""
        self.connection = self._init_connection()
    
    def _init_connection(self) -> Connection:
        """Create a connection to the SQLite database"""
        # Create data directory if it doesn't exist
        if not os.path.exists(AppConfig.DATA_DIR):
            os.makedirs(AppConfig.DATA_DIR)
        
        # Connect to the database (will create it if it doesn't exist)
        conn = sqlite3.connect(AppConfig.DATABASE_PATH, check_same_thread=False)
        
        # Create tables if they don't exist
        self._create_tables(conn)
        
        return conn
    
    def _create_tables(self, conn: Connection) -> None:
        """Create necessary tables if they don't exist"""
        cursor = conn.cursor()
        
        # Create fruits table with image_path column
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS fruits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create a trigger to update the updated_at timestamp
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_fruit_timestamp 
        AFTER UPDATE ON fruits
        FOR EACH ROW
        BEGIN
            UPDATE fruits SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
        END;
        ''')
        
        # Commit the changes
        conn.commit()
    
    def get_connection(self) -> Connection:
        """Get the database connection"""
        return self.connection
    
    def execute_query(self, query: str, params=()) -> sqlite3.Cursor:
        """Execute a database query with parameters"""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor
    
    def commit(self) -> None:
        """Commit changes to the database"""
        self.connection.commit()
