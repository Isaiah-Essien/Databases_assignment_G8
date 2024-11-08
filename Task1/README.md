# Task 1: Database Schema Normalization for Software Company Data

**Team Member:** Anissa Tegawende  OUEDRAOGO  
**Task Objective:** Design and implement a normalized database schema for unstructured software company data.

---

## Project Overview

This task involves transforming unstructured data from a software company into a structured, normalized SQL database. By examining the data, identifying key entities and relationships, and applying database normalization techniques, we aim to create a schema that is efficient, consistent, and minimizes redundancy.

### Key Deliverables

- Normalized Database Schema
- Entity-Relationship Diagram (ERD)
- Data Dictionary
- Normalization Documentation

---

## Requirements

- **Python 3.7+**
- **Libraries**: `pandas`, `sqlite3`
- **Database Management Tool**: SQLite (using Jupyter Notebook for code execution)

---

## Project Structure

- **data/**: Folder containing raw and processed data files.
- **scripts/**: Folder containing the Python scripts for loading, transforming, and inserting data.
- **docs/**: Documentation for the database schema, data dictionary, and ERD.
- **README.md**: Project documentation (this file).

---

## Workflow Steps

### Step 1: Load and Inspect Data

1. Load the Excel file using `pandas` in Jupyter Notebook.
2. Inspect data sheets to understand structure and identify entities:
   - **Entities Identified**: Company, Project, Client, Team Member, Project Requirements.
   - **Relationships**: Many-to-many relationships between Projects and Clients, and Projects and Team Members.

### Step 2: Design Normalized Schema

1. Identify columns that belong to each entity.
2. Apply normalization rules:
   - **1NF** (Eliminate repeating groups).
   - **2NF** (Eliminate partial dependencies).
   - **3NF** (Eliminate transitive dependencies).

### Step 3: Set Up Database and Tables

1. Connect to an SQLite database.
2. Create tables based on the identified schema:
   - Company
   - Project
   - Client
   - Team Member
   - Requirements
   - Join tables (Project_Client and Project_Team) for many-to-many relationships.

### Step 4: Data Transformation and Insertion

1. Clean and separate data by each entity.
2. Insert data into tables using `pandas.to_sql` in Jupyter Notebook.
3. Verify foreign key constraints and data integrity by running test queries.

### Step 5: Documentation

- **ERD**: Entity-Relationship Diagram showing table relationships.
- **Data Dictionary**: Details on each table’s fields, data types, and constraints.
- **Normalization Process**: Documentation of the normalization steps applied to the dataset.

---

## How to Run

1. **Clone this Repository**: Download the files to your local machine.
   
   ```bash
   git clone [repository-url]
   cd database-normalization
   ```

2. **Open Jupyter Notebook**: Access the Jupyter notebook file for data loading and transformation steps.

3. **Execute Code**:
   - Run each cell in the notebook to create the database schema, load data, and verify relationships.

4. **Check Results**:
   - Use SQLite or any compatible database viewer to examine the final structure and relationships.


## Contact Information

For any questions or clarifications, please reach out:

- **Name**: Anissa
- **Email**: a.ouedraogo@alustudent.com

