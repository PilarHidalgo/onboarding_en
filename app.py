import streamlit as st
import pandas as pd
from database import init_connection
from crud import (
    get_all_fruits,
    get_fruit_by_id,
    add_fruit,
    update_fruit,
    delete_fruit
)

# Page configuration
st.set_page_config(
    page_title="Fruit Store Management",
    page_icon="🍎",
    layout="wide"
)

# Initialize database connection
conn = init_connection()

# Sidebar navigation
st.sidebar.title("Fruit Store Management")
page = st.sidebar.selectbox("Choose an action", ["View Inventory", "Add Fruit", "Update Fruit", "Delete Fruit"])

# Function to display all fruits
def display_fruits():
    st.title("Fruit Inventory 🍎🍌🍇")
    
    # Get all fruits from database
    fruits = get_all_fruits(conn)
    
    if not fruits:
        st.info("No fruits in inventory. Add some fruits!")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(fruits, columns=["ID", "Name", "Price", "Quantity", "Category"])
    
    # Display as table
    st.dataframe(df, use_container_width=True)
    
    # Display some statistics
    st.subheader("Inventory Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fruit Types", len(fruits))
    with col2:
        total_quantity = sum(fruit[3] for fruit in fruits)
        st.metric("Total Quantity", total_quantity)
    with col3:
        total_value = sum(fruit[2] * fruit[3] for fruit in fruits)
        st.metric("Inventory Value", f"${total_value:.2f}")
    
    # Create a bar chart for quantity by fruit
    st.subheader("Quantity by Fruit")
    chart_data = pd.DataFrame({
        'Fruit': [fruit[1] for fruit in fruits],
        'Quantity': [fruit[3] for fruit in fruits]
    })
    st.bar_chart(chart_data.set_index('Fruit'))
    
    # Create a pie chart for category distribution
    st.subheader("Category Distribution")
    category_counts = {}
    for fruit in fruits:
        category = fruit[4]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    
    category_data = pd.DataFrame({
        'Category': list(category_counts.keys()),
        'Count': list(category_counts.values())
    })
    st.pie_chart(category_data.set_index('Category'))

# Function to add a new fruit
def add_new_fruit():
    st.title("Add New Fruit 🍏")
    
    with st.form("add_fruit_form"):
        name = st.text_input("Fruit Name")
        price = st.number_input("Price ($)", min_value=0.01, step=0.01, format="%.2f")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        category = st.selectbox("Category", ["Fresh Fruits", "Dried Fruits", "Exotic Fruits", "Berries", "Citrus", "Other"])
        
        submitted = st.form_submit_button("Add Fruit")
        
        if submitted:
            if name:
                add_fruit(conn, name, price, quantity, category)
                st.success(f"Successfully added {name} to inventory!")
                st.balloons()
            else:
                st.error("Fruit name cannot be empty!")

# Function to update an existing fruit
def update_existing_fruit():
    st.title("Update Fruit 🔄")
    
    # Get all fruits for selection
    fruits = get_all_fruits(conn)
    
    if not fruits:
        st.info("No fruits in inventory to update.")
        return
    
    # Create a selection box with fruit names
    fruit_names = [f"{fruit[0]} - {fruit[1]}" for fruit in fruits]
    selected_fruit = st.selectbox("Select a fruit to update", fruit_names)
    
    # Extract the ID from the selection
    fruit_id = int(selected_fruit.split(" - ")[0])
    
    # Get current fruit data
    fruit_data = get_fruit_by_id(conn, fruit_id)
    
    if fruit_data:
        with st.form("update_fruit_form"):
            name = st.text_input("Fruit Name", value=fruit_data[1])
            price = st.number_input("Price ($)", min_value=0.01, step=0.01, value=float(fruit_data[2]), format="%.2f")
            quantity = st.number_input("Quantity", min_value=0, step=1, value=int(fruit_data[3]))
            category = st.selectbox("Category", 
                                   ["Fresh Fruits", "Dried Fruits", "Exotic Fruits", "Berries", "Citrus", "Other"],
                                   index=["Fresh Fruits", "Dried Fruits", "Exotic Fruits", "Berries", "Citrus", "Other"].index(fruit_data[4]) if fruit_data[4] in ["Fresh Fruits", "Dried Fruits", "Exotic Fruits", "Berries", "Citrus", "Other"] else 5)
            
            submitted = st.form_submit_button("Update Fruit")
            
            if submitted:
                if name:
                    update_fruit(conn, fruit_id, name, price, quantity, category)
                    st.success(f"Successfully updated {name}!")
                else:
                    st.error("Fruit name cannot be empty!")

# Function to delete a fruit
def delete_existing_fruit():
    st.title("Delete Fruit 🗑️")
    
    # Get all fruits for selection
    fruits = get_all_fruits(conn)
    
    if not fruits:
        st.info("No fruits in inventory to delete.")
        return
    
    # Create a selection box with fruit names
    fruit_names = [f"{fruit[0]} - {fruit[1]}" for fruit in fruits]
    selected_fruit = st.selectbox("Select a fruit to delete", fruit_names)
    
    # Extract the ID from the selection
    fruit_id = int(selected_fruit.split(" - ")[0])
    fruit_name = selected_fruit.split(" - ")[1]
    
    # Confirm deletion
    if st.button(f"Delete {fruit_name}", type="primary"):
        delete_fruit(conn, fruit_id)
        st.success(f"Successfully deleted {fruit_name}!")
        st.experimental_rerun()

# Display the selected page
if page == "View Inventory":
    display_fruits()
elif page == "Add Fruit":
    add_new_fruit()
elif page == "Update Fruit":
    update_existing_fruit()
elif page == "Delete Fruit":
    delete_existing_fruit()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Fruit Store Management System v1.0")