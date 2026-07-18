from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.config.database import Base


class ArrestMaster(Base):
    __tablename__ = "arrest_master"

    arrest_id = Column(String, primary_key=True)

    case_id = Column(
        String,
        ForeignKey("case_master.case_id"),
        nullable=False,
    )

    accused_person_id = Column(
        String,
        ForeignKey("accused_master.accused_person_id"),
        nullable=False,
        unique=True,
    )

    arrest_date = Column(DateTime)

    arresting_officer_id = Column(String)

    accused = relationship("AccusedMaster", back_populates="arrest")