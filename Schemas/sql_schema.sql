
-- Create the table for the Users
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    age INT,
    gender VARCHAR(20),
    user_behavior VARCHAR(20),
);

-- Create the table for the Device Information
CREATE TABLE Device_Information (
    device_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    device_model VARCHAR(50),
    operating_system VARCHAR(20)
);

-- Create the table for the App Usage Stats
CREATE TABLE App_Usage_Stats (
    usage_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    app_usage_time INT,
    screen_on_time FLOAT,
    battery_drain INT,
    apps_installed INT,
    data_usage INT,
    behavior_class INT
);
