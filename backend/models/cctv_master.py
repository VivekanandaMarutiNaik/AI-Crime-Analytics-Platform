from sqlalchemy import Column, Integer, String, Float

from backend.config.database import Base


class CCTVMaster(Base):
    __tablename__ = "cctv_master"

    cctv_id = Column(String, primary_key=True, index=True)
    cctv_name = Column(String)

    district_id = Column(Integer)
    district = Column(String)

    taluk_id = Column(Integer)
    taluk = Column(String)

    gp_id = Column(Float)
    gram_panchayat = Column(String)

    village_id = Column(Integer)
    village = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    location_type = Column(String)
    coverage_radius_meters = Column(Integer)

    status = Column(String)

    nearest_police_station = Column(String)