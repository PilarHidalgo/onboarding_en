# File: crud.py
import streamlit as st

from sqlite3 import Connection
from typing import List, Tuple, Optional


def get_all_fruits(conn: Connection) -> List[Tuple]:
    """
    Retrieve all fruits from the database.
    
    Args:
        conn: Database connection
        
    Returns:
        List of tuples containing fruit data
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, quantity, category, image_path FROM fruits ORDER BY name")
    return cursor.fetchall()

def get_fruit_by_id(conn: Connection, fruit_id: int) -> Optional[Tuple]:
    """
    Retrieve a specific fruit by its ID.
    
    Args:
        conn: Database connection
        fruit_id: ID of the fruit to retrieve
        
    Returns:
        Tuple containing fruit data or None if not found
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, quantity, category, image_path FROM fruits WHERE id = ?", 
        (fruit_id,)
    )
    return cursor.fetchone()

def add_fruit(conn: Connection, name: str, price: float, quantity: int, category: str, image_path: str = None) -> int:
    """
    Add a new fruit to the database.
    
    Args:
        conn: Database connection
        name: Name of the fruit
        price: Price per unit
        quantity: Available quantity
        category: Category of the fruit
        image_path: Path to the fruit image
        
    Returns:
        ID of the newly added fruit
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fruits (name, price, quantity, category, image_path) VALUES (?, ?, ?, ?, ?)",
        (name, price, quantity, category, image_path)
    )
    conn.commit()
    return cursor.lastrowid

def update_fruit(conn: Connection, fruit_id: int, name: str, price: float, quantity: int, category: str, image_path: str = None) -> bool:
    """
    Update an existing fruit in the database.
    
    Args:
        conn: Database connection
        fruit_id: ID of the fruit to update
        name: New name of the fruit
        price: New price per unit
        quantity: New available quantity
        category: New category of the fruit
        image_path: Path to the fruit image
        
    Returns:
        True if the fruit was updated successfully, False otherwise
    """
    # If image_path is None, keep the existing image
    if image_path is None:
        cursor = conn.cursor()
        cursor.execute("SELECT image_path FROM fruits WHERE id = ?", (fruit_id,))
        result = cursor.fetchone()
        if result:
            image_path = result[0]
    
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE fruits SET name = ?, price = ?, quantity = ?, category = ?, image_path = ? WHERE id = ?",
        (name, price, quantity, category, image_path, fruit_id)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_fruit(conn: Connection, fruit_id: int) -> bool:
    """
    Delete a fruit from the database.
    
    Args:
        conn: Database connection
        fruit_id: ID of the fruit to delete
        
    Returns:
        True if the fruit was deleted successfully, False otherwise
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fruits WHERE id = ?", (fruit_id,))
    conn.commit()
    return cursor.rowcount > 0

def search_fruits(conn: Connection, search_term: str) -> List[Tuple]:
    """
    Search for fruits by name or category.
    
    Args:
        conn: Database connection
        search_term: Term to search for
        
    Returns:
        List of tuples containing matching fruit data
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, quantity, category, image_path FROM fruits WHERE name LIKE ? OR category LIKE ? ORDER BY name",
        (f"%{search_term}%", f"%{search_term}%")
    )
    return cursor.fetchall()

def get_fruits_by_category(conn: Connection, category: str) -> List[Tuple]:
    """
    Get all fruits in a specific category.
    
    Args:
        conn: Database connection
        category: Category to filter by
        
    Returns:
        List of tuples containing fruit data in the specified category
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, quantity, category, image_path FROM fruits WHERE category = ? ORDER BY name",
        (category,)
    )
    return cursor.fetchall()

def get_low_stock_fruits(conn: Connection, threshold: int = 10) -> List[Tuple]:
    """
    Get fruits with stock below a specified threshold.
    
    Args:
        conn: Database connection
        threshold: Quantity threshold for low stock
        
    Returns:
        List of tuples containing fruit data with low stock
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, quantity, category, image_path FROM fruits WHERE quantity < ? ORDER BY quantity",
        (threshold,)
    )
    return cursor.fetchall()

def get_total_inventory_value(conn: Connection) -> float:
    """
    Calculate the total value of all fruits in inventory.
    
    Args:
        conn: Database connection
        
    Returns:
        Total value of inventory
    """
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(price * quantity) FROM fruits")
    result = cursor.fetchone()[0]
    return float(result) if result is not None else 0.0

def get_category_statistics(conn: Connection) -> List[Tuple[str, int, float]]:
    """
    Get statistics for each fruit category.
    
    Args:
        conn: Database connection
        
    Returns:
        List of tuples containing (category, count, total_value)
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            category, 
            COUNT(*) as count, 
            SUM(price * quantity) as total_value 
        FROM fruits 
        GROUP BY category 
        ORDER BY total_value DESC
    """)
    return cursor.fetchall()
