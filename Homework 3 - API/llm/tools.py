import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # directory of the project
                                                  # __file__ is the current location
                                                  # resolve() gives the absolute path 
                                                  # parent = smart-librarian/llm/tools.py 
                                                  # parent.parent = smart-librarian

BOOKS_JSON = BASE_DIR / "data" / "book_summaries.json" # path to the json file

with open(BOOKS_JSON, "r", encoding="utf-8") as f: 
    BOOK_SUMMARIES = json.load(f) # transform the json file into a python dictionary


def get_summary_by_title(title: str) -> str:
    return BOOK_SUMMARIES.get(title,
        "Sorry, I couldn't find a summary for this book." # return the summary if the title exists 
    )


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Returns the detailed summary of a recommended book.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Exact title of the recommended book"
                    }
                },
                "required": ["title"]
            }
        }
    }
]