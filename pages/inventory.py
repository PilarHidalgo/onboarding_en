import streamlit as st
import pandas as pd
import os
from utils.data_handler import load_fruit_data, save_fruit_data
from utils.visualization import create_inventory_chart

# Page configuration
st.set_page_config(
    page_title="Inventory Management | Fresh Fruits Store",
    page_icon="🍎",
    layout="wide"
)

# Display logo
with open("assets/logo.txt", "r") as f:
    logo = f.read()
st.sidebar.text(logo)

# Page title
st.title("🍏 Inventory Management")
st.markdown("Manage your fruit inventory, add new items, update quantities, and more.")

# Load data
fruits_df = load_fruit_data()

# Create tabs for different inventory operations
tab1, tab2, tab3 = st.tabs(["View Inventory", "Add New Fruit", "Update Stock"])

# Tab 1: View Inventory
with tab1:
    st.subheader("Current Inventory")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            options=["Name (A-Z)", "Name (Z-A)", "Price (Low to High)", "Price (High to Low)", 
                     "Quantity (Low to High)", "Quantity (High to Low)"]
        )
    
    with col2:
        search_term = st.text_input("Search fruits", placeholder="Enter fruit name...")
    
    # Apply filters
    filtered_df = fruits_df.copy()
    
    if search_term:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False)]
    
    # Apply sorting
    if sort_by == "Name (A-Z)":
        filtered_df = filtered_df.sort_values('name')
    elif sort_by == "Name (Z-A)":
        filtered_df = filtered_df.sort_values('name', ascending=False)
    elif sort_by == "Price (Low to High)":
        filtered_df = filtered_df.sort_values('price')
    elif sort_by == "Price (High to Low)":
        filtered_df = filtered_df.sort_values('price', ascending=False)
    elif sort_by == "Quantity (Low to High)":
        filtered_df = filtered_df.sort_values('quantity')
    elif sort_by == "Quantity (High to Low)":
        filtered_df = filtered_df.sort_values('quantity', ascending=False)
    
    # Display inventory
    if filtered_df.empty:
        st.info("No fruits match your search criteria.")
    else:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Display inventory chart
        st.subheader("Inventory Visualization")
        inventory_chart = create_inventory_chart(filtered_df)
        st.plotly_chart(inventory_chart, use_container_width=True)
        
        # Summary statistics
        st.subheader("Inventory Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Varieties", len(filtered_df))
        
        with col2:
            st.metric("Total Stock", filtered_df['quantity'].sum())
        
        with col3:
            total_value = (filtered_df['price'] * filtered_df['quantity']).sum()
            st.metric("Total Value", f"${total_value:.2f}")

# Tab 2: Add New Fruit
with tab2:
    st.subheader("Add New Fruit to Inventory")
    
    with st.form("add_fruit_form_detailed"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_fruit_name = st.text_input("Fruit Name*")
            new_fruit_price = st.number_input("Price ($)*", min_value=0.01, step=0.01, format="%.2f")
            new_fruit_quantity = st.number_input("Initial Quantity*", min_value=1, step=1)
        
        with col2:
            new_fruit_category = st.selectbox(
                "Category",
                options=["Berries", "Citrus", "Tropical", "Stone Fruits", "Melons", "Other"]
            )
            new_fruit_origin = st.text_input("Country of Origin")
            new_fruit_organic = st.checkbox("Organic")
        
        new_fruit_description = st.text_area("Description", placeholder="Enter details about the fruit...")
        
        submitted = st.form_submit_button("Add to Inventory")
        
        if submitted:
            if not new_fruit_name:
                st.error("Fruit name is required!")
            else:
                # Create new fruit entry
                new_fruit = {
                    'name': new_fruit_name,
                    'price': new_fruit_price,
                    'quantity': new_fruit_quantity,
                    'category': new_fruit_category,
                    'origin': new_fruit_origin,
                    'organic': new_fruit_organic,
                    'description': new_fruit_description
                }
                
                # Add to dataframe
                fruits_df = pd.concat([fruits_df, pd.DataFrame([new_fruit])], ignore_index=True)
                
                # Save updated data
                save_fruit_data(fruits_df)
                
                st.success(f"Added {new_fruit_name} to inventory!")
                st.balloons()

# Tab 3: Update Stock
with tab3:
    st.subheader("Update Existing Stock")
    
    # Select fruit to update
    fruit_to_update = st.selectbox(
        "Select fruit to update",
        options=fruits_df['name'].tolist(),
        index=None,
        placeholder="Choose a fruit..."
    )
    
    if fruit_to_update:
        # Get current fruit data
        fruit_data = fruits_df[fruits_df['name'] == fruit_to_update].iloc[0]
        
        st.info(f"Current stock of {fruit_to_update}: {fruit_data['quantity']} units at ${fruit_data['price']:.2f} each")
        
        # Update options
        update_option = st.radio(
            "What would you like to update?",
            options=["Add to stock", "Remove from stock", "Adjust price", "Remove fruit entirely"]
        )
        
        if update_option == "Add to stock":
            quantity_to_add = st.number_input("Quantity to add", min_value=1, step=1)
            
            if st.button("Update Stock"):
                # Update quantity
                fruits_df.loc[fruits_df['name'] == fruit_to_update, 'quantity'] += quantity_to_add
                
                # Save updated data
                save_fruit_data(fruits_df)
                
                st.success(f"Added {quantity_to_add} units to {fruit_to_update} stock!")
                
        elif update_option == "Remove from stock":
            current_quantity = fruit_data['quantity']
            quantity_to_remove = st.number_input("Quantity to remove", min_value=1, max_value=current_quantity, step=1)
            
            if st.button("Update Stock"):
                # Update quantity
                fruits_df.loc[fruits_df['name'] == fruit_to_update, 'quantity'] -= quantity_to_remove
                
                # Save updated data
                save_fruit_data(fruits_df)
                
                st.success(f"Removed {quantity_to_remove} units from {fruit_to_update} stock!")
                
        elif update_option == "Adjust price":
            new_price = st.number_input("New price ($)", min_value=0.01, value=float(fruit_data['price']), step=0.01, format="%.2f")
            
            if st.button("Update Price"):
                # Update price
                fruits_df.loc[fruits_df['name'] == fruit_to_update, 'price'] = new_price
                
                # Save updated data
                save_fruit_data(fruits_df)
                
                st.success(f"Updated {fruit_to_update} price to ${new_price:.2f}!")
                
        elif update_option == "Remove fruit entirely":
            st.warning(f"Are you sure you want to remove {fruit_to_update} from inventory? This action cannot be undone.")
            
            if st.button("Remove Permanently"):
                # Remove fruit
                fruits_df = fruits_df[fruits_df['name'] != fruit_to_update]
                
                # Save updated data
                save_fruit_data(fruits_df)
                
                st.success(f"Removed {fruit_to_update} from inventory!")
                st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("© 2023 Fresh Fruits Store | Inventory Management v1.0")