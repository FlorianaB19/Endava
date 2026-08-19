import pandas as pd


COMPARISON_TRAITS = {
    "Match Score": "match_score",
    "Size": "calculated_size",
    "Average Weight (kg)": "average_weight",
    "Energy Level": "Energy Level",
    "Barking Level": "Barking Level",
    "Trainability": "Trainability Level",
    "Adaptability": "Adaptability Level",
    "Playfulness": "Playfulness Level",
    "Openness to Strangers": "Openness To Strangers",
    "Good with Children": "Good With Young Children",
    "Good with Other Dogs": "Good With Other Dogs",
}


def format_value(label, value):
    """
    Format breed data for the comparison table.
    """

    if value is None:
        return "N/A"

    if label == "Match Score":
        return f"{value}%"

    if label == "Size":
        return str(value).title()

    if label == "Average Weight (kg)":
        try:
            return f"{float(value):.1f}"
        except (TypeError, ValueError):
            return str(value)

    if label in {
        "Energy Level",
        "Barking Level",
        "Trainability",
        "Adaptability",
        "Playfulness",
        "Openness to Strangers",
        "Good with Children",
        "Good with Other Dogs",
    }:
        try:
            return f"{int(float(value))}/5"
        except (TypeError, ValueError):
            return str(value)

    return str(value)


def build_comparison_dataframe(recommendations):
    """
    Create a comparison table using only the breed information
    already retrieved from the project's dataset.
    """

    if not recommendations:
        return pd.DataFrame()

    comparison_data = {}

    for dog in recommendations:

        breed_name = dog.get(
            "breed",
            "Unknown Breed",
        )

        breed_values = []

        for label, key in COMPARISON_TRAITS.items():

            value = dog.get(key)

            breed_values.append(
                format_value(
                    label,
                    value,
                )
            )

        comparison_data[breed_name] = breed_values

    return pd.DataFrame(
        comparison_data,
        index=COMPARISON_TRAITS.keys(),
    )