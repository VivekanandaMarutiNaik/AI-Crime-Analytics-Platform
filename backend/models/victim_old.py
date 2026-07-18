from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class Victim(Base):
    __tablename__ = "victims"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("crime_cases.case_id"))
    victim_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    occupation = Column(String)