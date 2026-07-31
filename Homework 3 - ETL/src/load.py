
from src.utils import OUTPUT_DIR

def load_report(result):

    output_file = OUTPUT_DIR / "Attendance_Final_Report.xlsx"

    result.to_excel(
        output_file,
        index=False
    )

    print(f"Report saved successfully!")
    print(f"Location: {output_file}")


#here we save the results