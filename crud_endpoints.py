from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# Database connection setup
DATABASE_URL = "postgresql://userbehavior:fBhQfMmwf2Tuh5mlR2JHhoPXhDiyVyfe@dpg-cskcbitds78s73999kb0-a.oregon-postgres.render.com/userbehavior"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI instance
app = FastAPI()

# SQLAlchemy Models
class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    user_behavior = Column(String)

class DeviceInformation(Base):
    __tablename__ = "Device_Information"
    device_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id", ondelete="CASCADE"))
    device_model = Column(String)
    operating_system = Column(String)
    user = relationship("User", back_populates="device_info")

class AppUsageStats(Base):
    __tablename__ = "App_Usage_Stats"
    usage_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id", ondelete="CASCADE"))
    app_usage_time = Column(Integer)
    screen_on_time = Column(Float)
    battery_drain = Column(Integer)
    apps_installed = Column(Integer)
    data_usage = Column(Integer)
    behavior_class = Column(Integer)
    user = relationship("User", back_populates="app_usage_stats")

User.device_info = relationship("DeviceInformation", uselist=False, back_populates="user")
User.app_usage_stats = relationship("AppUsageStats", uselist=False, back_populates="user")

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Pydantic Models
class DeviceInfo(BaseModel):
    device_model: str
    operating_system: str

class AppUsageStatsModel(BaseModel):
    app_usage_time: int
    screen_on_time: float
    battery_drain: int
    apps_installed: int
    data_usage: int
    behavior_class: int

class UserCreate(BaseModel):
    age: int
    gender: str
    user_behavior: str
    device_info: DeviceInfo
    app_usage_stats: AppUsageStatsModel

class UserDetail(UserCreate):
    user_id: int
    device_info: DeviceInfo
    app_usage_stats: AppUsageStatsModel
    class Config:
        orm_mode = True

# Dependency for the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create (POST) - Creates a new user with device and app usage information
@app.post("/users/", response_model=UserDetail)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(age=user.age, gender=user.gender, user_behavior=user.user_behavior)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Insert Device Information
    device_info = DeviceInformation(
        user_id=db_user.user_id,
        device_model=user.device_info.device_model,
        operating_system=user.device_info.operating_system
    )
    db.add(device_info)

    # Insert App Usage Stats
    app_usage_stats = AppUsageStats(
        user_id=db_user.user_id,
        app_usage_time=user.app_usage_stats.app_usage_time,
        screen_on_time=user.app_usage_stats.screen_on_time,
        battery_drain=user.app_usage_stats.battery_drain,
        apps_installed=user.app_usage_stats.apps_installed,
        data_usage=user.app_usage_stats.data_usage,
        behavior_class=user.app_usage_stats.behavior_class
    )
    db.add(app_usage_stats)
    db.commit()
    
    db.refresh(db_user)
    return db_user

# Read (GET) - Retrieve all information about a user
@app.get("/users/{user_id}", response_model=UserDetail)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update (PUT) - Update user information in all related tables
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

# Delete (DELETE) - Delete user and associated records in all tables
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User and associated records deleted successfully"}