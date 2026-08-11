import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

BOOKS_JSON = (
    BASE_DIR
    / "data"
    / "book_summaries.json"
)


with open(
    BOOKS_JSON,
    "r",
    encoding="utf-8"
) as file:

    BOOK_SUMMARIES = json.load(file)


def get_summary_by_title(title: str) -> str:
    """
    Returns the detailed summary for an exact book title.
    """

    return BOOK_SUMMARIES.get(
        title,
        "Sorry, no summary was found for this title."
    )


TOOLS = [
    {
        "type": "function",
        "function": {

            "name": "get_summary_by_title",

            "description": (
                "Returns the detailed summary "
                "of a recommended book."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "title": {
                        "type": "string",
                        "description": (
                            "Exact title of the "
                            "recommended book."
                        )
                    }
                },

                "required": [
                    "title"
                ],

                "additionalProperties": False
            }
        }
    }
]