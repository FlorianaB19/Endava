from pathlib import Path

import pandas as pd

from chatbot.preference_extractor import UserPreferences


#dataset configurations

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "date_out" / "date.csv"


COLUMN_MAP = {
    "breed": "Breed",
    "energy_level": "Energy Level",
    "barking_level": "Barking Level",
    "trainability": "Trainability Level",
    "adaptability": "Adaptability Level",
    "playfulness": "Playfulness Level",
    "openness_to_strangers": "Openness To Strangers",
    "good_with_children": "Good With Young Children",
    "good_with_other_dogs": "Good With Other Dogs",
}


IMPORTANCE_MAP = {
    "energy_level": "energy_importance",
    "barking_level": "barking_importance",
    "trainability": "trainability_importance",
    "adaptability": "adaptability_importance",
    "playfulness": "playfulness_importance",
}


#data laodings
def load_dog_data():
    """
    Load the processed dog breed dataset.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dog dataset was not found at: {DATASET_PATH}"
        )

    return pd.read_csv(DATASET_PATH)


#trait similarity

def calculate_trait_similarity(actual, desired):
    """
    Compare two values on the 1-5 trait scale.

    1.00 = perfect match
    0.75 = one point difference
    0.50 = two point difference
    0.25 = three point difference
    0.00 = maximum difference
    """

    try:
        actual = float(actual)
        desired = float(desired)
    except (TypeError, ValueError):
        return None

    if pd.isna(actual) or pd.isna(desired):
        return None

    difference = abs(actual - desired)

    return max(
        0.0,
        1.0 - difference / 4.0,
    )


#dog size

def get_average_weight(row):
    """
    Calculate average breed weight.
    """

    try:
        min_weight = float(row["min_weight"])
        max_weight = float(row["max_weight"])
    except (KeyError, TypeError, ValueError):
        return None

    if pd.isna(min_weight) or pd.isna(max_weight):
        return None

    return (min_weight + max_weight) / 2


def determine_size(row):
    """
    Determine dog size using average weight.

    Small  -> <= 10 kg
    Medium -> > 10 kg and <= 25 kg
    Large  -> > 25 kg
    """

    weight = get_average_weight(row)

    if weight is None:
        return None

    if weight <= 10:
        return "small"

    if weight <= 25:
        return "medium"

    return "large"


def calculate_size_similarity(
    row,
    preferred_size,
):
    """
    Compare breed size with the user's preferred size.
    """

    if preferred_size is None:
        return None

    actual_size = determine_size(row)

    if actual_size is None:
        return None

    if actual_size == preferred_size:
        return 1.0

    sizes = [
        "small",
        "medium",
        "large",
    ]

    actual_index = sizes.index(actual_size)
    preferred_index = sizes.index(preferred_size)

    difference = abs(
        actual_index - preferred_index
    )

    if difference == 1:
        return 0.5

    return 0.0



#importance weights

def get_trait_weight(
    preferences,
    trait_name,
):
    """
    Return preference importance.

    1 = Nice to have
    2 = Important
    3 = Very important
    """

    importance_field = IMPORTANCE_MAP.get(
        trait_name
    )

    if importance_field is None:
        return 2

    importance = getattr(
        preferences,
        importance_field,
        None,
    )

    if importance is None:
        return 2

    return max(
        1,
        min(3, int(importance)),
    )


def get_size_weight(preferences):
    """
    Return size preference importance.
    """

    importance = getattr(
        preferences,
        "size_importance",
        None,
    )

    if importance is None:
        return 2

    return max(
        1,
        min(3, int(importance)),
    )


#recomandation engine

def recommend_breeds(
    preferences: UserPreferences,
    top_n: int = 3,
):
    """
    Recommend dog breeds using weighted similarity.

    OpenAI does not select the breeds here.
    Ranking is calculated using the local dataset.
    """

    df = load_dog_data()

    trait_preferences = {
        "energy_level": preferences.energy_level,
        "barking_level": preferences.barking_level,
        "trainability": preferences.trainability,
        "adaptability": preferences.adaptability,
        "playfulness": preferences.playfulness,
        "openness_to_strangers": (
            preferences.openness_to_strangers
        ),
        "good_with_children": (
            preferences.good_with_children
        ),
        "good_with_other_dogs": (
            preferences.good_with_other_dogs
        ),
    }

    results = []


#calculate score for each breed

    for index, row in df.iterrows():

        score_details = {}

        weighted_scores = []
        total_weight = 0

#numeric traits

        for trait_name, desired_value in (
            trait_preferences.items()
        ):

            if desired_value is None:
                continue

            column = COLUMN_MAP.get(
                trait_name
            )

            if (
                column is None
                or column not in df.columns
            ):
                continue

            similarity = (
                calculate_trait_similarity(
                    row[column],
                    desired_value,
                )
            )

            if similarity is None:
                continue

            weight = get_trait_weight(
                preferences,
                trait_name,
            )

            weighted_scores.append(
                similarity * weight
            )

            total_weight += weight

            score_details[trait_name] = {
                "score": round(
                    similarity * 100,
                    1,
                ),
                "importance": weight,
                "desired_value": desired_value,
                "actual_value": row[column],
            }

#size
        if preferences.preferred_size is not None:

            size_similarity = (
                calculate_size_similarity(
                    row,
                    preferences.preferred_size,
                )
            )

            if size_similarity is not None:

                size_weight = (
                    get_size_weight(
                        preferences
                    )
                )

                weighted_scores.append(
                    size_similarity
                    * size_weight
                )

                total_weight += size_weight

                score_details["size"] = {
                    "score": round(
                        size_similarity * 100,
                        1,
                    ),
                    "importance": size_weight,
                    "desired_value": (
                        preferences.preferred_size
                    ),
                    "actual_value": (
                        determine_size(row)
                    ),
                }


# skip if no comparable data

        if (
            not weighted_scores
            or total_weight == 0
        ):
            continue


#final weighted score

        overall_score = (
            sum(weighted_scores)
            / total_weight
        )

        results.append(
            {
                "index": index,
                "match_score": overall_score,
                "score_details": score_details,
            }
        )

#sort best matches first

    results.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

#final recomandation

    recommendations = []

    for result in results[:top_n]:

        row = df.loc[
            result["index"]
        ]

        breed_data = {
            "breed": row["Breed"],

            "match_score": round(
                result["match_score"] * 100,
                1,
            ),

            "score_details": (
                result["score_details"]
            ),

            "calculated_size": (
                determine_size(row)
            ),

            "average_weight": (
                get_average_weight(row)
            ),
        }

        # Include the original dataset information
        # so OpenAI can explain recommendations
        # using grounded data.

        for column in df.columns:

            value = row[column]

            if pd.isna(value):
                continue

            breed_data[column] = value

        recommendations.append(
            breed_data
        )

    return recommendations