from io import BytesIO

from openai import OpenAI

from config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def speech_to_text(audio_bytes: bytes) -> str:
    """
    Converts recorded audio into text using OpenAI Speech-to-Text.
    """

    audio_file = BytesIO(audio_bytes)

    # OpenAI needs a filename/extension for the uploaded audio file.
    audio_file.name = "recording.wav"

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file
    )

    return transcription.text


def text_to_speech(text: str) -> bytes:
    """
    Converts text into spoken audio using OpenAI Text-to-Speech.
    """

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    return response.read()



if __name__ == "__main__":

    text = (
        "Hello! Welcome to Smart Librarian. "
        "I can help you find your next book."
    )

    audio = text_to_speech(text)

    with open("test_audio.mp3", "wb") as file:
        file.write(audio)

    print("Audio generated successfully.")