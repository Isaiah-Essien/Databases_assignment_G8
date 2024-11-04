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