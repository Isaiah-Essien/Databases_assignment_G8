import pandas as pd
from pymongo import MongoClient

# Load the dataset
file_path = 'dataset/user_behavior_dataset.csv'
dataset = pd.read_csv(file_path)
print(dataset)


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['user_data']

# Create collections
users_collection = db['Users']
usage_stats_collection = db['Usage_Stats']

# Iterate through the dataset and insert documents into MongoDB
for _, row in dataset.iterrows():
    # Insert user data into Users collection
    user_document = {
        "_id": row['User ID'],
        "age": row['Age'],
        "gender": row['Gender'],
        "device_info": {
            "device_model": row['Device Model'],
            "operating_system": row['Operating System']
        }
    }
    users_collection.insert_one(user_document)
    
    # Insert usage statistics into Usage_Stats collection
    usage_stats_document = {
        "user_id": row['User ID'],
        "app_usage_time": row['App Usage Time (min/day)'],
        "screen_on_time": row['Screen On Time (hours/day)'],
        "battery_drain": row['Battery Drain (mAh/day)'],
        "apps_installed": row['Number of Apps Installed'],
        "data_usage": row['Data Usage (MB/day)'],
        "behavior_class": row['User Behavior Class']
    }
    usage_stats_collection.insert_one(usage_stats_document)

print("Data inserted successfully.")
