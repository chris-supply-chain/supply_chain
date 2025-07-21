import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from IPython.display import display, HTML

def create_sample_data():
    """Create sample inventory data for the replenishment system."""
    data = {
        'product_id': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008'],
        'inventory_id': ['INV001', 'INV002', 'INV003', 'INV004', 'INV005', 'INV006', 'INV007', 'INV008'],
        'abc_sku': ['A', 'A', 'B', 'B', 'C', 'C', 'A', 'B'],
        'target_inventory': [500, 750, 300, 450, 150, 200, 600, 350],
        'sellable_inventory': [420, 680, 250, 380, 120, 160, 520, 290],
        'available_inventory': [380, 620, 220, 340, 100, 140, 480, 260],
        'daily_demand': [25, 35, 15, 20, 8, 12, 30, 18],
        'lead_time': [7, 10, 5, 8, 3, 4, 9, 6],
        'shelf_life_days': [22, 22, 22, 22, 22, 22, 22, 22],
        'last_order_date': [
            datetime.now() - timedelta(days=5),
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=7),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=10),
            datetime.now() - timedelta(days=6),
            datetime.now() - timedelta(days=4),
            datetime.now() - timedelta(days=8)
        ]
    }
    return pd.DataFrame(data)

def calculate_inventory_metrics(df):
    """Calculate additional inventory metrics."""
    # Calculate inventory gaps
    df['inventory_gap'] = df['target_inventory'] - df['sellable_inventory']
    df['available_gap'] = df['target_inventory'] - df['available_inventory']
    
    # Calculate days of inventory
    df['days_of_inventory'] = (df['sellable_inventory'] / df['daily_demand']).round(1)
    df['available_days'] = (df['available_inventory'] / df['daily_demand']).round(1)
    
    # Calculate reorder points
    df['reorder_point'] = (df['daily_demand'] * df['lead_time']).round(0)
    
    # Calculate safety stock and cycle stock
    df['safety_stock'] = (df['daily_demand'] * df['lead_time'] * 0.5).round(0)  # 50% of lead time demand
    df['cycle_stock'] = df['target_inventory'] - df['safety_stock']
    
    # Determine replenishment status
    df['replenishment_status'] = df.apply(
        lambda row: 'Reorder Now' if row['sellable_inventory'] <= row['reorder_point'] 
        else 'Monitor' if row['sellable_inventory'] <= row['reorder_point'] * 1.2
        else 'OK', axis=1
    )
    
    # Calculate suggested order quantity
    df['suggested_order'] = df.apply(
        lambda row: max(0, row['target_inventory'] - row['sellable_inventory']) 
        if row['sellable_inventory'] <= row['reorder_point'] else 0, axis=1
    )
    
    return df

def display_dashboard(df):
    """Display the inventory dashboard in Jupyter."""
    
    # Header
    display(HTML("<h1>📦 Inventory Replenishment System</h1>"))
    display(HTML("<hr>"))
    
    # Key Metrics
    total_products = len(df)
    reorder_count = len(df[df['replenishment_status'] == 'Reorder Now'])
    total_gap = int(df['inventory_gap'].sum())
    total_suggested = int(df['suggested_order'].sum())
    
    metrics_html = f"""
    <div style="display: flex; justify-content: space-between; margin: 20px 0;">
        <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h3>Total Products</h3>
            <h2>{total_products}</h2>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #fff3cd; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h3>Need Reorder</h3>
            <h2>{reorder_count}</h2>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #d1ecf1; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h3>Total Gap</h3>
            <h2>{total_gap:,}</h2>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #d4edda; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h3>Suggested Orders</h3>
            <h2>{total_suggested:,}</h2>
        </div>
    </div>
    """
    display(HTML(metrics_html))
    
    # Inventory Table
    display(HTML("<h2>📊 Inventory Overview</h2>"))
    
    # Create display dataframe
    display_columns = [
        'product_id', 'inventory_id', 'abc_sku', 'target_inventory', 
        'sellable_inventory', 'available_inventory', 'days_of_inventory',
        'replenishment_status', 'suggested_order'
    ]
    
    display_df = df[display_columns].copy()
    display_df.columns = [
        'Product ID', 'Inventory ID', 'ABC SKU', 'Target Inventory',
        'Sellable Inventory', 'Available Inventory', 'Days of Inventory',
        'Status', 'Suggested Order'
    ]
    
    # Color code the status
    def color_status(val):
        if val == 'Reorder Now':
            return 'background-color: #ffcccc'
        elif val == 'Monitor':
            return 'background-color: #fff3cd'
        else:
            return 'background-color: #d4edda'
    
    styled_df = display_df.style.map(color_status, subset=['Status'])
    display(styled_df)
    
    # Charts
    display(HTML("<h2>📈 Inventory Analytics</h2>"))
    
    # Create charts using plotly for better Jupyter compatibility
    col1, col2 = st.columns(2) if 'st' in globals() else [None, None]
    
    # ABC SKU distribution
    fig_abc = px.pie(
        df, 
        names='abc_sku', 
        title='Inventory Distribution by ABC SKU',
        color_discrete_map={'A': '#ff6b6b', 'B': '#4ecdc4', 'C': '#45b7d1'}
    )
    fig_abc.update_layout(height=400)
    display(fig_abc)
    
    # Inventory levels chart with hover information
    fig_inventory = go.Figure()
    
    # Create hover text for target inventory
    hover_texts = []
    for i, row in df.iterrows():
        hover_text = f"Product: {row['product_id']}<br>" + \
                    f"Target Inventory: {row['target_inventory']}<br>" + \
                    f"Safety Stock: {row['safety_stock']}<br>" + \
                    f"Cycle Stock: {row['cycle_stock']}"
        hover_texts.append(hover_text)
    
    # Target Inventory with safety stock and cycle stock hover info
    fig_inventory.add_trace(go.Bar(
        name='Target Inventory',
        x=df['product_id'],
        y=df['target_inventory'],
        marker_color='#2ecc71',
        text=hover_texts,
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig_inventory.add_trace(go.Bar(
        name='Sellable Inventory',
        x=df['product_id'],
        y=df['sellable_inventory'],
        marker_color='#3498db',
        hovertemplate='<b>%{x}</b><br>' +
                      'Sellable Inventory: %{y}<br>' +
                      '<extra></extra>'
    ))
    
    fig_inventory.add_trace(go.Bar(
        name='Available Inventory',
        x=df['product_id'],
        y=df['available_inventory'],
        marker_color='#e74c3c',
        hovertemplate='<b>%{x}</b><br>' +
                      'Available Inventory: %{y}<br>' +
                      '<extra></extra>'
    ))
    
    fig_inventory.update_layout(
        title='Inventory Levels by Product (Hover over Target Inventory to see Safety & Cycle Stock)',
        barmode='group',
        xaxis_title='Product ID',
        yaxis_title='Inventory Units',
        height=400,
        hovermode='closest'
    )
    
    display(fig_inventory)
    
    # Detailed view for selected product
    display(HTML("<h2>🔍 Detailed Product View</h2>"))
    
    # Show details for first product as example
    product_data = df.iloc[0]
    
    detail_html = f"""
    <div style="display: flex; justify-content: space-between; margin: 20px 0;">
        <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h4>Target Inventory</h4>
            <h3>{product_data['target_inventory']}</h3>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h4>Sellable Inventory</h4>
            <h3>{product_data['sellable_inventory']}</h3>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h4>Available Inventory</h4>
            <h3>{product_data['available_inventory']}</h3>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h4>Daily Demand</h4>
            <h3>{product_data['daily_demand']}</h3>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h4>Lead Time (days)</h4>
            <h3>{product_data['lead_time']}</h3>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 5px;">
            <h4>Days of Inventory</h4>
            <h3>{product_data['days_of_inventory']}</h3>
        </div>
    </div>
    """
    display(HTML(detail_html))
    
    # Progress bars for utilization
    target_utilization = (product_data['sellable_inventory'] / product_data['target_inventory']) * 100
    available_utilization = (product_data['available_inventory'] / product_data['target_inventory']) * 100
    
    utilization_html = f"""
    <h3>Inventory Utilization</h3>
    <div style="margin: 10px 0;">
        <label>Target Utilization: {target_utilization:.1f}%</label>
        <div style="width: 100%; background-color: #e9ecef; border-radius: 10px; height: 20px;">
            <div style="width: {target_utilization}%; background-color: #28a745; height: 20px; border-radius: 10px;"></div>
        </div>
    </div>
    <div style="margin: 10px 0;">
        <label>Available Utilization: {available_utilization:.1f}%</label>
        <div style="width: 100%; background-color: #e9ecef; border-radius: 10px; height: 20px;">
            <div style="width: {available_utilization}%; background-color: #007bff; height: 20px; border-radius: 10px;"></div>
        </div>
    </div>
    """
    display(HTML(utilization_html))

def main():
    """Main function to run the inventory analysis."""
    # Create sample data
    df = create_sample_data()
    df = calculate_inventory_metrics(df)
    
    # Display the dashboard
    display_dashboard(df)
    
    return df

# Run the dashboard
if __name__ == "__main__":
    df = main()
else:
    # For Jupyter notebook execution
    df = main() 
