from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.config.database import Base


class ChargesheetMaster(Base):
    __tablename__ = "chargesheet_master"

    chargesheet_id = Column(String, primary_key=True)

    case_id = Column(
        String,
        ForeignKey("case_master.case_id"),
        nullable=False,
        unique=True,
    )

    court_id = Column(String)

    court_name = Column(String)

    filing_date = Column(DateTime)

    filing_officer_id = Column(String)

    chargesheet_status = Column(String)

    case = relationship("CaseMaster", back_populates="chargesheet")