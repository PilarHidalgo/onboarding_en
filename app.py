# File: app.py
# Import required libraries
import streamlit as st  # Web app framework
import pandas as pd     # Data manipulation
import os
from datetime import datetime  # Added missing import for datetime
from utils.helpers import calculate_total, apply_discount, generate_receipt  # Added generate_receipt import

# Configure the Streamlit page layout and appearance
st.set_page_config(
    page_title="Fresh Fruits Market",
    page_icon="🍎",
    layout="wide"  # Use full width of the browser
)

# Load fruit data from CSV with caching for performance
@st.cache_data  # Cache data to avoid reloading on each interaction
def load_data():
    try:
        return pd.read_csv("data/fruits.csv")
    except FileNotFoundError:
        # Fallback data if CSV is missing
        default_data = {
            'name': ['Apple', 'Banana', 'Orange', 'Strawberry', 'Mango', 'Pineapple', 'Grapes', 'Watermelon'],
            'price': [1.2, 0.5, 0.8, 2.5, 2.0, 3.0, 4.0, 5.0],
            'stock': [100, 150, 80, 50, 30, 20, 60, 15],
            'category': ['Core Fruits', 'Tropical', 'Citrus', 'Berries', 'Tropical', 'Tropical', 'Berries', 'Melon'],
            'organic': [True, False, True, True, False, False, True, False]
        }
        return pd.DataFrame(default_data)

# Main application controller
def main():
    # Create sidebar with app title
    st.sidebar.title("Fresh Fruits Market 🍎🍌🍊")
    
    # Navigation menu in sidebar
    page = st.sidebar.radio("Navigation", ["Home", "Shop", "Inventory", "Analytics"])
    
    # Load fruit data
    fruits_df = load_data()
    
    # Route to appropriate page based on navigation selection
    if page == "Home":
        show_home_page()
    elif page == "Shop":
        show_shop_page(fruits_df)
    elif page == "Inventory":
        show_inventory_page(fruits_df)
    elif page == "Analytics":
        show_analytics_page(fruits_df)

# Home page with store information
def show_home_page():
    st.title("Welcome to Fresh Fruits Market! 🍓🥭🍍")
    
    # Display store information using markdown
    st.markdown("""
    ## About Us
    Fresh Fruits Market offers the best quality fruits sourced directly from local farmers.
    Our mission is to provide fresh, organic produce at affordable prices.
    
    ## Today's Specials
    * 🍎 **Apple Sale**: Buy 3 get 1 free!
    * 🍌 **Banana Bundle**: 20% off when you buy a bunch
    * 🥭 **Mango Madness**: Premium mangoes at discounted prices
    
    ## Store Hours
    - Monday to Friday: 8:00 AM - 8:00 PM
    - Saturday: 9:00 AM - 7:00 PM
    - Sunday: 10:00 AM - 5:00 PM
    """)
    
    # Call-to-action for users
    st.info("Visit our Shop page to browse our selection of fresh fruits!")

# Shop page with product listings and cart functionality
def show_shop_page(fruits_df):
    st.title("Shop Fresh Fruits 🛒")
    
    # Filter section in sidebar
    st.sidebar.header("Filter Options")
    
    # Category dropdown filter
    categories = ["All"] + sorted(fruits_df["category"].unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    # Organic/Conventional radio button filter
    organic_option = st.sidebar.radio("Type", ["All", "Organic Only", "Conventional Only"])
    
    # Price range slider filter
    min_price = float(fruits_df["price"].min())
    max_price = float(fruits_df["price"].max())
    price_range = st.sidebar.slider("Price Range ($)", min_price, max_price, (min_price, max_price))
    
    # Apply all selected filters to the dataframe
    filtered_df = fruits_df.copy()
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
        
    if organic_option == "Organic Only":
        filtered_df = filtered_df[filtered_df["organic"] == True]
    elif organic_option == "Conventional Only":
        filtered_df = filtered_df[filtered_df["organic"] == False]
        
    filtered_df = filtered_df[(filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])]
    
    # Display filtered products
    st.subheader("Available Fruits")
    
    if filtered_df.empty:
        st.warning("No fruits match your filter criteria.")
    else:
        # Create 3-column layout for product display
        cols = st.columns(3)
        
        # Iterate through filtered fruits and display in grid
        for i, (_, fruit) in enumerate(filtered_df.iterrows()):
            with cols[i % 3]:  # Distribute items across 3 columns
                st.subheader(fruit["name"])
                st.write(f"**Category:** {fruit['category']}")
                st.write(f"**Price:** ${fruit['price']:.2f}")
                st.write(f"**{'🌱 Organic' if fruit['organic'] else 'Conventional'}**")
                
                # Quantity selector with stock limit
                if fruit["stock"] > 0:
                    quantity = st.number_input(f"Quantity for {fruit['name']}", 
                                              min_value=0, 
                                              max_value=fruit["stock"], 
                                              key=f"qty_{fruit['name']}")
                else:
                    st.error("Out of stock")
                    quantity = 0
                
                st.write("---")  # Separator between products
    
    # Shopping cart implementation in sidebar
    st.sidebar.header("Your Cart 🛒")
    
    # Calculate cart contents and total
    cart_items = {}
    cart_total = 0
    
    # Add items with quantity > 0 to cart
    for _, fruit in filtered_df.iterrows():
        quantity = st.session_state.get(f"qty_{fruit['name']}", 0)
        if quantity > 0:
            item_total = quantity * fruit["price"]
            cart_items[fruit["name"]] = {"quantity": quantity, "price": fruit["price"], "total": item_total}
            cart_total += item_total
    
    # Display cart contents and checkout options
    if cart_items:
        # List all items in cart with prices
        for item, details in cart_items.items():
            st.sidebar.write(f"{item}: {details['quantity']} x ${details['price']:.2f} = ${details['total']:.2f}")
        
        st.sidebar.write("---")
        st.sidebar.write(f"**Subtotal:** ${cart_total:.2f}")
        
        # Discount code functionality
        discount = 0.0  # Initialize discount variable
        discount_code = st.sidebar.text_input("Discount Code")
        if discount_code:
            discount = apply_discount(discount_code, cart_total)
            if discount > 0:
                st.sidebar.success(f"Discount applied: ${discount:.2f}")
                cart_total -= discount
        
        st.sidebar.write(f"**Total:** ${cart_total:.2f}")
        
        # Create two columns for checkout and receipt buttons
        col1, col2 = st.sidebar.columns(2)
        
        # Checkout button in first column
        if col1.button("Checkout"):
            st.sidebar.success("Order placed successfully! Thank you for shopping with us.")
            # Placeholder for order processing logic
        
        # Print receipt button in second column
        if col2.button("Print Receipt"):
            receipt = generate_receipt(cart_items, cart_total + discount, discount, cart_total)
            
            # Display receipt in a new section
            with st.expander("Receipt", expanded=True):
                # Add download button for receipt
                st.download_button(
                    label="Download Receipt",
                    data=receipt,
                    file_name=f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                # Display receipt in monospace font
                st.text(receipt)
    else:
        st.sidebar.write("Your cart is empty.")

# Inventory management page with admin access
def show_inventory_page(fruits_df):
    st.title("Fruit Inventory Management")
    
    # Simple password protection for admin area
    password = st.text_input("Enter admin password", type="password")
    if password != "admin123":  # Hard-coded password for demo purposes
        st.error("Please enter the correct password to access inventory management.")
        return
    
    st.success("Admin access granted!")
    
    # Inventory display with sorting options
    st.subheader("Current Inventory")
    
    # Sorting controls
    sort_by = st.selectbox("Sort by", ["name", "price", "stock", "category"])
    sort_order = st.radio("Sort order", ["Ascending", "Descending"])
    
    # Apply sorting to dataframe
    sorted_df = fruits_df.sort_values(
        by=sort_by, 
        ascending=(sort_order == "Ascending")
    )
    
    # Display sortable inventory table
    st.dataframe(sorted_df)
    
    # Form to add new fruits to inventory
    st.subheader("Add New Fruit")
    
    # Two-column layout for form
    col1, col2 = st.columns(2)
    
    # Form fields in first column
    with col1:
        new_name = st.text_input("Fruit Name")
        new_price = st.number_input("Price ($)", min_value=0.01, step=0.01)
        new_stock = st.number_input("Stock Quantity", min_value=0, step=1)
    
    # Form fields in second column
    with col2:
        new_category = st.selectbox("Category", sorted(fruits_df["category"].unique().tolist()))
        new_organic = st.checkbox("Organic")
    
    # Form submission and validation
    if st.button("Add Fruit"):
        if new_name and new_price > 0:
            # Placeholder for database update logic
            st.success(f"Added {new_name} to inventory!")
        else:
            st.error("Please fill in all required fields.")

# Analytics page with charts and statistics
def show_analytics_page(fruits_df):
    st.title("Fruit Store Analytics")
    
    # Key metrics display
    st.subheader("Summary Statistics")
    
    # Three-column layout for metrics
    col1, col2, col3 = st.columns(3)
    
    # Display key metrics in columns
    with col1:
        st.metric("Total Fruits", len(fruits_df))
    
    with col2:
        st.metric("Average Price", f"${fruits_df['price'].mean():.2f}")
    
    with col3:
        st.metric("Total Inventory Value", f"${calculate_total(fruits_df):.2f}")
    
    # Price distribution chart
    st.subheader("Price Distribution")
    st.bar_chart(fruits_df["price"].value_counts().sort_index())
    
    # Two-column layout for additional charts
    col1, col2 = st.columns(2)
    
    # Stock by category chart
    with col1:
        st.subheader("Stock by Category")
        category_data = fruits_df.groupby("category")["stock"].sum().reset_index()
        st.bar_chart(category_data.set_index("category"))
    
    # Organic vs conventional chart
    with col2:
        st.subheader("Organic vs. Conventional")
        organic_counts = fruits_df["organic"].value_counts().rename(index={True: "Organic", False: "Conventional"})
        st.bar_chart(organic_counts)
    
    # Average price by category chart
    st.subheader("Price Comparison by Category")
    category_price = fruits_df.groupby("category")["price"].mean().sort_values()
    st.bar_chart(category_price)

# Application entry point
if __name__ == "__main__":
    main()
