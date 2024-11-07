'''This script Fetches the Latest entry from the database and makes Predictions with it'''

import requests
import joblib
import pandas as pd
import os

api_url = "https://crudendpoints.onrender.com/users/latest"

# Fetch the latest entry
try:
    response = requests.get(api_url)
    response.raise_for_status()
    latest_entry = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    latest_entry = None

# Continue only if latest_entry is available
if latest_entry:
    print(f"Fetched Latest Entry: \n {latest_entry}")

    # Construct the absolute path to the model file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'models', 'user_behaviour_model.pkl')

    # Load the model
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Model file not found at {model_path}")
        model = None

    if model:
        # Convert the fetched entry into a DataFrame
        data_df = pd.DataFrame([latest_entry['app_usage_stats']])


        data_df['Age'] = latest_entry['age']
        # Binary encoding for gender
        data_df['Gender'] = 1 if latest_entry['gender'].lower() == "male" else 0


        data_df['Device_Model'] = latest_entry['device_info']['device_model']
        data_df['Operating_System'] = latest_entry['device_info']['operating_system']
        data_df['App_Usage_Time_min_day'] = latest_entry['app_usage_stats']['app_usage_time']
        data_df['Screen_On_Time_hours_day'] = latest_entry['app_usage_stats']['screen_on_time']
        data_df['Battery_Drain_mAh_day'] = latest_entry['app_usage_stats']['battery_drain']
        data_df['Number_of_Apps_Installed'] = latest_entry['app_usage_stats']['apps_installed']
        data_df['Data_Usage_MB_day'] = latest_entry['app_usage_stats']['data_usage']

        expected_columns = ['Device_Model', 'Operating_System', 'App_Usage_Time_min_day',
                            'Screen_On_Time_hours_day', 'Battery_Drain_mAh_day', 'Number_of_Apps_Installed',
                            'Data_Usage_MB_day', 'Age', 'Gender']

        # Ensure all expected columns are present
        for col in expected_columns:
            if col not in data_df.columns:
                data_df[col] = 0

        data_df = data_df[expected_columns]

        # Handle categorical variables
        data_df = pd.get_dummies(
            data_df, columns=['Device_Model', 'Operating_System'], drop_first=True)

        # Align the DataFrame with the model's expected input features
        model_features = model.feature_names_in_
        for feature in model_features:
            if feature not in data_df.columns:
                data_df[feature] = 0

        data_df = data_df[model_features]

        input_data = data_df.values

        # Make the prediction
        prediction = model.predict(input_data)
        print(f"Predicted User Behavior Class: {prediction[0]}")
    else:
        print("Model could not be loaded. Prediction aborted.")
else:
    print("No valid user data available. Prediction aborted.")
