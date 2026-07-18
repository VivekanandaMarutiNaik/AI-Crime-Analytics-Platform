from backend.config.database import Base, engine

# Import all models
from backend.models.case_master import CaseMaster
from backend.models.victim_master import VictimMaster
from backend.models.accused_master import AccusedMaster
from backend.models.investigation_master import InvestigationMaster
from backend.models.arrest_master import ArrestMaster
from backend.models.chargesheet_master import ChargesheetMaster
from backend.models.employee_master import EmployeeMaster
from backend.models.cctv_master import CCTVMaster
from backend.models.occurrence_master import OccurrenceMaster


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully.")


if __name__ == "__main__":
    create_tables()