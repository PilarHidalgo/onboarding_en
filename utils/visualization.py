import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_inventory_chart(df):
    """
    Create a bar chart visualization of the inventory.
    
    Args:
        df (pandas.DataFrame): DataFrame containing fruit inventory data
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    # Sort by quantity
    sorted_df = df.sort_values('quantity', ascending=False)
    
    # Create color scale based on quantity
    fig = px.bar(
        sorted_df,
        x='name',
        y='quantity',
        color='quantity',
        labels={'name': 'Fruit', 'quantity': 'Stock Quantity'},
        text='quantity',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        title='Current Inventory Levels',
        xaxis_title='Fruit',
        yaxis_title='Quantity',
        xaxis={'categoryorder': 'total descending'},
        height=500
    )
    
    # Add threshold line for low stock
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=10,
        x1=len(sorted_df) - 0.5,
        y1=10,
        line=dict(
            color="Red",
            width=2,
            dash="dash",
        )
    )
    
    # Add annotation for low stock threshold
    fig.add_annotation(
        x=len(sorted_df) - 1,
        y=10,
        text="Low Stock Threshold",
        showarrow=True,
        arrowhead=1,
        ax=50,
        ay=-30,
        font=dict(
            color="Red",
            size=12
        )
    )
    
    return fig

def create_inventory_value_chart(df):
    """
    Create a bar chart visualization of the inventory value.
    
    Args:
        df (pandas.DataFrame): DataFrame containing fruit inventory data
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    # Calculate inventory value
    df_with_value = df.copy()
    df_with_value['inventory_value'] = df_with_value['price'] * df_with_value['quantity']
    
    # Sort by inventory value
    sorted_df = df_with_value.sort_values('inventory_value', ascending=False)
    
    # Create color scale based on inventory value
    fig = px.bar(
        sorted_df,
        x='name',
        y='inventory_value',
        color='inventory_value',
        labels={'name': 'Fruit', 'inventory_value': 'Inventory Value ($)'},
        text_auto='.2s',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        title='Inventory Value by Fruit',
        xaxis_title='Fruit',
        yaxis_title='Value ($)',
        xaxis={'categoryorder': 'total descending'},
        height=500
    )
    
    return fig

def create_sales_chart(sales_df, time_period):
    """
    Create a line chart visualization of sales over time.
    
    Args:
        sales_df (pandas.DataFrame): DataFrame containing sales data
        time_period (str): Time period for grouping ('Daily', 'Weekly', 'Monthly', 'Yearly')
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if sales_df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='No Sales Data Available',
            xaxis_title='Date',
            yaxis_title='Sales ($)',
            height=500
        )
        return fig
    
    # Convert date to datetime if it's not already
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    # Group by time period
    if time_period == 'Daily':
        sales_by_period = sales_df.groupby(sales_df['date'].dt.date)['total_amount'].sum().reset_index()
        date_format = '%Y-%m-%d'
    elif time_period == 'Weekly':
        sales_df['week'] = sales_df['date'].dt.to_period('W').apply(lambda r: r.start_time)
        sales_by_period = sales_df.groupby('week')['total_amount'].sum().reset_index()
        sales_by_period.columns = ['date', 'total_amount']
        date_format = '%Y-%m-%d'
    elif time_period == 'Monthly':
        sales_df['month'] = sales_df['date'].dt.to_period('M').apply(lambda r: r.start_time)
        sales_by_period = sales_df.groupby('month')['total_amount'].sum().reset_index()
        sales_by_period.columns = ['date', 'total_amount']
        date_format = '%Y-%m'
    else:  # Yearly
        sales_df['year'] = sales_df['date'].dt.to_period('Y').apply(lambda r: r.start_time)
        sales_by_period = sales_df.groupby('year')['total_amount'].sum().reset_index()
        sales_by_period.columns = ['date', 'total_amount']
        date_format = '%Y'
    
    # Sort by date
    sales_by_period = sales_by_period.sort_values('date')
    
    # Create figure
    fig = px.line(
        sales_by_period,
        x='date',
        y='total_amount',
        labels={'date': 'Date', 'total_amount': 'Sales Amount ($)'},
        markers=True,
        line_shape='spline'
    )
    
    # Add data points
    fig.add_trace(
        go.Scatter(
            x=sales_by_period['date'],
            y=sales_by_period['total_amount'],
            mode='markers',
            marker=dict(size=8, color='#3366CC'),
            name='Sales'
        )
    )
    
    # Format x-axis dates
    fig.update_xaxes(
        tickformat=date_format
    )
    
    # Format y-axis with dollar signs
    fig.update_yaxes(
        tickprefix='$'
    )
    
    fig.update_layout(
        title=f'{time_period} Sales',
        xaxis_title='Date',
        yaxis_title='Sales Amount ($)',
        height=500,
        showlegend=False
    )
    
    return fig

def create_sales_by_fruit_chart(items_df):
    """
    Create a bar chart visualization of sales by fruit.
    
    Args:
        items_df (pandas.DataFrame): DataFrame containing sales items data
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if items_df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='No Sales Data Available',
            xaxis_title='Fruit',
            yaxis_title='Sales ($)',
            height=500
        )
        return fig
    
    # Group by fruit
    sales_by_fruit = items_df.groupby('fruit').agg({
        'quantity': 'sum',
        'total': 'sum'
    }).reset_index()
    
    # Sort by total sales
    sales_by_fruit = sales_by_fruit.sort_values('total', ascending=False)
    
    # Create figure
    fig = px.bar(
        sales_by_fruit,
        x='fruit',
        y='total',
        color='quantity',
        labels={'fruit': 'Fruit', 'total': 'Sales Amount ($)', 'quantity': 'Units Sold'},
        text_auto='.2s',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        title='Sales by Fruit',
        xaxis_title='Fruit',
        yaxis_title='Sales Amount ($)',
        xaxis={'categoryorder': 'total descending'},
        height=500
    )
    
    return fig

def create_sales_trend_chart(sales_df, time_period):
    """
    Create a line chart visualization of sales trend over time with moving average.
    
    Args:
        sales_df (pandas.DataFrame): DataFrame containing sales data
        time_period (str): Time period for grouping ('Daily', 'Weekly', 'Monthly')
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if sales_df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='No Sales Data Available',
            xaxis_title='Date',
            yaxis_title='Sales ($)',
            height=500
        )
        return fig
    
    # Convert date to datetime if it's not already
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    # Group by time period
    if time_period == 'Daily':
        sales_by_period = sales_df.groupby(sales_df['date'].dt.date)['total_amount'].sum().reset_index()
        window_size = 7  # 7-day moving average
        date_format = '%Y-%m-%d'
    elif time_period == 'Weekly':
        sales_df['week'] = sales_df['date'].dt.to_period('W').apply(lambda r: r.start_time)
        sales_by_period = sales_df.groupby('week')['total_amount'].sum().reset_index()
        sales_by_period.columns = ['date', 'total_amount']
        window_size = 4  # 4-week moving average
        date_format = '%Y-%m-%d'
    else:  # Monthly
        sales_df['month'] = sales_df['date'].dt.to_period('M').apply(lambda r: r.start_time)
        sales_by_period = sales_df.groupby('month')['total_amount'].sum().reset_index()
        sales_by_period.columns = ['date', 'total_amount']
        window_size = 3  # 3-month moving average
        date_format = '%Y-%m'
    
    # Sort by date
    sales_by_period = sales_by_period.sort_values('date')
    
    # Calculate moving average if enough data points
    if len(sales_by_period) >= window_size:
        sales_by_period['moving_avg'] = sales_by_period['total_amount'].rolling(window=window_size).mean()
    
    # Create figure
    fig = go.Figure()
    
    # Add actual sales
    fig.add_trace(
        go.Scatter(
            x=sales_by_period['date'],
            y=sales_by_period['total_amount'],
            mode='lines+markers',
            name='Actual Sales',
            line=dict(color='#3366CC', width=2),
            marker=dict(size=8)
        )
    )
    
    # Add moving average if available
    if 'moving_avg' in sales_by_period.columns:
        fig.add_trace(
            go.Scatter(
                x=sales_by_period['date'],
                y=sales_by_period['moving_avg'],
                mode='lines',
                name=f'{window_size}-Period Moving Average',
                line=dict(color='#FF9900', width=3, dash='dash')
            )
        )
    
    # Format x-axis dates
    fig.update_xaxes(
        tickformat=date_format
    )
    
    # Format y-axis with dollar signs
    fig.update_yaxes(
        tickprefix='$'
    )
    
    fig.update_layout(
        title=f'{time_period} Sales Trend',
        xaxis_title='Date',
        yaxis_title='Sales Amount ($)',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_sales_heatmap(sales_df):
    """
    Create a heatmap visualization of sales by day of week and hour.
    
    Args:
        sales_df (pandas.DataFrame): DataFrame containing sales data
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if sales_df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='No Sales Data Available',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            height=500
        )
        return fig
    
    # Convert date to datetime if it's not already
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    # Extract day of week and hour
    sales_df['day_of_week'] = sales_df['date'].dt.day_name()
    sales_df['hour'] = sales_df['date'].dt.hour
    
    # Group by day of week and hour
    sales_by_day_hour = sales_df.groupby(['day_of_week', 'hour'])['total_amount'].sum().reset_index()
    
    # Create pivot table
    pivot_table = sales_by_day_hour.pivot_table(
        values='total_amount',
        index='day_of_week',
        columns='hour',
        aggfunc='sum'
    ).fillna(0)
    
    # Reorder days of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(day_order)
    
    # Create heatmap
    fig = px.imshow(
        pivot_table,
        labels=dict(x="Hour of Day", y="Day of Week", color="Sales Amount ($)"),
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale='Viridis',
        aspect="auto"
    )
    
    # Add text annotations
    for i, day in enumerate(pivot_table.index):
        for j, hour in enumerate(pivot_table.columns):
            value = pivot_table.iloc[i, j]
            if value > 0:
                fig.add_annotation(
                    x=hour,
                    y=day,
                    text=f"${value:.0f}",
                    showarrow=False,
                    font=dict(
                        color="white" if value > pivot_table.values.max() / 3 else "black",
                        size=9
                    )
                )
    
    fig.update_layout(
        title='Sales Heatmap by Day and Hour',
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        height=500
    )
    
    return fig

def create_category_comparison_chart(df):
    """
    Create a grouped bar chart comparing categories by quantity and value.
    
    Args:
        df (pandas.DataFrame): DataFrame containing fruit inventory data
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='No Inventory Data Available',
            xaxis_title='Category',
            yaxis_title='Value',
            height=500
        )
        return fig
    
    # Calculate inventory value
    df_with_value = df.copy()
    df_with_value['inventory_value'] = df_with_value['price'] * df_with_value['quantity']
    
    # Group by category
    category_data = df_with_value.groupby('category').agg({
        'quantity': 'sum',
        'inventory_value': 'sum',
        'name': 'count'
    }).reset_index()
    
    category_data.columns = ['Category', 'Total Quantity', 'Total Value', 'Number of Varieties']
    
    # Sort by total value
    category_data = category_data.sort_values('Total Value', ascending=False)
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add bars for quantity
    fig.add_trace(
        go.Bar(
            x=category_data['Category'],
            y=category_data['Total Quantity'],
            name='Quantity',
            marker_color='#3366CC',
            text=category_data['Total Quantity'],
            textposition='auto'
        )
    )
    
    # Add bars for value
    fig.add_trace(
        go.Bar(
            x=category_data['Category'],
            y=category_data['Total Value'],
            name='Value ($)',
            marker_color='#FF9900',
            text=category_data['Total Value'].apply(lambda x: f"${x:.2f}"),
            textposition='auto',
            yaxis='y2'
        )
    )
    
    # Add number of varieties as text
    for i, row in enumerate(category_data.itertuples()):
        fig.add_annotation(
            x=row.Category,
            y=row._2 + (row._2 * 0.1),  # Slightly above the quantity bar
            text=f"{row._4} varieties",
            showarrow=False,
            font=dict(size=10)
        )
    
    # Update layout with secondary y-axis
    fig.update_layout(
        title='Category Comparison: Quantity vs. Value',
        xaxis_title='Category',
        yaxis=dict(
            title='Quantity',
            side='left'
        ),
        yaxis2=dict(
            title='Value ($)',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return fig

def create_price_distribution_chart(df):
    """
    Create a histogram visualization of price distribution.
    
    Args:
        df (pandas.DataFrame): DataFrame containing fruit inventory data
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='No Inventory Data Available',
            xaxis_title='Price ($)',
            yaxis_title='Count',
            height=500
        )
        return fig
    
    # Create histogram
    fig = px.histogram(
        df,
        x='price',
        nbins=20,
        labels={'price': 'Price ($)', 'count': 'Number of Fruits'},
        color_discrete_sequence=['#3CB371'],
        marginal='box'  # Add box plot on the margin
    )
    
    # Add average price line
    avg_price = df['price'].mean()
    fig.add_vline(
        x=avg_price,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Avg: ${avg_price:.2f}",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title='Price Distribution',
        xaxis_title='Price ($)',
        yaxis_title='Number of Fruits',
        height=500
    )
    
    return fig