# Import necessary libraries
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from datetime import datetime

# Function to connect to MongoDB collections (both online and local)
def connect_to_mongo(collection_name):
    try:
        # Connect to online MongoDB
        client_online = MongoClient("mongodb+srv://JaGrIt:jagrit@cluster0.fegfu.mongodb.net/")
        db_online = client_online["MSR"]
        collection_online = db_online[collection_name]
        
        # Connect to local MongoDB
        client_local = MongoClient("mongodb://localhost:27017/")
        db_local = client_local["MSR"]
        collection_local = db_local[collection_name]
        
        return collection_online, collection_local
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None

# Function to retrieve data from both collections and merge them
def retrieve_and_merge_data(collection_name, query, projection):
    collection_online, collection_local = connect_to_mongo(collection_name)
    
    # Retrieve data from online collection
    cursor_online = collection_online.find(query, projection)
    df_online = pd.DataFrame(list(cursor_online))
    
    # Retrieve data from local collection
    cursor_local = collection_local.find(query, projection)
    df_local = pd.DataFrame(list(cursor_local))
    
    # Merge the two dataframes
    df_combined = pd.concat([df_online, df_local], ignore_index=True)
    
    return df_combined

# Retrieve bug report data from both databases and merge
bug_reports_df = retrieve_and_merge_data(
    collection_name="Bug_meta_data",
    query={},
    projection={
        'creation_time': 1,
        'product': 1,
        'component': 1,
        'version': 1,
        '_id': 0  # Exclude the MongoDB _id field
    }
)

# Convert creation_time to datetime
# print(bug_reports_df.summary)
print(bug_reports_df.describe())

bug_reports_df['creation_time'] = pd.to_datetime(bug_reports_df['creation_time'])

# Extract year and month for aggregation
bug_reports_df['year_month'] = bug_reports_df['creation_time'].dt.to_period('M')

# **Filter products with more than 1000 bug reports**

# Count total bugs per product
product_bug_counts = bug_reports_df.groupby('product').size().reset_index(name='total_bugs')

# Filter products with total bugs >= 1000
products_with_many_bugs = product_bug_counts[product_bug_counts['total_bugs'] >= 5000]['product']

# Filter the main dataframe to include only these products
bug_reports_df = bug_reports_df[bug_reports_df['product'].isin(products_with_many_bugs)]

# Group by year_month and product to get bug counts
bug_counts = bug_reports_df.groupby(['year_month', 'product']).size().reset_index(name='bug_count')

# Convert year_month back to datetime for plotting
bug_counts['year_month'] = bug_counts['year_month'].dt.to_timestamp()

# Pivot the DataFrame for plotting
bug_counts_pivot = bug_counts.pivot(index='year_month', columns='product', values='bug_count').fillna(0)

# Plotting the bug trends over time for each product
plt.figure(figsize=(14, 7))
for product in bug_counts_pivot.columns:
    plt.plot(bug_counts_pivot.index, bug_counts_pivot[product], label=product)

plt.title('Trend of Bug Reports Over Time by Product (Products with ≥5000 Bugs)')
plt.xlabel('Time')
plt.ylabel('Number of Bugs Reported')
plt.legend()
plt.tight_layout()
plt.show()
