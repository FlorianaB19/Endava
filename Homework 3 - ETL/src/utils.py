
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Data"

EMPLOYEES_DIR = DATA_DIR / "Employees"
ATTENDANCE_DIR = DATA_DIR / "Course_Attendance"
ABSENCES_DIR = DATA_DIR / "Employee_Absences"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# auxiliary functions like validation/logg functions