from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import func 
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection setup with echo=True for SQL logging
DATABASE_URL = "postgresql://userbehavior:fBhQfMmwf2Tuh5mlR2JHhoPXhDiyVyfe@dpg-cskcbitds78s73999kb0-a.oregon-postgres.render.com/userbehavior"
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Enable SQL logging
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,
    max_overflow=10
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI instance
app = FastAPI()

# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"  # Changed to lowercase
    user_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    user_behavior = Column(String)

class DeviceInformation(Base):
    __tablename__ = "device_information"  # Changed to lowercase
    device_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    device_model = Column(String)
    operating_system = Column(String)
    user = relationship("User", back_populates="device_info")

class AppUsageStats(Base):
    __tablename__ = "app_usage_stats"  # Changed to lowercase
    usage_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    app_usage_time = Column(Integer)
    screen_on_time = Column(Float)
    battery_drain = Column(Integer)
    apps_installed = Column(Integer)
    data_usage = Column(Integer)
    behavior_class = Column(Integer)
    user = relationship("User", back_populates="app_usage_stats")

User.device_info = relationship("DeviceInformation", uselist=False, back_populates="user", cascade="all, delete-orphan")
User.app_usage_stats = relationship("AppUsageStats", uselist=False, back_populates="user", cascade="all, delete-orphan")

# Pydantic Models
class DeviceInfo(BaseModel):
    device_model: str
    operating_system: str
    model_config = ConfigDict(from_attributes=True)

class AppUsageStatsModel(BaseModel):
    app_usage_time: int
    screen_on_time: float
    battery_drain: int
    apps_installed: int
    data_usage: int
    behavior_class: int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    age: int
    gender: str
    user_behavior: str
    device_info: DeviceInfo
    app_usage_stats: AppUsageStatsModel

class UserDetail(BaseModel):
    user_id: int
    age: int
    gender: str
    user_behavior: str
    device_info: DeviceInfo
    app_usage_stats: AppUsageStatsModel
    model_config = ConfigDict(from_attributes=True)

# Database initialization
@app.on_event("startup")
async def startup_event():
    try:
        # Verify database connection
        with engine.connect() as conn:
            logger.info("Successfully connected to the database")
            
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Log existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Existing tables in database: {existing_tables}")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise e

# Dependency for the database session with logging
def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session created")
        yield db
    finally:
        logger.info("Database session closed")
        db.close()

# Create (POST)
@app.post("/users/", response_model=UserDetail)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Find the current maximum user_id in the database
        max_user_id = db.query(func.max(User.user_id)).scalar()  # Get the highest user_id or None
        new_user_id = (max_user_id or 0) + 1  # Start at 1 if max_user_id is None

        logger.info(f"Creating new user with ID: {new_user_id}")

        # Create the new user with the incremented user_id
        db_user = User(
            user_id=new_user_id,
            age=user.age,
            gender=user.gender,
            user_behavior=user.user_behavior
        )
        db.add(db_user)
        db.flush()  # Flush to update the session with new user data

        # Add device information
        device_info = DeviceInformation(
            user_id=new_user_id,
            device_model=user.device_info.device_model,
            operating_system=user.device_info.operating_system
        )
        db.add(device_info)

        # Add app usage stats
        app_usage_stats = AppUsageStats(
            user_id=new_user_id,
            app_usage_time=user.app_usage_stats.app_usage_time,
            screen_on_time=user.app_usage_stats.screen_on_time,
            battery_drain=user.app_usage_stats.battery_drain,
            apps_installed=user.app_usage_stats.apps_installed,
            data_usage=user.app_usage_stats.data_usage,
            behavior_class=user.app_usage_stats.behavior_class
        )
        db.add(app_usage_stats)

        # Commit the transaction
        db.commit()
        db.refresh(db_user)
        logger.info("User created successfully with incremented user_id")

        return db_user

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

# Get the latest user
@app.get("/users/latest", response_model=UserDetail)
def get_latest_user(db: Session = Depends(get_db)):
    try:
        logger.info("Attempting to retrieve the latest user")
        
        # Query the latest user by sorting by user_id in descending order
        latest_user = (
            db.query(User)
            .outerjoin(DeviceInformation)
            .outerjoin(AppUsageStats)
            .order_by(User.user_id.desc())
            .first()
        )
        
        if not latest_user:
            logger.warning("No users found in the database")
            raise HTTPException(status_code=404, detail="No users found")
            
        logger.info(f"Successfully retrieved the latest user with ID: {latest_user.user_id}")
        return latest_user
        
    except Exception as e:
        logger.error(f"Error retrieving the latest user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving the latest user: {str(e)}")

# Read (GET)
@app.get("/users/{user_id}", response_model=UserDetail)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Attempting to retrieve user with ID: {user_id}")
        
        # Query with explicit joins
        user = (
            db.query(User)
            .outerjoin(DeviceInformation)
            .outerjoin(AppUsageStats)
            .filter(User.user_id == user_id)
            .first()
        )
        
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
            
        logger.info(f"Successfully retrieved user: {user.user_id}")
        return user
        
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")

# Get all users
@app.get("/users/", response_model=list[UserDetail])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Attempting to retrieve users with skip={skip} and limit={limit}")
        
        # Query with explicit joins
        users = (
            db.query(User)
            .outerjoin(DeviceInformation)
            .outerjoin(AppUsageStats)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        logger.info(f"Retrieved {len(users)} users")
        return users
        
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")

# Update (PUT)
@app.put("/users/{user_id}", response_model=UserDetail)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user data
    db_user.age = user.age
    db_user.gender = user.gender
    db_user.user_behavior = user.user_behavior

    # Update device information
    db_device_info = db.query(DeviceInformation).filter(DeviceInformation.user_id == user_id).first()
    if db_device_info:
        db_device_info.device_model = user.device_info.device_model
        db_device_info.operating_system = user.device_info.operating_system

    # Update app usage stats
    db_app_usage_stats = db.query(AppUsageStats).filter(AppUsageStats.user_id == user_id).first()
    if db_app_usage_stats:
        db_app_usage_stats.app_usage_time = user.app_usage_stats.app_usage_time
        db_app_usage_stats.screen_on_time = user.app_usage_stats.screen_on_time
        db_app_usage_stats.battery_drain = user.app_usage_stats.battery_drain
        db_app_usage_stats.apps_installed = user.app_usage_stats.apps_installed
        db_app_usage_stats.data_usage = user.app_usage_stats.data_usage
        db_app_usage_stats.behavior_class = user.app_usage_stats.behavior_class

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete (DELETE)
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User and associated records deleted successfully"}



