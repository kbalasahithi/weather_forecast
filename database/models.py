from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    
    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float)
    pressure = Column(Float)
    description = Column(String)
    
    def __repr__(self):
        return f"<WeatherData(city='{self.city}', timestamp='{self.timestamp}')>"