from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend.config.database import Base


class VictimMaster(Base):
    __tablename__ = "victim_master"

    victim_id = Column(String, primary_key=True)

    case_id = Column(
        String,
        ForeignKey("case_master.case_id"),
        nullable=False,
    )

    victim_name = Column(String)

    gender = Column(String)

    age = Column(Integer)

    occupation = Column(String)

    injury_type = Column(String)

    relationship_to_accused = Column(String)

    address = Column(String)

    case = relationship("CaseMaster", back_populates="victims")