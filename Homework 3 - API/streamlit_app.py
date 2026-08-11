import requests
import streamlit as st

from llm.audio import speech_to_text, text_to_speech
from utils.feedback import save_feedback



# CONFIGURATION


API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Smart Librarian",
    page_icon="📚",
    layout="wide",
)



# CUSTOM CSS

st.markdown(
    """
    <style>

        .main-title {
            font-size: 2.6rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1rem;
            color: #7a7a7a;
            margin-bottom: 1.5rem;
        }

        .info-card {
            padding: 1rem;
            border-radius: 16px;
            background: rgba(120, 120, 120, 0.08);
            border: 1px solid rgba(120, 120, 120, 0.18);
            margin-bottom: 1rem;
        }

        .example-card {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            background: rgba(120, 120, 120, 0.06);
            margin-bottom: 0.6rem;
        }

        .footer-note {
            font-size: 0.85rem;
            color: #888888;
            margin-top: 2rem;
        }

    </style>
    """,
    unsafe_allow_html=True,
)



# HEADER


st.markdown(
    '<div class="main-title">📚 Smart Librarian</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        AI-powered book recommendations using OpenAI GPT,
        RAG, ChromaDB, FastAPI, Streamlit and Voice AI.
    </div>
    """,
    unsafe_allow_html=True,
)



# BACKEND


def call_backend(question: str) -> dict:
    """
    Sends the user's question to FastAPI.

    The backend now returns:
    {
        "answer": "...",
        "retrieved_books": [...]
    }
    """

    response = requests.post(
        API_URL,
        json={"question": question},
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    if "answer" not in data:
        raise ValueError(
            "The backend response does not contain 'answer'."
        )

    if "retrieved_books" not in data:
        raise ValueError(
            "The backend response does not contain 'retrieved_books'."
        )

    # IMPORTANT:
    # We return the complete JSON response,
    # not only data["answer"].
    return data


# 
# RAG EXPLAINABILITY


def display_rag_explainability(retrieved_books: list):
    """
    Displays the books retrieved from ChromaDB
    and their vector distances.
    """

    with st.expander(
        "🔍 How was this recommendation found?"
    ):

        st.markdown(
            """
The recommendation was generated using **Retrieval-Augmented Generation (RAG)**.

**Step 1 — Embedding**

The user's question was converted into a numerical vector using the OpenAI embedding model.

**Step 2 — Vector Search**

ChromaDB compared the query vector with the vectors of the indexed books.

**Step 3 — Retrieval**

The most semantically relevant books were retrieved and provided to GPT as context.
"""
        )

        st.divider()

        st.markdown("### 📚 Retrieved Books")

        if not retrieved_books:
            st.warning(
                "No books passed the relevance threshold."
            )
            return

        for index, book in enumerate(
            retrieved_books,
            start=1
        ):

            st.markdown(
                f"""
**{index}. {book["title"]}**

Vector distance: `{book["distance"]}`
"""
            )

        st.divider()

        st.caption(
            "Lower vector distance means a stronger semantic match."
        )



# RESET CONVERSATION


def reset_conversation():

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋\n\n"
                "Tell me what kind of book you are looking for.\n\n"
                "You can type your question or use the microphone.\n\n"
                "For example: "
                "**I want a book about friendship and magic.**"
            ),
        }
    ]

    st.session_state.voice_question = None



# SESSION STATE


if "messages" not in st.session_state:
    reset_conversation()

if "voice_question" not in st.session_state:
    st.session_state.voice_question = None



# SIDEBAR

with st.sidebar:

    st.header("About the Project")

    st.markdown(
        """
        <div class="info-card">

        Smart Librarian combines semantic search,
        generative AI and voice technologies to recommend
        books from a local knowledge base.

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
- 🤖 OpenAI GPT
- 🧠 OpenAI Embeddings
- 🔍 Retrieval-Augmented Generation
- 📚 ChromaDB
- ⚡ FastAPI
- 💻 Streamlit
- 🛠️ Native Function Calling
- 🎤 Speech-to-Text
- 🔊 Text-to-Speech
"""
    )

    st.divider()

    st.subheader("Example Questions")

    examples = [
        "I want a fantasy book.",
        "Recommend a horror novel.",
        "I want a book about health.",
        "Recommend a personal development book.",
        "I am interested in science fiction.",
        "What is 1984 about?",
        "Recommend a romance novel.",
    ]

    for example in examples:

        st.markdown(
            f"""
            <div class="example-card">
                {example}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        reset_conversation()

        st.rerun()

    st.markdown(
        """
        <div class="footer-note">

        FastAPI backend:

        <code>http://127.0.0.1:8000</code>

        </div>
        """,
        unsafe_allow_html=True,
    )



# DISPLAY CHAT HISTORY


for index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        # Display message
        st.markdown(
            message["content"]
        )

        
        # RAG EXPLAINABILITY
        

        if message.get("retrieved_books") is not None:

            display_rag_explainability(
                message["retrieved_books"]
            )

        
        # TEXT TO SPEECH
        

        if (
            message["role"] == "assistant"
            and message.get("can_speak", False)
        ):

            if st.button(
                "🔊 Listen",
                key=f"listen_{index}",
            ):

                try:

                    with st.spinner(
                        "Generating audio..."
                    ):

                        audio_bytes = text_to_speech(
                            message["content"]
                        )

                    st.audio(
                        audio_bytes,
                        format="audio/mp3"
                    )

                except Exception as error:

                    st.error(
                        f"Text-to-Speech error: {error}"
                    )

        
        # USER FEEDBACK
        

        if (
            message["role"] == "assistant"
            and message.get("can_feedback", False)
        ):

            st.markdown(
                "#### Was this recommendation useful?"
            )

            feedback_col1, feedback_col2 = st.columns(2)

            # Check if feedback was already submitted
            feedback_given = message.get(
                "feedback_given",
                False
            )

            with feedback_col1:

                if st.button(
                    "👍 Yes",
                    key=f"positive_{index}",
                    disabled=feedback_given
                ):

                    save_feedback(
                        question=message["question"],
                        answer=message["content"],
                        rating="positive"
                    )

                    st.session_state.messages[index][
                        "feedback_given"
                    ] = True

                    st.session_state.messages[index][
                        "feedback"
                    ] = "positive"

                    st.rerun()

            with feedback_col2:

                if st.button(
                    "👎 No",
                    key=f"negative_{index}",
                    disabled=feedback_given
                ):

                    save_feedback(
                        question=message["question"],
                        answer=message["content"],
                        rating="negative"
                    )

                    st.session_state.messages[index][
                        "feedback_given"
                    ] = True

                    st.session_state.messages[index][
                        "feedback"
                    ] = "negative"

                    st.rerun()

            # Show confirmation after feedback
            if message.get("feedback") == "positive":

                st.success(
                    "👍 Thanks for your feedback!"
                )

            elif message.get("feedback") == "negative":

                st.info(
                    "👎 Thanks for your feedback!"
                )



# VOICE INPUT


st.divider()

st.subheader("🎤 Voice Mode")

st.caption(
    "Record your question and Smart Librarian "
    "will convert your voice into text."
)

audio_recording = st.audio_input(
    "Ask for a book using your voice"
)


if audio_recording is not None:

    current_audio = audio_recording.getvalue()

    audio_id = hash(current_audio)

    if (
        st.session_state.get("last_audio_id")
        != audio_id
    ):

        try:

            with st.spinner(
                "Transcribing your voice..."
            ):

                transcription = speech_to_text(
                    current_audio
                )

            transcription = transcription.strip()

            if transcription:

                st.session_state.voice_question = (
                    transcription
                )

                st.session_state.last_audio_id = (
                    audio_id
                )

                st.success(
                    "Voice transcription completed."
                )

        except Exception as error:

            st.error(
                f"Speech-to-Text error: {error}"
            )



# SHOW VOICE TRANSCRIPTION


if st.session_state.voice_question:

    st.info(
        "🎤 You said: "
        + st.session_state.voice_question
    )

    if st.button(
        "📚 Send voice question"
    ):

        st.session_state.pending_question = (
            st.session_state.voice_question
        )

        st.session_state.voice_question = None

        st.rerun()



# TEXT INPUT


typed_question = st.chat_input(
    "Describe the type of book you are looking for..."
)

if typed_question:

    st.session_state.pending_question = (
        typed_question
    )



# PROCESS QUESTION


if "pending_question" in st.session_state:

    question = (
        st.session_state
        .pop("pending_question")
        .strip()
    )

    if question:

        
        # User message
        

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        
        # Assistant response
        

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching ChromaDB and generating "
                "your recommendation..."
            ):

                try:

                    # IMPORTANT:
                    # call_backend now returns
                    # the complete API response.

                    result = call_backend(
                        question
                    )

                    answer = result["answer"]

                    retrieved_books = result[
                        "retrieved_books"
                    ]

                    
                    # Show answer
                    

                    st.markdown(answer)

                    
                    # Show RAG Explainability
                    

                    display_rag_explainability(
                        retrieved_books
                    )

                    
                    # Save complete assistant message
                    

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,

                            # Text-to-Speech
                            "can_speak": True,

                            # RAG Explainability
                            "retrieved_books": retrieved_books,

                            # Feedback
                            "can_feedback": True,
                            "feedback_given": False,
                            "feedback": None,

                            # Original user question
                            "question": question,
                        }
                    )

                    st.toast(
                        "Book recommendation generated successfully.",
                        icon="📚",
                    )

                    # Rerun so Listen and RAG details
                    # are persisted in the chat history.
                    st.rerun()


                
                # BACKEND OFFLINE
                

                except requests.exceptions.ConnectionError:

                    error_message = (
                        "Unable to connect to the "
                        "FastAPI backend.\n\n"
                        "Start the backend with:\n\n"
                        "`py -m uvicorn app:app --reload`"
                    )

                    st.error(
                        error_message
                    )


                
                # TIMEOUT
                

                except requests.exceptions.Timeout:

                    st.error(
                        "The request took too long. "
                        "Please try again."
                    )


                
                # HTTP ERROR
                

                except requests.exceptions.HTTPError as error:

                    try:

                        backend_detail = (
                            error.response
                            .json()
                            .get(
                                "detail",
                                "Unknown backend error."
                            )
                        )

                    except ValueError:

                        backend_detail = (
                            error.response.text
                        )

                    st.error(
                        f"Backend error: {backend_detail}"
                    )


                
                # OTHER ERRORS
                

                except Exception as error:

                    st.error(
                        f"Unexpected error: {error}"
                    )