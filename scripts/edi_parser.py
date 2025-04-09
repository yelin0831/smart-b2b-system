# pylint: skip-file
import json
import pandas as pd
from datetime import datetime

# Load order data from JSON
with open('../data/orders.json', 'r') as f:
    orders = json.load(f)

# Load customer and inventory data
customers = pd.read_csv('../data/customers.csv')
inventory = pd.read_csv('../data/inventory.csv')

# Create lists to store orders
processed_orders = []
reorder_requests = []

# Process each order
for order in orders:
    customer_id = order['CustomerID']
    product_id = order['ProductID']
    quantity = order['Quantity']
    order_id = order['OrderID']
    order_date = order['OrderDate']

    # Check if customer exists
    if customer_id not in customers['CustomerID'].values:
        print(f"[ERROR] Customer {customer_id} not found.")
        continue

    # Check if product exists
    if product_id not in inventory['ProductID'].values:
        print(f"[ERROR] Product {product_id} not found.")
        continue

    # Get current stock
    current_stock = inventory.loc[inventory['ProductID'] == product_id, 'Stock'].values[0]

    if quantity > current_stock:
        print(f"[WARNING] Not enough stock for order {order_id}. Skipped.")

        # Add a reorder request entry
        reorder_requests.append({
            'ProductID': product_id,
            'RequestedQty': quantity,
            'CustomerID': customer_id,
            'OrderID': order_id,
            'OrderDate': order_date
        })
        continue


    # Update inventory
    inventory.loc[inventory['ProductID'] == product_id, 'Stock'] -= quantity

    # Save processed order
    processed_orders.append({
        'OrderID': order_id,
        'CustomerID': customer_id,
        'ProductID': product_id,
        'Quantity': quantity,
        'OrderDate': order_date,
        'Status': 'Processed'
    })

# Save updated inventory
inventory.to_csv('../data/inventory_updated.csv', index=False)

# Save processed orders
df_orders = pd.DataFrame(processed_orders)
df_orders.to_csv('../data/processed_orders.csv', index=False)

# Save reorder requests if any
if reorder_requests:
    reorder_df = pd.DataFrame(reorder_requests)
    reorder_df.to_csv('../data/reorder_requests.csv', index=False)
    print("Reorder requests saved (Out-of-stock items detected)")

print("Order processing complete.")
