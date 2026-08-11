import json
from datetime import datetime
from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

FEEDBACK_FILE = (
    BASE_DIR
    / "data"
    / "feedback.jsonl"
)


def save_feedback(
    question: str,
    answer: str,
    rating: str
):
    """
    Saves user feedback as JSON Lines.
    """

    feedback = {
        "timestamp": (
            datetime
            .now()
            .isoformat()
        ),
        "question": question,
        "answer": answer,
        "rating": rating
    }

    with open(
        FEEDBACK_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                feedback,
                ensure_ascii=False
            )
            + "\n"
        )