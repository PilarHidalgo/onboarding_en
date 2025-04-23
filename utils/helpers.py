import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

def calculate_total(df):
    """
    Calculate the total inventory value
    
    Args:
        df: DataFrame containing 'price' and 'stock' columns
        
    Returns:
        float: Total inventory value
    """
    return (df['price'] * df['stock']).sum()

def apply_discount(code, total):
    """
    Apply discount based on the provided code
    
    Args:
        code: Discount code string
        total: Total amount before discount
        
    Returns:
        float: Discount amount
    """
    # Standard discount codes
    discount_codes = {
        'FRESH10': 0.10,  # 10% off
        'FRUIT20': 0.20,  # 20% off
        'WELCOME15': 0.15,  # 15% off
        'SUMMER25': 0.25,  # 25% off
    }
    
    # Check for fixed amount discount (e.g., SAVE5 for $5 off)
    fixed_match = re.match(r'SAVE(\d+)', code)
    
    if code.upper() in discount_codes:
        return total * discount_codes[code.upper()]
    elif fixed_match:
        amount = int(fixed_match.group(1))
        return min(amount, total)  # Don't discount more than the total
    else:
        return 0.0

def get_seasonal_fruits():
    """
    Get a list of seasonal fruits based on the current month
    
    Returns:
        list: List of seasonal fruits
    """
    current_month = datetime.now().month
    
    seasonal_fruits = {
        # Winter (Dec-Feb)
        12: ['Orange', 'Grapefruit', 'Kiwi', 'Pear', 'Pomegranate'],
        1: ['Orange', 'Grapefruit', 'Kiwi', 'Pear', 'Pomegranate'],
        2: ['Orange', 'Grapefruit', 'Kiwi', 'Pear', 'Pomegranate'],
        
        # Spring (Mar-May)
        3: ['Strawberry', 'Pineapple', 'Mango', 'Apricot'],
        4: ['Strawberry', 'Pineapple', 'Mango', 'Apricot', 'Cherry'],
        5: ['Strawberry', 'Pineapple', 'Mango', 'Cherry', 'Melon'],
        
        # Summer (Jun-Aug)
        6: ['Watermelon', 'Peach', 'Plum', 'Blueberry', 'Raspberry'],
        7: ['Watermelon', 'Peach', 'Plum', 'Blueberry', 'Raspberry', 'Blackberry'],
        8: ['Watermelon', 'Peach', 'Plum', 'Apple', 'Blackberry', 'Fig'],
        
        # Fall (Sep-Nov)
        9: ['Apple', 'Pear', 'Grape', 'Fig', 'Persimmon'],
        10: ['Apple', 'Pear', 'Grape', 'Persimmon', 'Cranberry'],
        11: ['Apple', 'Pear', 'Cranberry', 'Pomegranate', 'Orange']
    }
    
    return seasonal_fruits.get(current_month, ['Apple', 'Banana', 'Orange'])  # Default fruits if month not found

def format_currency(amount):
    """
    Format a number as currency
    
    Args:
        amount: Number to format
        
    Returns:
        str: Formatted currency string
    """
    return f"${amount:.2f}"

def calculate_discount_price(original_price, discount_percentage):
    """
    Calculate the discounted price
    
    Args:
        original_price: Original price
        discount_percentage: Discount percentage (0-100)
        
    Returns:
        float: Discounted price
    """
    return original_price * (1 - (discount_percentage / 100))

def get_expiry_date(days=7):
    """
    Calculate an expiry date from today
    
    Args:
        days: Number of days until expiry
        
    Returns:
        str: Formatted date string
    """
    expiry_date = datetime.now() + timedelta(days=days)
    return expiry_date.strftime("%Y-%m-%d")

def filter_organic(df, organic_only=False):
    """
    Filter dataframe for organic products
    
    Args:
        df: DataFrame with an 'organic' column
        organic_only: If True, return only organic products
        
    Returns:
        DataFrame: Filtered dataframe
    """
    if organic_only:
        return df[df['organic'] == True]
    return df

def calculate_nutrition(fruit_name):
    """
    Return estimated nutrition facts for a fruit
    
    Args:
        fruit_name: Name of the fruit
        
    Returns:
        dict: Dictionary with nutrition information
    """
    # Simplified nutrition data (per 100g)
    nutrition_data = {
        'Apple': {'calories': 52, 'carbs': 14, 'fiber': 2.4, 'sugar': 10},
        'Banana': {'calories': 89, 'carbs': 23, 'fiber': 2.6, 'sugar': 12},
        'Orange': {'calories': 47, 'carbs': 12, 'fiber': 2.4, 'sugar': 9},
        'Strawberry': {'calories': 32, 'carbs': 8, 'fiber': 2.0, 'sugar': 4.9},
        'Mango': {'calories': 60, 'carbs': 15, 'fiber': 1.6, 'sugar': 14},
        'Pineapple': {'calories': 50, 'carbs': 13, 'fiber': 1.4, 'sugar': 10},
        'Grapes': {'calories': 69, 'carbs': 18, 'fiber': 0.9, 'sugar': 16},
        'Watermelon': {'calories': 30, 'carbs': 8, 'fiber': 0.4, 'sugar': 6},
    }
    
    # Return default values if fruit not in database
    default = {'calories': 50, 'carbs': 10, 'fiber': 2.0, 'sugar': 8}
    return nutrition_data.get(fruit_name, default)

def generate_fruit_recommendation(purchase_history):
    """
    Generate fruit recommendations based on purchase history
    
    Args:
        purchase_history: List of previously purchased fruits
        
    Returns:
        list: List of recommended fruits
    """
    # Simple recommendation system
    fruit_affinities = {
        'Apple': ['Pear', 'Grapes', 'Strawberry'],
        'Banana': ['Mango', 'Pineapple', 'Strawberry'],
        'Orange': ['Lemon', 'Lime', 'Grapefruit'],
        'Strawberry': ['Blueberry', 'Raspberry', 'Blackberry'],
        'Mango': ['Pineapple', 'Papaya', 'Banana'],
        'Pineapple': ['Mango', 'Banana', 'Kiwi'],
        'Grapes': ['Apple', 'Pear', 'Plum'],
        'Watermelon': ['Cantaloupe', 'Honeydew', 'Pineapple'],
    }
    
    recommendations = []
    for fruit in purchase_history:
        if fruit in fruit_affinities:
            recommendations.extend(fruit_affinities[fruit])
    
    # Remove duplicates and already purchased items
    recommendations = list(set(recommendations) - set(purchase_history))
    
    # Return top 3 recommendations or fewer if not enough
    return recommendations[:3]

# Add to utils/helpers.py

def generate_receipt(cart_items, subtotal, discount=0.0, total=None):
    """
    Generate a formatted receipt string
    
    Args:
        cart_items: Dictionary of items in cart with quantities and prices
        subtotal: Original total before discount
        discount: Discount amount applied (default 0.0)
        total: Final total after discount (if None, will be calculated)
        
    Returns:
        str: Formatted receipt string
    """
    if total is None:
        total = subtotal - discount
    
    # Get current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build receipt
    receipt = [
        "=" * 40,
        "FRESH FRUITS MARKET",
        "=" * 40,
        f"Date: {current_time}",
        "-" * 40,
        "ITEMS:",
        "-" * 40,
    ]
    
    # Add items
    for item, details in cart_items.items():
        qty = details['quantity']
        price = details['price']
        item_total = details['total']
        receipt.append(f"{item:<20} {qty:>3} x ${price:>6.2f} = ${item_total:>7.2f}")
    
    # Add totals
    receipt.extend([
        "-" * 40,
        f"{'Subtotal:':<30} ${subtotal:>7.2f}",
    ])
    
    # Add discount if any
    if discount > 0:
        receipt.append(f"{'Discount:':<30} ${discount:>7.2f}")
    
    receipt.extend([
        f"{'Total:':<30} ${total:>7.2f}",
        "=" * 40,
        "Thank you for shopping with us!",
        "Please come again!",
        "=" * 40
    ])
    
    return "\n".join(receipt)
