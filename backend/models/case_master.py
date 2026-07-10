from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from backend.config.database import Base


class CaseMaster(Base):
    __tablename__ = "case_master"

    case_id = Column(String, primary_key=True, index=True)

    crime_datetime = Column(DateTime, nullable=False)

    district = Column(String, nullable=False)
    taluk = Column(String, nullable=False)
    police_station = Column(String, nullable=False)

    crime_category = Column(String, nullable=False)
    crime_type = Column(String, nullable=False)
    crime_severity = Column(String, nullable=False)

    case_status = Column(String, nullable=False)
    fir_registered = Column(String, nullable=False)

    act_id = Column(String)
    section_id = Column(String)

    victims = relationship(
        "VictimMaster",
        back_populates="case"
    )

    accused = relationship(
        "AccusedMaster",
        back_populates="case"
    )

    investigation = relationship(
        "InvestigationMaster",
        back_populates="case",
        uselist=False,
    )

    chargesheet = relationship(
        "ChargesheetMaster",
        back_populates="case",
        uselist=False,
    )