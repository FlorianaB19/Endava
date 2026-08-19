import json

from chatbot.openai_client import (
    get_openai_client,
    get_model_name,
)

from chatbot.prompts import RESPONSE_GENERATION_PROMPT


def generate_recommendation_response(
    user_message,
    preferences,
    recommendations,
):
    """
    Generate a natural-language explanation using ONLY the
    breed information retrieved from the local dataset.
    """

    client = get_openai_client()

    context = {
        "original_user_message": user_message,
        "extracted_preferences": preferences.model_dump(),
        "candidate_breeds": recommendations,
    }

    response = client.responses.create(
        model=get_model_name(),
        instructions=RESPONSE_GENERATION_PROMPT,
        input=json.dumps(
            context,
            indent=2,
            default=str,
        ),
    )

    return response.output_text