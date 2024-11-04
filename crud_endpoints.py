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