import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_openai_client():
    """
    Create and return an OpenAI client using the API key
    stored in the .env file.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. "
            "Please add it to your .env file."
        )

    return OpenAI(api_key=api_key)


def get_model_name():
    """
    Return the OpenAI model configured in the environment.
    """

    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")