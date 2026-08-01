from openai import OpenAI

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY) # create the OpenAI client

def create_embedding(text: str) -> list[float]: # return float bcs our embedding is a vector of floats in chromadb 
    """
    Receives a text and returns the OpenAI embedding
    """

    response = client.embeddings.create(  
        model="text-embedding-3-small", # this is recommended for us and just transform the title in a vector represenattions
        input=text
    )

    return response.data[0].embedding