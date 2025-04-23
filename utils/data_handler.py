import pandas as pd
import os
import json
from datetime import datetime
import numpy as np

# Define data directory
DATA_DIR = "data"

# Ensure data directory exists
def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# File paths
FRUITS_FILE = os.path.join(DATA_DIR, "fruits.csv")
SALES_FILE = os.path.join(DATA_DIR, "sales.json")

def load_fruit_data():
    """
    Load fruit inventory data from CSV file.
    If file doesn't exist, create a sample dataset.
    
    Returns:
        pandas.DataFrame: DataFrame containing fruit inventory data
    """
    ensure_data_dir()
    
    if os.path.exists(FRUITS_FILE):
        try:
            return pd.read_csv(FRUITS_FILE)
        except Exception as e:
            print(f"Error loading fruit data: {e}")
            return create_sample_fruit_data()
    else:
        return create_sample_fruit_data()

def save_fruit_data(df):
    """
    Save fruit inventory data to CSV file.
    
    Args:
        df (pandas.DataFrame): DataFrame containing fruit inventory data
    """
    ensure_data_dir()
    
    try:
        df.to_csv(FRUITS_FILE, index=False)
    except Exception as e:
        print(f"Error saving fruit data: {e}")

def create_sample_fruit_data():
    """
    Create sample fruit inventory data.
    
    Returns:
        pandas.DataFrame: DataFrame containing sample fruit inventory data
    """
    sample_fruits = [
        {
            'name': 'Apple',
            'price': 1.99,
            'quantity': 150,
            'category': 'Core Fruits',
            'origin': 'USA',
            'organic': True,
            'description': 'Fresh red apples, perfect for snacking or baking.'
        },
        {
            'name': 'Banana',
            'price': 0.59,
            'quantity': 200,
            'category': 'Tropical',
            'origin': 'Ecuador',
            'organic': False,
            'description': 'Ripe yellow bananas, rich in potassium.'
        },
        {
            'name': 'Orange',
            'price': 1.29,
            'quantity': 100,
            'category': 'Citrus',
            'origin': 'Florida',
            'organic': True,
            'description': 'Juicy oranges, excellent source of vitamin C.'
        },
        {
            'name': 'Strawberry',
            'price': 3.99,
            'quantity': 50,
            'category': 'Berries',
            'origin': 'California',
            'organic': True,
            'description': 'Sweet red strawberries, perfect for desserts.'
        },
        {
            'name': 'Mango',
            'price': 2.49,
            'quantity': 75,
            'category': 'Tropical',
            'origin': 'Mexico',
            'organic': False,
            'description': 'Sweet and juicy mangoes, tropical delight.'
        },
        {
            'name': 'Blueberry',
            'price': 4.99,
            'quantity': 40,
            'category': 'Berries',
            'origin': 'Maine',
            'organic': True,
            'description': 'Antioxidant-rich blueberries, great for smoothies.'
        },
        {
            'name': 'Watermelon',
            'price': 5.99,
            'quantity': 30,
            'category': 'Melons',
            'origin': 'Texas',
            'organic': False,
            'description': 'Refreshing watermelon, perfect for hot summer days.'
        },
        {
            'name': 'Pineapple',
            'price': 3.49,
            'quantity': 45,
            'category': 'Tropical',
            'origin': 'Costa Rica',
            'organic': False,
            'description': 'Sweet and tangy pineapple, tropical favorite.'
        },
        {
            'name': 'Grapes',
            'price': 2.99,
            'quantity': 80,
            'category': 'Berries',
            'origin': 'California',
            'organic': True,
            'description': 'Sweet seedless grapes, perfect snack.'
        },
        {
            'name': 'Peach',
            'price': 1.79,
            'quantity': 65,
            'category': 'Stone Fruits',
            'origin': 'Georgia',
            'organic': True,
            'description': 'Juicy peaches, summer favorite.'
        },
        {
            'name': 'Kiwi',
            'price': 0.99,
            'quantity': 90,
            'category': 'Exotic',
            'origin': 'New Zealand',
            'organic': False,
            'description': 'Tangy kiwi fruit, rich in vitamin C.'
        },
        {
            'name': 'Lemon',
            'price': 0.79,
            'quantity': 120,
            'category': 'Citrus',
            'origin': 'Italy',
            'organic': True,
            'description': 'Zesty lemons, perfect for cooking and drinks.'
        },
        {
            'name': 'Avocado',
            'price': 2.29,
            'quantity': 60,
            'category': 'Other',
            'origin': 'Mexico',
            'organic': True,
            'description': 'Creamy avocados, great for guacamole.'
        },
        {
            'name': 'Cherry',
            'price': 4.49,
            'quantity': 35,
            'category': 'Stone Fruits',
            'origin': 'Washington',
            'organic': False,
            'description': 'Sweet cherries, summer treat.'
        },
        {
            'name': 'Pear',
            'price': 1.89,
            'quantity': 70,
            'category': 'Core Fruits',
            'origin': 'Oregon',
            'organic': True,
            'description': 'Juicy pears, sweet and refreshing.'
        }
    ]
    
    df = pd.DataFrame(sample_fruits)
    save_fruit_data(df)
    return df

def load_sales_data():
    """
    Load sales data from JSON file.
    If file doesn't exist, create an empty DataFrame.
    
    Returns:
        pandas.DataFrame: DataFrame containing sales data
    """
    ensure_data_dir()
    
    if os.path.exists(SALES_FILE):
        try:
            with open(SALES_FILE, 'r') as f:
                sales_data = json.load(f)
            
            # Convert to DataFrame
            if sales_data:
                return pd.DataFrame(sales_data)
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading sales data: {e}")
            return create_sample_sales_data()
    else:
        return create_sample_sales_data()

def save_sales_data(df):
    """
    Save sales data to JSON file.
    
    Args:
        df (pandas.DataFrame): DataFrame containing sales data
    """
    ensure_data_dir()
    
    try:
        # Convert DataFrame to list of dictionaries
        sales_data = df.to_dict('records')
        
        with open(SALES_FILE, 'w') as f:
            json.dump(sales_data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving sales data: {e}")

def create_sample_sales_data():
    """
    Create sample sales data.
    
    Returns:
        pandas.DataFrame: DataFrame containing sample sales data
    """
    # Load fruit data to use for sample sales
    fruits_df = load_fruit_data()
    
    if fruits_df.empty:
        return pd.DataFrame()
    
    # Create sample sales
    sample_sales = []
    
    # Generate sales for the past 30 days
    end_date = datetime.now()
    start_date = end_date - pd.Timedelta(days=30)
    
    # Generate random dates
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    # Filter to business hours (8am-8pm)
    dates = dates[dates.hour.isin(range(8, 21))]
    
    # Sample random dates
    sale_dates = np.random.choice(dates, size=50, replace=False)
    
    payment_methods = ["Cash", "Credit Card", "Debit Card", "Mobile Payment"]
    customer_names = [
        "Walk-in Customer", "John Smith", "Maria Garcia", "James Johnson", 
        "Sarah Williams", "David Brown", "Lisa Davis", "Michael Miller",
        "Emma Wilson", "Robert Moore", "Walk-in Customer", "Walk-in Customer"
    ]
    
    for i, sale_date in enumerate(sorted(sale_dates)):
        # Generate 1-5 items per sale
        num_items = np.random.randint(1, 6)
        
        # Sample random fruits
        sale_fruits = fruits_df.sample(n=min(num_items, len(fruits_df)))
        
        items = []
        total_amount = 0
        
        for _, fruit in sale_fruits.iterrows():
            # Random quantity between 1 and 5
            quantity = np.random.randint(1, 6)
            
            # Calculate item total
            item_total = quantity * fruit['price']
            total_amount += item_total
            
            items.append({
                'fruit': fruit['name'],
                'quantity': quantity,
                'unit_price': fruit['price'],
                'total': item_total
            })
        
        # Create sale record
        sale = {
            'sale_id': f"SALE-{i+1:04d}",
            'date': sale_date,
            'customer': np.random.choice(customer_names),
            'payment_method': np.random.choice(payment_methods),
            'receipt_number': f"R-{np.random.randint(10000, 100000)}",
            'items': items,
            'total_amount': total_amount
        }
        
        sample_sales.append(sale)
    
    df = pd.DataFrame(sample_sales)
    save_sales_data(df)
    return df

def backup_data():
    """
    Create backup of all data files.
    """
    ensure_data_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup fruits data
    if os.path.exists(FRUITS_FILE):
        backup_file = os.path.join(DATA_DIR, f"fruits_backup_{timestamp}.csv")
        try:
            with open(FRUITS_FILE, 'r') as src, open(backup_file, 'w') as dst:
                dst.write(src.read())
            print(f"Fruits data backed up to {backup_file}")
        except Exception as e:
            print(f"Error backing up fruits data: {e}")
    
    # Backup sales data
    if os.path.exists(SALES_FILE):
        backup_file = os.path.join(DATA_DIR, f"sales_backup_{timestamp}.json")
        try:
            with open(SALES_FILE, 'r') as src, open(backup_file, 'w') as dst:
                dst.write(src.read())
            print(f"Sales data backed up to {backup_file}")
        except Exception as e:
            print(f"Error backing up sales data: {e}")

def restore_data_from_backup(fruits_backup=None, sales_backup=None):
    """
    Restore data from backup files.
    
    Args:
        fruits_backup (str): Path to fruits backup file
        sales_backup (str): Path to sales backup file
    
    Returns:
        bool: True if restore was successful, False otherwise
    """
    success = True
    
    # Restore fruits data
    if fruits_backup and os.path.exists(fruits_backup):
        try:
            with open(fruits_backup, 'r') as src, open(FRUITS_FILE, 'w') as dst:
                dst.write(src.read())
            print(f"Fruits data restored from {fruits_backup}")
        except Exception as e:
            print(f"Error restoring fruits data: {e}")
            success = False
    
    # Restore sales data
    if sales_backup and os.path.exists(sales_backup):
        try:
            with open(sales_backup, 'r') as src, open(SALES_FILE, 'w') as dst:
                dst.write(src.read())
            print(f"Sales data restored from {sales_backup}")
        except Exception as e:
            print(f"Error restoring sales data: {e}")
            success = False
    
    return success

def get_backup_files():
    """
    Get list of available backup files.
    
    Returns:
        dict: Dictionary with lists of fruits and sales backup files
    """
    ensure_data_dir()
    
    fruits_backups = []
    sales_backups = []
    
    for file in os.listdir(DATA_DIR):
        if file.startswith("fruits_backup_") and file.endswith(".csv"):
            fruits_backups.append(os.path.join(DATA_DIR, file))
        elif file.startswith("sales_backup_") and file.endswith(".json"):
            sales_backups.append(os.path.join(DATA_DIR, file))
    
    return {
        'fruits': sorted(fruits_backups, reverse=True),
        'sales': sorted(sales_backups, reverse=True)
    }

def export_data_to_excel(output_file):
    """
    Export all data to Excel file.
    
    Args:
        output_file (str): Path to output Excel file
    
    Returns:
        bool: True if export was successful, False otherwise
    """
    try:
        # Load data
        fruits_df = load_fruit_data()
        sales_df = load_sales_data()
        
        # Create Excel writer
        with pd.ExcelWriter(output_file) as writer:
            fruits_df.to_excel(writer, sheet_name='Inventory', index=False)
            
            if not sales_df.empty:
                # For sales, we need to handle the items column which contains lists
                sales_export = sales_df.copy()
                
                # Convert items column to string representation
                sales_export['items'] = sales_export['items'].apply(lambda x: str(x))
                
                sales_export.to_excel(writer, sheet_name='Sales', index=False)
        
        return True
    except Exception as e:
        print(f"Error exporting data to Excel: {e}")
        return False