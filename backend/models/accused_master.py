from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from backend.config.database import Base


class AccusedMaster(Base):
    __tablename__ = "accused_master"

    accused_person_id = Column(String, primary_key=True)

    case_id = Column(
        String,
        ForeignKey("case_master.case_id"),
        nullable=False,
    )

    accused_name = Column(String)

    gender = Column(String)

    age = Column(Integer)

    occupation = Column(String)

    is_arrested = Column(Boolean)

    is_history_sheeter = Column(Boolean)

    address = Column(String)

    case = relationship("CaseMaster", back_populates="accused")

    arrest = relationship(
        "ArrestMaster",
        back_populates="accused",
        uselist=False,
    )