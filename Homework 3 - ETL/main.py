from src.extract import (
    extract_members,
    extract_absences,
    extract_attendance
)

from src.transform import transform_data
from src.load import load_report


print("=" * 50)
print("EXTRACT")
print("=" * 50)

members = extract_members()
attendance = extract_attendance()
absences = extract_absences()

print(f"Members loaded: {len(members)}")
print(f"Attendance records: {len(attendance)}")
print(f"Absences loaded: {len(absences)}")

print("\n" + "=" * 50)
print("TRANSFORM")
print("=" * 50)

result = transform_data(
    members,
    attendance,
    absences
)

print(result.head())

print("\n" + "=" * 50)
print("LOAD")
print("=" * 50)

load_report(result)

print("\nETL Process completed successfully!")

# for ochestrations