from sqlalchemy import Column, Integer, String, Float
from backend.config.database import Base


class CrimeCase(Base):
    __tablename__ = "crime_cases"

    id = Column(Integer, primary_key=True, index=True)

    crime_id = Column(String, unique=True, nullable=False, index=True)
    crime_datetime = Column(String, nullable=False)
    time_slot = Column(String)

    district = Column(String, index=True)
    taluk = Column(String)
    village = Column(String)
    gram_panchayat = Column(String)

    police_station_name = Column(String)
    police_station_latitude = Column(Float)
    police_station_longitude = Column(Float)

    crime_category = Column(String)
    crime_type = Column(String)
    crime_severity = Column(String)

    hotspot_score = Column(Integer)

    victim_age = Column(Integer)
    victim_gender = Column(String)

    accused_id = Column(String)
    accused_age = Column(Integer)
    accused_gender = Column(String)

    fir_registered = Column(String)
    case_status = Column(String)

    cctv_available = Column(String)

    response_time_minutes = Column(Integer)