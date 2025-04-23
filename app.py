import streamlit as st
import pandas as pd
import os
from utils.helpers import calculate_total, apply_discount

# Page configuration
st.set_page_config(
    page_title="Fresh Fruits Market",
    page_icon="🍎",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/fruits.csv")
    except FileNotFoundError:
        # Create default data if file doesn't exist
        default_data = {
            'name': ['Apple', 'Banana', 'Orange', 'Strawberry', 'Mango', 'Pineapple', 'Grapes', 'Watermelon'],
            'price': [1.2, 0.5, 0.8, 2.5, 2.0, 3.0, 4.0, 5.0],
            'stock': [100, 150, 80, 50, 30, 20, 60, 15],
            'category': ['Core Fruits', 'Tropical', 'Citrus', 'Berries', 'Tropical', 'Tropical', 'Berries', 'Melon'],
            'organic': [True, False, True, True, False, False, True, False]
        }
        return pd.DataFrame(default_data)

# Main function
def main():
    # Sidebar
    st.sidebar.title("Fresh Fruits Market 🍎🍌🍊")
    
    # Navigation
    page = st.sidebar.radio("Navigation", ["Home", "Shop", "Inventory", "Analytics"])
    
    # Load data
    fruits_df = load_data()
    
    if page == "Home":
        show_home_page()
    elif page == "Shop":
        show_shop_page(fruits_df)
    elif page == "Inventory":
        show_inventory_page(fruits_df)
    elif page == "Analytics":
        show_analytics_page(fruits_df)

def show_home_page():
    st.title("Welcome to Fresh Fruits Market! 🍓🥭🍍")
    
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
    
    st.info("Visit our Shop page to browse our selection of fresh fruits!")

def show_shop_page(fruits_df):
    st.title("Shop Fresh Fruits 🛒")
    
    # Filter options
    st.sidebar.header("Filter Options")
    
    # Category filter
    categories = ["All"] + sorted(fruits_df["category"].unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    # Organic filter
    organic_option = st.sidebar.radio("Type", ["All", "Organic Only", "Conventional Only"])
    
    # Price range filter
    min_price = float(fruits_df["price"].min())
    max_price = float(fruits_df["price"].max())
    price_range = st.sidebar.slider("Price Range ($)", min_price, max_price, (min_price, max_price))
    
    # Apply filters
    filtered_df = fruits_df.copy()
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
        
    if organic_option == "Organic Only":
        filtered_df = filtered_df[filtered_df["organic"] == True]
    elif organic_option == "Conventional Only":
        filtered_df = filtered_df[filtered_df["organic"] == False]
        
    filtered_df = filtered_df[(filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])]
    
    # Display products
    st.subheader("Available Fruits")
    
    if filtered_df.empty:
        st.warning("No fruits match your filter criteria.")
    else:
        # Create columns for the fruit display
        cols = st.columns(3)
        
        for i, (_, fruit) in enumerate(filtered_df.iterrows()):
            with cols[i % 3]:
                st.subheader(fruit["name"])
                st.write(f"**Category:** {fruit['category']}")
                st.write(f"**Price:** ${fruit['price']:.2f}")
                st.write(f"**{'🌱 Organic' if fruit['organic'] else 'Conventional'}**")
                
                # Only allow adding to cart if in stock
                if fruit["stock"] > 0:
                    quantity = st.number_input(f"Quantity for {fruit['name']}", 
                                              min_value=0, 
                                              max_value=fruit["stock"], 
                                              key=f"qty_{fruit['name']}")
                else:
                    st.error("Out of stock")
                    quantity = 0
                
                st.write("---")
    
    # Shopping cart
    st.sidebar.header("Your Cart 🛒")
    
    cart_items = {}
    cart_total = 0
    
    for _, fruit in filtered_df.iterrows():
        quantity = st.session_state.get(f"qty_{fruit['name']}", 0)
        if quantity > 0:
            item_total = quantity * fruit["price"]
            cart_items[fruit["name"]] = {"quantity": quantity, "price": fruit["price"], "total": item_total}
            cart_total += item_total
    
    if cart_items:
        for item, details in cart_items.items():
            st.sidebar.write(f"{item}: {details['quantity']} x ${details['price']:.2f} = ${details['total']:.2f}")
        
        st.sidebar.write("---")
        st.sidebar.write(f"**Subtotal:** ${cart_total:.2f}")
        
        # Apply discount
        discount_code = st.sidebar.text_input("Discount Code")
        if discount_code:
            discount = apply_discount(discount_code, cart_total)
            if discount > 0:
                st.sidebar.success(f"Discount applied: ${discount:.2f}")
                cart_total -= discount
        
        st.sidebar.write(f"**Total:** ${cart_total:.2f}")
        
        if st.sidebar.button("Checkout"):
            st.sidebar.success("Order placed successfully! Thank you for shopping with us.")
            # In a real app, you would process the order here
    else:
        st.sidebar.write("Your cart is empty.")

def show_inventory_page(fruits_df):
    st.title("Fruit Inventory Management")
    
    # Admin password check (simple implementation for demo)
    password = st.text_input("Enter admin password", type="password")
    if password != "admin123":
        st.error("Please enter the correct password to access inventory management.")
        return
    
    st.success("Admin access granted!")
    
    # Display current inventory
    st.subheader("Current Inventory")
    
    # Add sorting and filtering options
    sort_by = st.selectbox("Sort by", ["name", "price", "stock", "category"])
    sort_order = st.radio("Sort order", ["Ascending", "Descending"])
    
    sorted_df = fruits_df.sort_values(
        by=sort_by, 
        ascending=(sort_order == "Ascending")
    )
    
    # Display the inventory table with editable cells
    st.dataframe(sorted_df)
    
    # Add new fruit form
    st.subheader("Add New Fruit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("Fruit Name")
        new_price = st.number_input("Price ($)", min_value=0.01, step=0.01)
        new_stock = st.number_input("Stock Quantity", min_value=0, step=1)
    
    with col2:
        new_category = st.selectbox("Category", sorted(fruits_df["category"].unique().tolist()))
        new_organic = st.checkbox("Organic")
    
    if st.button("Add Fruit"):
        if new_name and new_price > 0:
            # In a real app, you would save this to the CSV file
            st.success(f"Added {new_name} to inventory!")
        else:
            st.error("Please fill in all required fields.")

def show_analytics_page(fruits_df):
    st.title("Fruit Store Analytics")
    
    # Summary statistics
    st.subheader("Summary Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Fruits", len(fruits_df))
    
    with col2:
        st.metric("Average Price", f"${fruits_df['price'].mean():.2f}")
    
    with col3:
        st.metric("Total Inventory Value", f"${calculate_total(fruits_df):.2f}")
    
    # Charts
    st.subheader("Price Distribution")
    
    # Using Streamlit's native chart instead of matplotlib
    st.bar_chart(fruits_df["price"].value_counts().sort_index())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stock by Category")
        category_data = fruits_df.groupby("category")["stock"].sum().reset_index()
        st.bar_chart(category_data.set_index("category"))
    
    with col2:
        st.subheader("Organic vs. Conventional")
        organic_counts = fruits_df["organic"].value_counts().rename(index={True: "Organic", False: "Conventional"})
        st.bar_chart(organic_counts)
    
    # Price comparison
    st.subheader("Price Comparison by Category")
    category_price = fruits_df.groupby("category")["price"].mean().sort_values()
    st.bar_chart(category_price)

if __name__ == "__main__":
    main()
