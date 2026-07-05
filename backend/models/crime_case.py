from sqlalchemy import Column, Integer, String, Float, Date, Time
from backend.config.database import Base

class CrimeCase(Base):
    __tablename__ = "crime_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, nullable=False)
    fir_number = Column(String, unique=True, nullable=False)
    crime_type = Column(String, nullable=False)
    district = Column(String, nullable=False)
    police_station = Column(String, nullable=False)
    incident_date = Column(Date)
    incident_time = Column(Time)
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String)
    officer_name = Column(String)
    brief_facts = Column(String)