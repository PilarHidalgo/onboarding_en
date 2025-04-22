import sqlite3
import os
from sqlite3 import Connection

def init_connection() -> Connection:
    """Create a connection to the SQLite database"""
    # Create a 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Connect to the database (will create it if it doesn't exist)
    conn = sqlite3.connect('data/fruit_store.db', check_same_thread=False)
    
    # Create tables if they don't exist
    create_tables(conn)
    
    return conn

def create_tables(conn: Connection):
    """Create necessary tables if they don't exist"""
    cursor = conn.cursor()
    
    # Create fruits table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fruits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        category TEXT NOT NULL,
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

def seed_sample_data(conn: Connection):
    """Seed the database with sample data if it's empty"""
    cursor = conn.cursor()
    
    # Check if the fruits table is empty
    cursor.execute("SELECT COUNT(*) FROM fruits")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert sample data
        sample_fruits = [
            ('Apple', 1.99, 100, 'Fresh Fruits'),
            ('Banana', 0.99, 150, 'Fresh Fruits'),
            ('Orange', 1.49, 80, 'Citrus'),
            ('Strawberry', 3.99, 50, 'Berries'),
            ('Mango', 2.99, 40, 'Exotic Fruits'),
            ('Pineapple', 3.99, 30, 'Exotic Fruits'),
            ('Grapes', 4.99, 60, 'Fresh Fruits'),
            ('Blueberry', 6.99, 45, 'Berries'),
            ('Kiwi', 1.99, 70, 'Exotic Fruits'),
            ('Lemon', 0.99, 90, 'Citrus'),
            ('Dried Apricot', 7.99, 25, 'Dried Fruits'),
            ('Raisins', 3.99, 35, 'Dried Fruits')
        ]
        
        cursor.executemany(
            "INSERT INTO fruits (name, price, quantity, category) VALUES (?, ?, ?, ?)",
            sample_fruits
        )
        
        conn.commit()