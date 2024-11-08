import pandas as pd

# Load the Excel file
excel_file = 'Unstructured Data - Software Company.xlsx'
excel_data = pd.ExcelFile(excel_file)

# Get sheet names
sheet_names = excel_data.sheet_names

# Load data from relevant sheets (replace with actual sheet names)
requirements_data = excel_data.parse('Can you update the unstructured')
client_data = excel_data.parse('Sheet1')

# Display first few rows to inspect data
print(requirements_data.head())
print(client_data.head())

# Proceed with separating entities into tables (this part needs further development)
# ..
# Get basic info for requirements_data
print("Requirements Data Info:")
print(requirements_data.info())

# Get basic info for client_data
print("\nClient Data Info:")
print(client_data.info())

# Check for unique values and potential keys
print("\nUnique values in requirements_data columns:")
print(requirements_data.nunique())

print("\nUnique values in client_data columns:")
print(client_data.nunique())
# Separate the Company table (since company names might repeat, use .drop_duplicates())
company_columns = ['Company']  # Only the company name for now
companies_df = requirements_data[company_columns].drop_duplicates()

# Separate the Client table
client_columns = ['Client ID', 'Team Lead', 'Team Members']
clients_df = requirements_data[client_columns].drop_duplicates()

# Separate the Project table
project_columns = ['Project ID', 'Project name', 'Company', 'Client ID', 'Requirements', 'Deadline']
projects_df = requirements_data[project_columns].drop_duplicates()

# Display the first few rows of each table
print("Companies Table:")
print(companies_df.head())

print("\nClients Table:")
print(clients_df.head())

print("\nProjects Table:")
print(projects_df.head())
import sqlite3

# Connect to SQLite (creates a new database file if it doesn't exist)
conn = sqlite3.connect('software_company_data.db')  # Name your database file
cursor = conn.cursor()

# Step 1: Create tables for Companies, Clients, and Projects

# Create Companies table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT UNIQUE
    )
''')

# Create Clients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id TEXT UNIQUE,
        team_lead TEXT,
        team_members TEXT
    )
''')

# Create Projects table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT UNIQUE,
        project_name TEXT,
        company_name TEXT,
        client_id TEXT,
        requirements TEXT,
        deadline TEXT,
        FOREIGN KEY (company_name) REFERENCES companies(company_name),
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    )
''')

# Step 2: Insert data from DataFrames into the SQLite tables

# Insert data into the Companies table
companies_df.to_sql('companies', conn, if_exists='replace', index=False)

# Insert data into the Clients table
clients_df.to_sql('clients', conn, if_exists='replace', index=False)

# Insert data into the Projects table
projects_df.to_sql('projects', conn, if_exists='replace', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data successfully inserted into SQLite database.")
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('software_company_data.db')
cursor = conn.cursor()

# Enable foreign key support (only necessary if you're enforcing foreign keys in SQLite)
cursor.execute("PRAGMA foreign_keys = ON;")

# Create tables using Python's multi-line strings for SQL commands
try:
    # Company Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Company (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL
        );
    """)

    # Project Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project (
            project_id INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL,
            company_id INTEGER,
            deadline DATE,
            FOREIGN KEY (company_id) REFERENCES Company(company_id)
        );
    """)

    # Client Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Client (
            client_id INTEGER PRIMARY KEY,
            client_name TEXT NOT NULL
        );
    """)

    # Team Member Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Team_Member (
            team_member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_member_name TEXT NOT NULL,
            is_team_lead BOOLEAN
        );
    """)

    # Project_Client Table (join table for many-to-many relationship)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project_Client (
            project_client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            client_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES Project(project_id),
            FOREIGN KEY (client_id) REFERENCES Client(client_id)
        );
    """)

    # Requirements Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Requirements (
            requirement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            requirement_description TEXT,
            FOREIGN KEY (project_id) REFERENCES Project(project_id)
        );
    """)

    print("Tables created successfully.")

except sqlite3.Error as e:
    print("An error occurred:", e)

# Commit the transaction and close the connection
conn.commit()
conn.close()
# Reconnect to SQLite
conn = sqlite3.connect('software_company_data.db')
cursor = conn.cursor()

# Check the columns in the 'projects' table
cursor.execute("PRAGMA table_info(projects);")
columns = cursor.fetchall()
print("Projects Table Structure:")
for column in columns:
    print(column)

# Check the foreign keys in the 'projects' table
cursor.execute('PRAGMA foreign_key_list(projects);')
foreign_keys = cursor.fetchall()
print("\nForeign Key Constraints in Projects Table:")
for fk in foreign_keys:
    print(fk)

# Close the connection
conn.close()
# Reconnect to SQLite
conn = sqlite3.connect('software_company_data.db')
cursor = conn.cursor()

# Verify data integrity by checking projects with invalid company names (instead of company_id)
cursor.execute('''
SELECT * FROM projects
WHERE "Company" NOT IN (SELECT "Company" FROM companies);
''')
invalid_entries = cursor.fetchall()

# Print out invalid entries if found
if invalid_entries:
    print("Invalid entries found:")
    for entry in invalid_entries:
        print(entry)
else:
    print("All projects have valid company names.")

# Close the connection
conn.close()

