import pandas as pd
from src.utils import EMPLOYEES_DIR, ATTENDANCE_DIR, ABSENCES_DIR


def extract_members():
    return pd.read_csv(EMPLOYEES_DIR / "members.csv")


def extract_absences():
    return pd.read_excel(ABSENCES_DIR / "absente_confluence.xlsx")


def extract_attendance():

    attendance_files = list(
        ATTENDANCE_DIR.glob("Dava.X Academy*.csv")
    )

    attendance_list = []

    for file in attendance_files:

        df = pd.read_csv(
            file,
            encoding="utf-16",
            sep="\t",
            skiprows=9
        )

        df["Session"] = file.stem

        attendance_list.append(df)

    return pd.concat(
        attendance_list,
        ignore_index=True
    )