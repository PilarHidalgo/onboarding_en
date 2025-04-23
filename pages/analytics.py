import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_handler import load_fruit_data, load_sales_data
from utils.visualization import create_sales_trend_chart, create_inventory_value_chart, create_sales_heatmap

# Page configuration
st.set_page_config(
    page_title="Analytics Dashboard | Fresh Fruits Store",
    page_icon="🍎",
    layout="wide"
)

# Display logo
with open("assets/logo.txt", "r") as f:
    logo = f.read()
st.sidebar.text(logo)

# Page title
st.title("📊 Analytics Dashboard")
st.markdown("Analyze sales trends, inventory metrics, and business performance.")

# Load data
fruits_df = load_fruit_data()
sales_df = load_sales_data()

# Date range selector for filtering data
st.sidebar.header("Filter Data")
default_start_date = datetime.now() - timedelta(days=90)
default_end_date = datetime.now()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(default_start_date.date(), default_end_date.date()),
    max_value=datetime.now().date()
)

# Apply date filter to sales data if available
filtered_sales_df = sales_df.copy() if not sales_df.empty else pd.DataFrame()
if not filtered_sales_df.empty and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_sales_df = filtered_sales_df[
        (pd.to_datetime(filtered_sales_df['date']).dt.date >= start_date) & 
        (pd.to_datetime(filtered_sales_df['date']).dt.date <= end_date)
    ]

# Create tabs for different analytics views
tab1, tab2, tab3, tab4 = st.tabs(["Sales Analytics", "Inventory Analytics", "Customer Insights", "Forecasting"])

# Tab 1: Sales Analytics
with tab1:
    st.header("Sales Performance")
    
    if not filtered_sales_df.empty:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Total revenue
        total_revenue = filtered_sales_df['total_amount'].sum()
        col1.metric(
            label="Total Revenue",
            value=f"${total_revenue:.2f}"
        )
        
        # Number of sales
        num_sales = len(filtered_sales_df)
        col2.metric(
            label="Number of Sales",
            value=num_sales
        )
        
        # Average sale value
        avg_sale = total_revenue / num_sales if num_sales > 0 else 0
        col3.metric(
            label="Average Sale Value",
            value=f"${avg_sale:.2f}"
        )
        
        # Calculate items sold
        total_items_sold = 0
        for _, sale in filtered_sales_df.iterrows():
            for item in sale['items']:
                total_items_sold += item['quantity']
        
        col4.metric(
            label="Total Items Sold",
            value=total_items_sold
        )
        
        # Sales trend chart
        st.subheader("Sales Trend")
        time_period = st.radio(
            "Group by",
            options=["Daily", "Weekly", "Monthly"],
            horizontal=True
        )
        
        sales_trend_chart = create_sales_trend_chart(filtered_sales_df, time_period)
        st.plotly_chart(sales_trend_chart, use_container_width=True)
        
        # Payment method distribution
        st.subheader("Payment Method Distribution")
        
        payment_counts = filtered_sales_df['payment_method'].value_counts().reset_index()
        payment_counts.columns = ['Payment Method', 'Count']
        
        fig = px.pie(
            payment_counts,
            values='Count',
            names='Payment Method',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top selling fruits
        st.subheader("Top Selling Fruits")
        
        # Extract all items from filtered sales
        all_items = []
        for _, sale in filtered_sales_df.iterrows():
            for item in sale['items']:
                all_items.append(item)
        
        if all_items:
            items_df = pd.DataFrame(all_items)
            top_fruits = items_df.groupby('fruit').agg({
                'quantity': 'sum',
                'total': 'sum'
            }).reset_index().sort_values('total', ascending=False)
            
            # Display top 10 fruits
            top_10_fruits = top_fruits.head(10)
            
            fig = px.bar(
                top_10_fruits,
                x='fruit',
                y='total',
                text_auto='.2s',
                labels={'fruit': 'Fruit', 'total': 'Revenue ($)'},
                color='total',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Sales heatmap by day and hour
            st.subheader("Sales Heatmap by Day and Hour")
            sales_heatmap = create_sales_heatmap(filtered_sales_df)
            st.plotly_chart(sales_heatmap, use_container_width=True)
        else:
            st.info("No sales item data available for the selected period.")
    else:
        st.info("No sales data available. Please record some sales first.")

# Tab 2: Inventory Analytics
with tab2:
    st.header("Inventory Analysis")
    
    if not fruits_df.empty:
        # Key metrics
        col1, col2, col3 = st.columns(3)
        
        # Total inventory value
        total_value = (fruits_df['price'] * fruits_df['quantity']).sum()
        col1.metric(
            label="Total Inventory Value",
            value=f"${total_value:.2f}"
        )
        
        # Average price
        avg_price = fruits_df['price'].mean()
        col2.metric(
            label="Average Price",
            value=f"${avg_price:.2f}"
        )
        
        # Total stock
        total_stock = fruits_df['quantity'].sum()
        col3.metric(
            label="Total Stock",
            value=total_stock
        )
        
        # Inventory value chart
        st.subheader("Inventory Value by Fruit")
        inventory_value_chart = create_inventory_value_chart(fruits_df)
        st.plotly_chart(inventory_value_chart, use_container_width=True)
        
        # Stock distribution
        st.subheader("Stock Distribution")
        
        # Create stock level categories
        fruits_df['stock_level'] = pd.cut(
            fruits_df['quantity'],
            bins=[0, 10, 50, 100, float('inf')],
            labels=['Low (0-10)', 'Medium (11-50)', 'High (51-100)', 'Very High (100+)']
        )
        
        stock_counts = fruits_df['stock_level'].value_counts().reset_index()
        stock_counts.columns = ['Stock Level', 'Count']
        
        fig = px.pie(
            stock_counts,
            values='Count',
            names='Stock Level',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Price distribution
        st.subheader("Price Distribution")
        
        fig = px.histogram(
            fruits_df,
            x='price',
            nbins=20,
            labels={'price': 'Price ($)', 'count': 'Number of Fruits'},
            color_discrete_sequence=['#3CB371']
        )
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Low stock alerts
        st.subheader("Low Stock Alerts")
        low_stock = fruits_df[fruits_df['quantity'] < 10].sort_values('quantity')
        
        if not low_stock.empty:
            st.warning(f"{len(low_stock)} fruits are running low on stock!")
            
            fig = px.bar(
                low_stock,
                x='name',
                y='quantity',
                text='quantity',
                labels={'name': 'Fruit', 'quantity': 'Remaining Stock'},
                color='quantity',
                color_continuous_scale=px.colors.sequential.Reds_r
            )
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("All fruits are well-stocked!")
    else:
        st.info("No inventory data available. Please add some fruits to your inventory first.")

# Tab 3: Customer Insights
with tab3:
    st.header("Customer Insights")
    
    if not filtered_sales_df.empty:
        # Extract customer data
        customers = filtered_sales_df[filtered_sales_df['customer'] != "Walk-in Customer"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Number of unique customers
            unique_customers = customers['customer'].nunique()
            st.metric(
                label="Unique Customers",
                value=unique_customers
            )
        
        with col2:
            # Walk-in vs. named customers
            walk_in_count = len(filtered_sales_df[filtered_sales_df['customer'] == "Walk-in Customer"])
            named_count = len(filtered_sales_df) - walk_in_count
            
            st.metric(
                label="Named Customer Percentage",
                value=f"{named_count / len(filtered_sales_df) * 100:.1f}%"
            )
        
        # Customer purchase frequency
        if not customers.empty:
            st.subheader("Top Customers by Purchase Amount")
            
            customer_sales = customers.groupby('customer').agg({
                'sale_id': 'count',
                'total_amount': 'sum'
            }).reset_index()
            
            customer_sales.columns = ['Customer', 'Number of Purchases', 'Total Spent']
            customer_sales = customer_sales.sort_values('Total Spent', ascending=False).head(10)
            
            fig = px.bar(
                customer_sales,
                x='Customer',
                y='Total Spent',
                text_auto='.2s',
                color='Number of Purchases',
                labels={'Total Spent': 'Total Amount Spent ($)'},
                color_continuous_scale=px.colors.sequential.Viridis
            )
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Customer purchase patterns
            st.subheader("Customer Purchase Patterns")
            
            # Extract day of week from sales
            customers['day_of_week'] = pd.to_datetime(customers['date']).dt.day_name()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            day_counts = customers['day_of_week'].value_counts().reindex(day_order).reset_index()
            day_counts.columns = ['Day of Week', 'Number of Purchases']
            
            fig = px.line(
                day_counts,
                x='Day of Week',
                y='Number of Purchases',
                markers=True,
                line_shape='spline',
                labels={'Number of Purchases': 'Number of Customer Purchases'},
                color_discrete_sequence=['#FF6B6B']
            )
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No named customer data available for the selected period.")
    else:
        st.info("No sales data available. Please record some sales first.")

# Tab 4: Forecasting
with tab4:
    st.header("Sales Forecasting")
    
    if not filtered_sales_df.empty and len(filtered_sales_df) > 10:
        # Simple forecasting based on historical data
        st.subheader("Sales Trend and Forecast")
        
        # Prepare daily sales data
        filtered_sales_df['date'] = pd.to_datetime(filtered_sales_df['date'])
        daily_sales = filtered_sales_df.groupby(filtered_sales_df['date'].dt.date)['total_amount'].sum().reset_index()
        daily_sales.columns = ['date', 'sales']
        
        # Calculate moving average
        window_size = st.slider("Moving Average Window (days)", min_value=3, max_value=30, value=7)
        daily_sales['moving_avg'] = daily_sales['sales'].rolling(window=window_size).mean()
        
        # Create forecast for next 14 days
        last_date = daily_sales['date'].max()
        forecast_dates = [last_date + timedelta(days=i+1) for i in range(14)]
        
        # Simple linear regression for forecasting
        if len(daily_sales) > window_size:
            # Use last window_size*2 days for trend calculation
            recent_sales = daily_sales.tail(window_size*2)
            x = np.arange(len(recent_sales))
            y = recent_sales['sales'].values
            
            # Linear regression
            z = np.polyfit(x, y, 1)
            slope = z[0]
            intercept = z[1]
            
            # Create forecast
            forecast_values = [slope * (len(recent_sales) + i) + intercept for i in range(1, 15)]
            forecast_df = pd.DataFrame({
                'date': forecast_dates,
                'forecast': forecast_values
            })
            
            # Combine actual and forecast
            combined_df = pd.concat([
                daily_sales[['date', 'sales', 'moving_avg']],
                forecast_df
            ])
            
            # Create plot
            fig = go.Figure()
            
            # Actual sales
            fig.add_trace(go.Scatter(
                x=daily_sales['date'],
                y=daily_sales['sales'],
                mode='markers',
                name='Actual Sales',
                marker=dict(color='#3366CC', size=8)
            ))
            
            # Moving average
            fig.add_trace(go.Scatter(
                x=daily_sales['date'],
                y=daily_sales['moving_avg'],
                mode='lines',
                name=f'{window_size}-Day Moving Average',
                line=dict(color='#FF9900', width=2)
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast_df['date'],
                y=forecast_df['forecast'],
                mode='lines+markers',
                name='14-Day Forecast',
                line=dict(color='#109618', width=3, dash='dash'),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title='Sales Trend and 14-Day Forecast',
                xaxis_title='Date',
                yaxis_title='Sales Amount ($)',
                height=600,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast summary
            st.subheader("Forecast Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_forecast = np.mean(forecast_values)
                st.metric(
                    label="Average Daily Forecast",
                    value=f"${avg_forecast:.2f}"
                )
            
            with col2:
                total_forecast = np.sum(forecast_values)
                st.metric(
                    label="Total 14-Day Forecast",
                    value=f"${total_forecast:.2f}"
                )
            
            with col3:
                trend_direction = "Upward" if slope > 0 else "Downward"
                trend_percentage = abs(slope) / np.mean(y) * 100
                st.metric(
                    label="Sales Trend",
                    value=trend_direction,
                    delta=f"{trend_percentage:.1f}% per day"
                )
            
            # Seasonal patterns
            if len(daily_sales) >= 30:
                st.subheader("Day of Week Patterns")
                
                # Add day of week
                daily_sales['day_of_week'] = pd.to_datetime(daily_sales['date']).dt.day_name()
                
                # Group by day of week
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_avg = daily_sales.groupby('day_of_week')['sales'].mean().reindex(day_order).reset_index()
                day_avg.columns = ['Day of Week', 'Average Sales']
                
                fig = px.bar(
                    day_avg,
                    x='Day of Week',
                    y='Average Sales',
                    text_auto='.2s',
                    labels={'Average Sales': 'Average Daily Sales ($)'},
                    color='Average Sales',
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Best performing day
                best_day = day_avg.loc[day_avg['Average Sales'].idxmax()]
                st.info(f"💡 **Insight:** {best_day['Day of Week']} is typically your best sales day, with an average of ${best_day['Average Sales']:.2f} in sales.")
        else:
            st.warning("Not enough data for forecasting. Need at least 14 days of sales data.")
    else:
        st.info("Not enough sales data available for forecasting. Please record more sales first.")

# Footer
st.markdown("---")
st.markdown("© 2023 Fresh Fruits Store | Analytics Dashboard v1.0")