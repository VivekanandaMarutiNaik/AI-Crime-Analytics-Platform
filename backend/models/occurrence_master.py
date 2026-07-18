
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.config.database import Base


class OccurrenceMaster(Base):
    __tablename__ = "occurrence_master"

    occurrence_id = Column(String, primary_key=True, index=True)

    case_id = Column(
        String,
        ForeignKey("case_master.case_id"),
        nullable=False,
        unique=True,
    )

    occurrence_datetime = Column(DateTime)

    time_slot = Column(String)

    district = Column(String)
    taluk = Column(String)

    gram_panchayat = Column(String)
    village = Column(String)

    police_station = Column(String)

    crime_latitude = Column(Float)
    crime_longitude = Column(Float)

    case = relationship(
        "CaseMaster",
        back_populates="occurrence",
    )