def transform_data(members, attendance, absences):

    # CLEAN DATA
    members["Name"] = members["Name"].str.strip()
    attendance["Name"] = attendance["Name"].str.strip()
    absences["Required Attendees"] = (
        absences["Required Attendees"]
        .astype(str)
        .str.strip()
    )

    # REMOVE DUPLICATES
    attendance.drop_duplicates(inplace=True)


    # KEEP ONLY REQUIRED COLUMNS
    attendance = attendance[
        [
            "Name",
            "Email",
            "In-Meeting Duration",
            "Session"
        ]
    ]

    # COUNT ATTENDED SESSIONS
    attendance_summary = (
        attendance
        .groupby("Name")
        .agg(
            Sessions_Attended=("Session", "count")
        )
        .reset_index()
    )

    # MERGE MEMBERS + ATTENDANCE
    result = members.merge(
        attendance_summary,
        on="Name",
        how="left"
    )


    # FILL NULL VALUES
    result["Sessions_Attended"] = (
        result["Sessions_Attended"]
        .fillna(0)
        .astype(int)
    )

 
    # CREATE STATUS
    result["Status"] = result["Sessions_Attended"].apply(
        lambda x: "Present" if x > 0 else "Absent"
    )

    # JUSTIFIED / UNJUSTIFIED ABSENCE
    justified_absences = set(
        absences["Required Attendees"]
    )

    def get_absence_type(row):

        if row["Status"] == "Present":
            return "Present"

        if row["Name"] in justified_absences:
            return "Justified"

        return "Unjustified"

    result["Absence_Type"] = result.apply(
        get_absence_type,
        axis=1
    )

    return result