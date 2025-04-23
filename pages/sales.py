import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils.data_handler import load_fruit_data, save_fruit_data, load_sales_data, save_sales_data
from utils.visualization import create_sales_chart, create_sales_by_fruit_chart

# Page configuration
st.set_page_config(
    page_title="Sales Management | Fresh Fruits Store",
    page_icon="🍎",
    layout="wide"
)

# Display logo
with open("assets/logo.txt", "r") as f:
    logo = f.read()
st.sidebar.text(logo)

# Page title
st.title("💰 Sales Management")
st.markdown("Record sales, view transaction history, and manage revenue.")

# Load data
fruits_df = load_fruit_data()
sales_df = load_sales_data()

# Create tabs for different sales operations
tab1, tab2, tab3 = st.tabs(["Record Sale", "Sales History", "Revenue Analysis"])

# Tab 1: Record Sale
with tab1:
    st.subheader("Record New Sale")
    
    # Create a form for recording sales
    with st.form("record_sale_form"):
        # Date and customer info
        col1, col2 = st.columns(2)
        
        with col1:
            sale_date = st.date_input("Sale Date", value=datetime.date.today())
            customer_name = st.text_input("Customer Name (optional)")
        
        with col2:
            payment_method = st.selectbox(
                "Payment Method",
                options=["Cash", "Credit Card", "Debit Card", "Mobile Payment", "Other"]
            )
            receipt_number = st.text_input("Receipt Number (optional)")
        
        # Create a container for adding items to the sale
        st.subheader("Sale Items")
        
        # Initialize session state for sale items if not exists
        if 'sale_items' not in st.session_state:
            st.session_state.sale_items = []
        
        # Display current sale items
        if st.session_state.sale_items:
            sale_items_df = pd.DataFrame(st.session_state.sale_items)
            st.dataframe(sale_items_df, use_container_width=True, hide_index=True)
            
            total_amount = sum(item['total'] for item in st.session_state.sale_items)
            st.subheader(f"Total Sale Amount: ${total_amount:.2f}")
        else:
            st.info("No items added to this sale yet.")
        
        # Add item section
        st.markdown("---")
        st.markdown("#### Add Item to Sale")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            available_fruits = fruits_df[fruits_df['quantity'] > 0]['name'].tolist()
            selected_fruit = st.selectbox("Select Fruit", options=available_fruits, key="fruit_select")
        
        with col2:
            if selected_fruit:
                fruit_data = fruits_df[fruits_df['name'] == selected_fruit].iloc[0]
                max_quantity = int(fruit_data['quantity'])
                unit_price = float(fruit_data['price'])
                
                st.write(f"Available: {max_quantity} units")
                st.write(f"Unit Price: ${unit_price:.2f}")
                
                quantity = st.number_input("Quantity", min_value=1, max_value=max_quantity, value=1, step=1, key="quantity_input")
            else:
                quantity = st.number_input("Quantity", min_value=1, value=1, step=1, disabled=True)
        
        with col3:
            if selected_fruit:
                total_price = quantity * unit_price
                st.write(f"Total Price: ${total_price:.2f}")
                
                if st.button("Add to Sale"):
                    # Add item to session state
                    st.session_state.sale_items.append({
                        'fruit': selected_fruit,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total': total_price
                    })
                    st.experimental_rerun()
        
        # Clear items button
        if st.session_state.sale_items and st.button("Clear All Items"):
            st.session_state.sale_items = []
            st.experimental_rerun()
        
        # Submit sale button
        submitted = st.form_submit_button("Complete Sale")
        
        if submitted:
            if not st.session_state.sale_items:
                st.error("Cannot complete sale with no items!")
            else:
                # Create sale record
                sale_id = f"SALE-{len(sales_df) + 1:04d}"
                sale_timestamp = datetime.datetime.combine(sale_date, datetime.datetime.now().time())
                total_amount = sum(item['total'] for item in st.session_state.sale_items)
                
                # Add sale to sales dataframe
                new_sale = {
                    'sale_id': sale_id,
                    'date': sale_timestamp,
                    'customer': customer_name if customer_name else "Walk-in Customer",
                    'payment_method': payment_method,
                    'receipt_number': receipt_number if receipt_number else "N/A",
                    'items': st.session_state.sale_items,
                    'total_amount': total_amount
                }
                
                sales_df = pd.concat([sales_df, pd.DataFrame([new_sale])], ignore_index=True)
                
                # Update inventory
                for item in st.session_state.sale_items:
                    fruit_name = item['fruit']
                    sold_quantity = item['quantity']
                    
                    # Reduce quantity in inventory
                    fruits_df.loc[fruits_df['name'] == fruit_name, 'quantity'] -= sold_quantity
                
                # Save updated data
                save_sales_data(sales_df)
                save_fruit_data(fruits_df)
                
                # Clear session state
                st.session_state.sale_items = []
                
                # Show success message
                st.success(f"Sale {sale_id} completed successfully! Total: ${total_amount:.2f}")
                st.balloons()

# Tab 2: Sales History
with tab2:
    st.subheader("Sales History")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()),
            max_value=datetime.date.today()
        )
    
    with col2:
        payment_filter = st.multiselect(
            "Payment Method",
            options=["All"] + sorted(sales_df['payment_method'].unique().tolist() if not sales_df.empty else ["Cash", "Credit Card", "Debit Card", "Mobile Payment", "Other"]),
            default=["All"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            options=["Most Recent", "Oldest First", "Highest Amount", "Lowest Amount"]
        )
    
    # Apply filters
    if not sales_df.empty:
        filtered_sales = sales_df.copy()
        
        # Date filter
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_sales = filtered_sales[
                (pd.to_datetime(filtered_sales['date']).dt.date >= start_date) & 
                (pd.to_datetime(filtered_sales['date']).dt.date <= end_date)
            ]
        
        # Payment method filter
        if "All" not in payment_filter and payment_filter:
            filtered_sales = filtered_sales[filtered_sales['payment_method'].isin(payment_filter)]
        
        # Apply sorting
        if sort_by == "Most Recent":
            filtered_sales = filtered_sales.sort_values('date', ascending=False)
        elif sort_by == "Oldest First":
            filtered_sales = filtered_sales.sort_values('date')
        elif sort_by == "Highest Amount":
            filtered_sales = filtered_sales.sort_values('total_amount', ascending=False)
        elif sort_by == "Lowest Amount":
            filtered_sales = filtered_sales.sort_values('total_amount')
        
        # Display sales
        if filtered_sales.empty:
            st.info("No sales match your filter criteria.")
        else:
            # Display summary metrics
            total_sales = len(filtered_sales)
            total_revenue = filtered_sales['total_amount'].sum()
            avg_sale = filtered_sales['total_amount'].mean()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Sales", total_sales)
            col2.metric("Total Revenue", f"${total_revenue:.2f}")
            col3.metric("Average Sale", f"${avg_sale:.2f}")
            
            # Display sales table
            display_df = filtered_sales[['sale_id', 'date', 'customer', 'payment_method', 'total_amount']].copy()
            display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d %H:%M')
            display_df['total_amount'] = display_df['total_amount'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Sale details expander
            st.subheader("Sale Details")
            sale_id_to_view = st.selectbox("Select Sale ID to View Details", options=filtered_sales['sale_id'].tolist())
            
            if sale_id_to_view:
                sale_details = filtered_sales[filtered_sales['sale_id'] == sale_id_to_view].iloc[0]
                
                st.markdown(f"**Sale ID:** {sale_details['sale_id']}")
                st.markdown(f"**Date:** {pd.to_datetime(sale_details['date']).strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**Customer:** {sale_details['customer']}")
                st.markdown(f"**Payment Method:** {sale_details['payment_method']}")
                st.markdown(f"**Receipt Number:** {sale_details['receipt_number']}")
                st.markdown(f"**Total Amount:** ${sale_details['total_amount']:.2f}")
                
                st.markdown("#### Items Purchased")
                items_df = pd.DataFrame(sale_details['items'])
                items_df['unit_price'] = items_df['unit_price'].apply(lambda x: f"${x:.2f}")
                items_df['total'] = items_df['total'].apply(lambda x: f"${x:.2f}")
                st.dataframe(items_df, use_container_width=True, hide_index=True)
    else:
        st.info("No sales records available.")

# Tab 3: Revenue Analysis
with tab3:
    st.subheader("Revenue Analysis")
    
    if not sales_df.empty:
        # Time period selection
        time_period = st.radio(
            "Select Time Period",
            options=["Daily", "Weekly", "Monthly", "Yearly"],
            horizontal=True
        )
        
        # Create sales chart
        sales_chart = create_sales_chart(sales_df, time_period)
        st.plotly_chart(sales_chart, use_container_width=True)
        
        # Sales by fruit
        st.subheader("Sales by Fruit")
        
        # Extract all items from all sales
        all_items = []
        for _, sale in sales_df.iterrows():
            for item in sale['items']:
                item_with_date = item.copy()
                item_with_date['date'] = sale['date']
                all_items.append(item_with_date)
        
        if all_items:
            items_df = pd.DataFrame(all_items)
            
            # Create sales by fruit chart
            fruit_chart = create_sales_by_fruit_chart(items_df)
            st.plotly_chart(fruit_chart, use_container_width=True)
            
            # Top selling fruits
            st.subheader("Top Selling Fruits")
            
            fruit_sales = items_df.groupby('fruit').agg({
                'quantity': 'sum',
                'total': 'sum'
            }).reset_index()
            
            fruit_sales = fruit_sales.sort_values('total', ascending=False)
            fruit_sales['total'] = fruit_sales['total'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(fruit_sales, use_container_width=True, hide_index=True)
        else:
            st.info("No sales item data available.")
    else:
        st.info("No sales records available for analysis.")

# Footer
st.markdown("---")
st.markdown("© 2023 Fresh Fruits Store | Sales Management v1.0")