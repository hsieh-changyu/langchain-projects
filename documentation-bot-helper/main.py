from typing import Set

from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

# Page Configuration
st.set_page_config(
    page_title="Pinecone Document Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
with st.sidebar:
    st.image(
        "https://media.licdn.com/dms/image/sync/v2/D4E18AQEM--GBUdUPJw/companyUpdate-article-image-shrink_200_200/companyUpdate-article-image-shrink_200_200/0/1667186040534/icons-semantic-searchpng?e=1738800000&v=beta&t=UTEEDYm7PHgqAD3Bie_EYkkeXzjRG-KFQbNVXeBPuA4"
    )
    st.write("Welcome to the self-hosting Pinecone Documentation Helper Bot.")
    st.markdown(
        "This bot helps you find relevant information from documentation efficiently."
    )
    st.markdown("---")
    st.info("Tip: Enter a clear and concise query for better results!")

# Main Header
st.title("Pinecone - Documentation Helper Bot")
st.markdown(
    """
    **Welcome!** This chatbot is powered by <img src="https://miro.medium.com/v2/resize:fit:640/format:webp/0*puT7vGWrtcbaD6VY.png" alt="LangChain Logo" width="100" style="display:inline-block;">
    and helps you interact with documentation efficiently. Type your query below to get started.
    """,
    unsafe_allow_html=True,
)


# Initialize Session State
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Helper Function
def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = sorted((source_urls))
    sources_string = "Sources:\n" + "\n".join(
        [f"{i+1}. {url}" for i, url in enumerate(sources_list)]
    )
    return sources_string


# Display Chat History
# if st.session_state["chat_answers_history"]:
#     for user_query, ai_response in zip(
#         st.session_state["user_prompt_history"],
#         st.session_state["chat_answers_history"],
#     ):
#         st.markdown(
#             f"<div class='user-message'>{user_query}</div>", unsafe_allow_html=True
#         )
#         st.markdown(
#             f"<div class='bot-message'>{ai_response}</div>", unsafe_allow_html=True
#         )

# User Input (Dynamic Input Box)
prompt = st.text_input(
    "Ask a question",
    placeholder="Enter your question here...",
    label_visibility="visible",
)

# Chat Logic
if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        # sources = set(doc.metadata["source"] for doc in generated_response["context"])
        sources = [
            doc.metadata.get("source")
            for doc in generated_response["context"]
            if doc.metadata.get("source") is not None
        ]
        print(sources)
        formatted_response = (
            f"{generated_response['answer']} \n\n{create_sources_string(sources)}"
        )
        # Update session state
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["answer"]))

# Display Chat History
if st.session_state["chat_answers_history"]:
    for user_query, ai_response in zip(
        st.session_state["user_prompt_history"],
        st.session_state["chat_answers_history"],
    ):
        message(user_query, is_user=True, avatar_style="croodles")
        message(ai_response, avatar_style="initials", seed="AI")
