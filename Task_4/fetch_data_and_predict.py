import requests
import joblib
import pandas as pd

# Define the API endpoint for fetching the latest user entry
api_url = "https://crudendpoints.onrender.com/users/latest"

# Fetch the latest entry
try:
    response = requests.get(api_url)
    response.raise_for_status()  
    users = response.json()
    if users:
        latest_entry = users[-1]
    else:
        print("No entries found in the database.")
        latest_entry = None
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    latest_entry = None

# Continue only if latest_entry is available
if latest_entry:

    model_path = "Task_4/models/user_behaviour_model.pkl"
    model = joblib.load(model_path)

    # Convert the fetched entry into a DataFrame
    data_df = pd.DataFrame([latest_entry['app_usage_stats']])

    # Ensure all necessary columns match the model's expected input
    data_df['Age'] = latest_entry['age']
    # binary encoding for gender
    data_df['Gender'] = 1 if latest_entry['gender'] == "Male" else 0

    # Map other columns directly
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

    for col in expected_columns:
        if col not in data_df.columns:
            data_df[col] = 0

    data_df = data_df[expected_columns]
    input_data = data_df.values

    # Step 4: Make the prediction
    prediction = model.predict(input_data)
    print(f"Predicted User Behavior Class: {prediction[0]}")
