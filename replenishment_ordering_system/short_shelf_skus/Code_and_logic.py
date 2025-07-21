import pandas as pd

def create_inventory_data():
    """Create the initial inventory data."""
    data = {
        'Product': ['Product A', 'Product B', 'Product C'],
        'Daily Demand': [20, 30, 40],
        'Std Demand Forecast': [5, 3, 6],
        'Lead Time': [15, 25, 17],
        'Review Time': [7, 7, 7],
        'Z-score': [1.96, 1.96, 1.96]  # Placeholder Z-scores for now
    }
    return pd.DataFrame(data)

def calculate_basic_inventory_metrics(df, high_z_score=2.56):
    """Calculate basic inventory metrics including cycle stock and safety stock."""
    # Calculate Cycle Stock
    df['Cycle Stock'] = (df['Daily Demand'] * (df['Lead Time'] + df['Review Time'])).round(0)
    
    # Calculate Safety Stock with new Z-score
    df['Safety Stock'] = (df['Z-score'] * df['Std Demand Forecast'] *
                          (df['Lead Time'] + df['Review Time'])**(1/2)).round(0).astype(int)
    
    # Update Z-score to high value
    df['Z-score'] = high_z_score
    
    # Calculate Target Stock
    df['Target Stock'] = df['Cycle Stock'] + df['Safety Stock']
    
    # Add Daily Sales (Example data)
    df['Daily Sales'] = df['Daily Demand'] - 2
    
    # Add Final Planning Horizon
    df['Final Planning Horizon (Days)'] = df['Lead Time'] + df['Review Time']
    
    return df

def calculate_target_inventory(df, shelf_life_days=22, inventory_cap_percentage=0.7):
    """Calculate target inventory units and weeks with shelf life constraints."""
    days_in_week = 7
    
    # Calculate shelf life in weeks
    shelf_life_weeks = shelf_life_days / days_in_week
    
    # Calculate initial target inventory units (no cap applied)
    initial_target_inventory_days = shelf_life_days * 1.0  # 100% of shelf life
    df['Initial Target Inventory Units'] = (df['Daily Demand'] * initial_target_inventory_days).round(0)
    
    # Calculate initial cycle stock and safety stock
    df['Initial Safety Stock'] = df['Safety Stock']
    df['Initial Cycle Stock'] = df['Initial Target Inventory Units'] - df['Initial Safety Stock']
    
    # Calculate initial target weeks
    df['Initial Target Weeks'] = (df['Initial Target Inventory Units'] / df['Daily Demand'] / days_in_week).round(1)
    
    # Apply shelf life cap to both target units and weeks (using 70% cap)
    max_target_weeks = (shelf_life_days * inventory_cap_percentage) / days_in_week
    max_target_units = (df['Daily Demand'] * shelf_life_days * inventory_cap_percentage).round(0)
    
    # Calculate final target inventory units (capped)
    df['Final Target Inventory Units'] = df['Initial Target Inventory Units'].clip(upper=max_target_units)
    
    # Calculate final target weeks (capped)
    df['Final Target Weeks'] = df['Initial Target Weeks'].clip(upper=max_target_weeks)
    
    # Calculate final cycle stock and safety stock
    # First, remove ALL safety stock from final target inventory
    df['Final Safety Stock'] = 0  # Remove all safety stock
    df['Final Cycle Stock'] = df['Final Target Inventory Units']  # All remaining is cycle stock
    
    # Add shelf life columns
    df['Shelf Life Days'] = shelf_life_days
    df['Shelf Life Cap'] = inventory_cap_percentage
    df['Max Shelf Life Days'] = shelf_life_days * inventory_cap_percentage
    df['Max Shelf Life Weeks'] = (shelf_life_days * inventory_cap_percentage) / days_in_week
    
    # Debug: Print the cap calculation
    print(f"\nShelf Life Cap Calculation:")
    print(f"Shelf Life: {shelf_life_days} days")
    print(f"Shelf Life: {shelf_life_weeks:.1f} weeks")
    print(f"Cap Percentage: {inventory_cap_percentage}")
    print(f"Max Target Weeks: {max_target_weeks:.2f} weeks")
    
    return df

def print_debug_info(df):
    """Print debugging information for verification."""
    print("\nTarget Inventory Analysis:")
    print(df[['Product', 'Initial Cycle Stock', 'Initial Safety Stock', 'Initial Target Inventory Units', 
              'Final Target Inventory Units', 'Final Cycle Stock', 'Final Safety Stock', 
              'Initial Target Weeks', 'Final Target Weeks', 'Shelf Life Days', 'Shelf Life Cap', 
              'Max Shelf Life Days', 'Max Shelf Life Weeks', 'Daily Sales', 'Daily Demand']])

def main():
    """Main function to run the inventory analysis."""
    # Configuration
    SHELF_LIFE_DAYS = 22
    INVENTORY_CAP_PERCENTAGE = 0.7  # 70% of shelf life
    HIGH_Z_SCORE = 2.56
    
    # Create and process data
    df = create_inventory_data()
    df = calculate_basic_inventory_metrics(df, HIGH_Z_SCORE)
    df = calculate_target_inventory(df, SHELF_LIFE_DAYS, INVENTORY_CAP_PERCENTAGE)
    
    # Print target inventory output
    print_debug_info(df)
    
    # Use the same columns for CSV output as what we're printing
    final_columns = [
        'Product', 'Initial Cycle Stock', 'Initial Safety Stock', 'Initial Target Inventory Units',
        'Final Target Inventory Units', 'Final Cycle Stock', 'Final Safety Stock', 
        'Initial Target Weeks', 'Final Target Weeks', 'Shelf Life Days', 'Shelf Life Cap', 
        'Max Shelf Life Days', 'Max Shelf Life Weeks', 'Daily Sales', 'Daily Demand'
    ]
    
    df_result = df[final_columns]
    
    # Save results
    output_path = '/Users/christian_hahn/Documents/stock_output_with_shelf_life.csv'
    df_result.to_csv(output_path, index=False)
    
    print(f"\nFile saved to: {output_path}")
    
    return df_result

if __name__ == "__main__":
    main() 
