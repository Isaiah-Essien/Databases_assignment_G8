# Database Design Assignment

## Mobile Device Usage Pattern Analysis: A Task-Based Implementation

## 📱 Project Overview
This project analyzes mobile device usage patterns to predict user behavior through a systematic approach, implemented by a team of four developers. Each team member tackled specific components, building upon each other's work to create a comprehensive solution.

## 🎯 Problem Statement
Create an end-to-end system that can:
1. Store and manage mobile device usage data
2. Provide API access to the data
3. Predict user behavior based on usage patterns

## 👥 Team Tasks & Implementation

### Task 1: Database Schema Normalization
**Team Member:** Anissa  
**Problem:** Design a normalized database schema for unstructured Software Company Data

**Approach:**
1. Analyzed raw dataset structure
2. Identified entities and relationships
3. Applied normalization rules
4. Created visual schema representation

**Key Deliverables:**
- Normalized database schema
- Entity Relationship Diagram (ERD)
- Data dictionary
- Normalization documentation

### Task 2: Database Implementation
**Team Members:** Johnson  
**Problem:** Implement dual database system using PostgreSQL and MongoDB for  mobile device usage data

#### Dataset Used:
[Kaggle](https://www.kaggle.com/datasets/valakhorasani/mobile-device-usage-and-user-behavior-dataset)

**Approach:**
1. PostgreSQL Implementation:
   - Created tables based on normalized schema
   - Implemented relationships and constraints
   - Set up indexing for optimization
   - Developed data migration scripts

2. MongoDB Implementation:
   - Designed document structure
   - Created collections
   - Implemented data validation rules
   - Set up aggregation pipelines

**Key Deliverables:**
- PostgreSQL database schema
- MongoDB collections
- Data migration scripts
- Performance optimization documentation

### Task 3: API Development
**Team Member:** Elvis  
**Problem:** Create RESTful API endpoints for CRUD operations

**Approach:**
1. Set up FastAPI framework
2. Implemented endpoints:
   ```python
   # Example endpoint structure
   @app.post("/users/")
   async def create_user(user: UserModel):
       return await create_user_in_db(user)
   ```
3. Added data validation
4. Implemented error handling
5. Created API documentation

#### Play around: with the Endpoints:

[CRUD Endpoints](https://crudendpoints.onrender.com/docs)

**Key Deliverables:**
- FastAPI application
- CRUD endpoints
- Request/Response models
- API documentation
- Testing suite

### Task 4: Machine Learning Integration
**Team Member:** Isaiah  
**Problem:** Develop prediction system for user behavior

**Approach:**
1. Model Development:
   - Data preprocessing
   - Feature engineering
   - Model training
   - Validation

2. Integration:
   - Created prediction script
   - Implemented API connection
   - Set up real-time prediction

**Key Deliverables:**
- Trained ML model
- Prediction script
- Integration documentation
- Performance metrics