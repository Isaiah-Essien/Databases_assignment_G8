# Task 2: SQL and MongoDB Schema

## Overview
This task involves creating an SQL and MongoDB schemas and ingesting user behavior data from a CSV file into SQL database. The dataset contains user information and their app usage statistics, which are stored in two separate tables. For MongoDB, only the schema was created.
 
## Files and Directories
- `mongodb_schema.py`: Python script to load the dataset, connect to MongoDB, and insert data into the collections.
- `dataset/user_behavior_dataset.csv`: CSV file containing user behavior data.
- `schema_diagram/sql_schema_diagram.drawio`: Diagram file representing the SQL schema.
- `sql_schema.sql`: SQL script for creating the schema in a relational database.


## SQL Schema

### Table for Users
- `device_id`: Unique identifier for the user (from `User ID` in the dataset).
- `age`: Age of the user.
- `gender`: Gender of the user.
- `user_behavior`: Behaviors of the user.

### Table for Device information
- `device_id`: Unique identifier for the user (from `User ID` in the dataset).
- `user_id`: ID of the user.
- `device_model`: model of device.
- `operating_system`: Operating system of the device.

### Table for App Usage Stats
- `user_id`: Reference to the user (from `User ID` in the dataset).
- `usage_id`: How users use devices.
- `app_usage_time`: Average app usage time per day (in minutes).
- `screen_on_time`: Average screen on time per day (in hours).
- `battery_drain`: Average battery drain per day (in mAh).
- `apps_installed`: Number of apps installed on the user's device.
- `data_usage`: How a user use data.
- `behavior_class`: Behaviors of users.


## MongoDB Schema

### Users Collection
The `Users` collection stores user information with the following fields:
- `_id`: Unique identifier for the user (from `User ID` in the dataset).
- `age`: Age of the user.
- `gender`: Gender of the user.
- `device_info`: Embedded document containing device information:
  - `device_model`: Model of the user's device.
  - `operating_system`: Operating system of the user's device.

### Usage_Stats Collection
The `Usage_Stats` collection stores app usage statistics for each user with the following fields:
- `user_id`: Reference to the user (from `User ID` in the dataset).
- `app_usage_time`: Average app usage time per day (in minutes).
- `screen_on_time`: Average screen on time per day (in hours).
- `battery_drain`: Average battery drain per day (in mAh).
- `apps_installed`: Number of apps installed on the user's device.
