from sqlalchemy import Column, String, DateTime

from backend.config.database import Base


class EmployeeMaster(Base):
    __tablename__ = "employee_master"

    employee_id = Column(String, primary_key=True)

    kgid = Column(String)

    employee_name = Column(String)

    gender = Column(String)

    date_of_birth = Column(DateTime)

    blood_group = Column(String)

    rank = Column(String)

    rank_code = Column(String)

    appointment_date = Column(DateTime)

    district = Column(String)

    taluk = Column(String)

    police_station_name = Column(String)

    police_station_id = Column(String)