import os

from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# read the key    read the value 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the key exists
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found, so check the .env file"
    )