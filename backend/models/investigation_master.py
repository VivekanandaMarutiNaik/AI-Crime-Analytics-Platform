from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.config.database import Base


class InvestigationMaster(Base):
    __tablename__ = "investigation_master"

    investigation_id = Column(String, primary_key=True)

    case_id = Column(
        String,
        ForeignKey("case_master.case_id"),
        nullable=False,
        unique=True,
    )

    investigating_officer_id = Column(String)

    investigation_start_date = Column(DateTime)

    investigation_end_date = Column(DateTime)

    investigation_status = Column(String)

    witness_count = Column(Integer)

    evidence_collected = Column(String)

    forensic_required = Column(String)

    forensic_completed = Column(String)
    remarks = Column(String)

    case = relationship("CaseMaster", back_populates="investigation")