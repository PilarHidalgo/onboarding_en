"""Database connection management and configuration"""
import sqlite3
from typing import Optional, Union, Tuple, List
from contextlib import contextmanager
import logging
from pathlib import Path

class DatabaseConnection:
    """Manages database connections and provides query execution capabilities"""
    
    def __init__(self, db_path: Union[str, Path]):
        """Initialize database connection manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = str(db_path)
        self._connection: Optional[sqlite3.Connection] = None
        self.setup_logging()
        
    def setup_logging(self) -> None:
        """Configure logging for database operations"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Create handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    @contextmanager
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection using context manager
        
        Yields:
            Active database connection
            
        Raises:
            sqlite3.Error: If connection fails
        """
        try:
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row
            yield connection
            connection.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()

    def execute_query(
        self, 
        query: str, 
        parameters: Tuple = ()
    ) -> Optional[List[sqlite3.Row]]:
        """Execute a SQL query and return results
        
        Args:
            query: SQL query string
            parameters: Query parameters tuple
            
        Returns:
            List of query results or None on error
            
        Raises:
            sqlite3.Error: If query execution fails
        """
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, parameters)
                return cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Query execution error: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Parameters: {parameters}")
            raise

    def execute_many(
        self, 
        query: str, 
        parameters: List[Tuple]
    ) -> None:
        """Execute multiple SQL queries
        
        Args:
            query: SQL query string
            parameters: List of parameter tuples
            
        Raises:
            sqlite3.Error: If query execution fails
        """
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.executemany(query, parameters)
        except sqlite3.Error as e:
            self.logger.error(f"Batch execution error: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Parameters: {parameters}")
            raise

    def create_tables(self) -> None:
        """Create database tables if they don't exist"""
        create_fruits_table = """
        CREATE TABLE IF NOT EXISTS fruits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_trigger = """
        CREATE TRIGGER IF NOT EXISTS update_fruits_timestamp 
        AFTER UPDATE ON fruits
        BEGIN
            UPDATE fruits SET updated_at = CURRENT_TIMESTAMP 
            WHERE id = NEW.id;
        END;
        """
        
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(create_fruits_table)
                cursor.execute(create_trigger)
                self.logger.info("Database tables created successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error creating tables: {e}")
            raise

    def get_table_info(self, table_name: str) -> List[sqlite3.Row]:
        """Get information about table columns
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information
        """
        return self.execute_query(f"PRAGMA table_info({table_name});")