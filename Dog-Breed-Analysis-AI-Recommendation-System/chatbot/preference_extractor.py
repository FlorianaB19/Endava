from typing import Optional, Literal

from pydantic import BaseModel

from chatbot.openai_client import (
    get_openai_client,
    get_model_name,
)
from chatbot.prompts import PREFERENCE_EXTRACTION_PROMPT


class UserPreferences(BaseModel):
    preferred_size: Optional[
        Literal["small", "medium", "large"]
    ] = None

    energy_level: Optional[int] = None
    barking_level: Optional[int] = None
    trainability: Optional[int] = None
    adaptability: Optional[int] = None
    playfulness: Optional[int] = None
    openness_to_strangers: Optional[int] = None
    good_with_children: Optional[int] = None
    good_with_other_dogs: Optional[int] = None

    size_importance: Optional[int] = None
    energy_importance: Optional[int] = None
    barking_importance: Optional[int] = None
    trainability_importance: Optional[int] = None
    adaptability_importance: Optional[int] = None
    playfulness_importance: Optional[int] = None


def extract_preferences(user_message: str) -> UserPreferences:
    """
    Extract structured dog preferences from the latest user message.
    """

    client = get_openai_client()

    response = client.responses.parse(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": PREFERENCE_EXTRACTION_PROMPT,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        text_format=UserPreferences,
    )

    return response.output_parsed


def merge_preferences(
    current_preferences: dict,
    new_preferences: UserPreferences,
) -> dict:
    """
    Merge newly extracted preferences with the existing profile.

    New explicitly detected values replace older values.
    Missing values do not erase previously known preferences.
    """

    merged = current_preferences.copy()

    new_data = new_preferences.model_dump()

    for key, value in new_data.items():
        if value is not None:
            merged[key] = value

    return merged


def get_missing_core_preferences(preferences: dict) -> list[str]:
    """
    Return important information that is still missing.
    """

    core_fields = [
        "preferred_size",
        "energy_level",
        "barking_level",
        "trainability",
    ]

    return [
        field
        for field in core_fields
        if preferences.get(field) is None
    ]


def has_enough_information(preferences: dict) -> bool:
    """
    Decide whether enough information is available
    to generate useful recommendations.
    """

    core_fields = [
        "preferred_size",
        "energy_level",
        "barking_level",
        "trainability",
    ]

    known_values = sum(
        preferences.get(field) is not None
        for field in core_fields
    )

    return known_values >= 3


def get_clarifying_question(preferences: dict) -> str:
    """
    Ask one useful follow-up question based on missing information.
    """

    missing = get_missing_core_preferences(preferences)

    questions = {
        "preferred_size": (
            "Do you prefer a small, medium, or large dog?"
        ),
        "energy_level": (
            "How active are you on a typical day? "
            "Would you prefer a low-energy, moderately active, "
            "or very energetic dog?"
        ),
        "barking_level": (
            "How important is it for you to have a quiet dog "
            "that does not bark very much?"
        ),
        "trainability": (
            "Would you prefer a dog that is relatively easy to train, "
            "or is trainability not very important to you?"
        ),
    }

    if missing:
        return questions[missing[0]]

    return (
        "Could you tell me a little more about the type of dog "
        "you would enjoy living with?"
    )