# from fastapi import FastAPI
# app = FastAPI()
# @app.get("/home")
# def home():
#     return {"Data": "Test"}


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

# Database setup
DATABASE_URL = "mysql+pymysql://root:@localhost/gpsdata"  # No password included
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database model
class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Define Pydantic model for request validation
class LocationCreate(BaseModel):
    latitude: float
    longitude: float

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Create a route to post latitude and longitude
# @app.post("/locations/")
# def create_location(location: LocationCreate, db: Session = Depends(get_db)):
#     db_location = Location(latitude=location.latitude, longitude=location.longitude)
#     db.add(db_location)
#     db.commit()
#     db.refresh(db_location)
#     return {"id": db_location.id, "latitude": db_location.latitude, "longitude": db_location.longitude}

# # Run the app with: uvicorn script_name:app --reload


@app.post("/locations/")
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = Location(latitude=location.latitude, longitude=location.longitude)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return {"id": db_location.id, "latitude": db_location.latitude, "longitude": db_location.longitude}

# db_location = Location(latitude=location.latitude, longitude=location.longitude)
# db_add(db_)

   



