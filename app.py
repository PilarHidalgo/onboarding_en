import streamlit as st
import pandas as pd
import os
from utils.data_handler import load_fruit_data, save_fruit_data
from utils.visualization import create_price_chart

# Page configuration
st.set_page_config(
    page_title="Fresh Fruits Store",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display logo
with open("assets/logo.txt", "r") as f:
    logo = f.read()
st.sidebar.text(logo)

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.info(
    "Select a page above or use the main dashboard below."
)

# Main page content
st.title("🍎 Fresh Fruits Store Dashboard")
st.markdown("""
Welcome to the Fresh Fruits Store management system. Use this dashboard to:
- View and manage your fruit inventory
- Track sales and revenue
- Analyze sales trends and popular items
""")

# Load data
fruits_df = load_fruit_data()

# Display summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Fruit Varieties",
        value=len(fruits_df),
        delta=None
    )

with col2:
    total_stock = fruits_df['quantity'].sum()
    st.metric(
        label="Total Stock",
        value=f"{total_stock} units",
        delta=None
    )

with col3:
    total_value = (fruits_df['price'] * fruits_df['quantity']).sum()
    st.metric(
        label="Inventory Value",
        value=f"${total_value:.2f}",
        delta=None
    )

# Quick add fruit form
st.subheader("Quick Add Fruit")
with st.form("add_fruit_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_fruit_name = st.text_input("Fruit Name")
    
    with col2:
        new_fruit_price = st.number_input("Price ($)", min_value=0.01, step=0.01, format="%.2f")
    
    with col3:
        new_fruit_quantity = st.number_input("Quantity", min_value=1, step=1)
    
    new_fruit_description = st.text_area("Description", height=100)
    
    submitted = st.form_submit_button("Add Fruit")
    
    if submitted:
        if new_fruit_name:
            # Create new fruit entry
            new_fruit = {
                'name': new_fruit_name,
                'price': new_fruit_price,
                'quantity': new_fruit_quantity,
                'description': new_fruit_description
            }
            
            # Add to dataframe
            fruits_df = pd.concat([fruits_df, pd.DataFrame([new_fruit])], ignore_index=True)
            
            # Save updated data
            save_fruit_data(fruits_df)
            
            st.success(f"Added {new_fruit_name} to inventory!")
            st.experimental_rerun()
        else:
            st.error("Fruit name is required!")

# Display inventory preview
st.subheader("Inventory Preview")
st.dataframe(
    fruits_df[['name', 'price', 'quantity']].sort_values('quantity', ascending=False),
    use_container_width=True,
    hide_index=True
)

# Display price chart
st.subheader("Price Distribution")
price_chart = create_price_chart(fruits_df)
st.plotly_chart(price_chart, use_container_width=True)

# Low stock alerts
st.subheader("Low Stock Alerts")
low_stock = fruits_df[fruits_df['quantity'] < 10].sort_values('quantity')

if not low_stock.empty:
    st.warning("The following fruits are running low on stock:")
    for _, fruit in low_stock.iterrows():
        st.info(f"🔸 {fruit['name']}: Only {fruit['quantity']} units left")
else:
    st.success("All fruits are well-stocked!")

# Footer
st.markdown("---")
st.markdown("© 2023 Fresh Fruits Store | Dashboard v1.0")