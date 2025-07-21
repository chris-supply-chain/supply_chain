import pandas as pd

# Original Data
data = {'Product' : ['Product A', 'Product B', 'Product C'],
        'Daily Demand' : [20, 30, 40],
        'Std Demand Forecast' : [5, 3, 6],
        'Lead Time' : [15, 25, 17],
        'Review Time' : [7, 7, 7],
        'Z-score' : [1.96, 1.96, 1.96]
       }

# Create DataFrame
df = pd.DataFrame(data)

# Calculate Cycle Stock
df['Cycle Stock'] = (df['Daily Demand'] * (df['Lead Time'] + df['Review Time'])).round(0)

# Calculate Safety Stock
df['Safety Stock'] = (df['Z-score'] * df['Std Demand Forecast'] *
                      (df['Lead Time'] + df['Review Time'])**(1/2)).round(0).astype(int)

# Calculate Target Stock
df['Target Stock'] = df['Cycle Stock'] + df['Safety Stock']

# Add Daily Sales (Example data, can be updated as needed)
df['Daily Sales'] = df['Daily Demand'] - 2  # Example: assume sales is daily demand minus 2 units

# Add Final Planning Horizon (Lead Time + Review Time)
df['Final Planning Horizon (Days)'] = df['Lead Time'] + df['Review Time']

# Reorder columns to place Target Stock, Cycle Stock, and Safety Stock right after Product
df_result = df[['Product', 'Target Stock', 'Cycle Stock', 'Safety Stock', 'Daily Demand', 'Daily Sales', 'Final Planning Horizon (Days)']]

# Print the final DataFrame
print(df_result)
