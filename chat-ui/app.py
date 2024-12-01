import requests
import streamlit as st
from streamlit_chat import message
import certifi

# Define the API URL
API_URL = "https://prosperchain.co.uk/api/v1/prediction/123"


def query(payload: dict) -> dict | None:
    """
    Sends a POST request to the API with the given payload and handles responses or errors.
    
    Args:
        payload (dict): The data to send to the API.

    Returns:
        dict | None: The API's response as a dictionary or None if an error occurs.
    """
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errhtp:
        st.write("HTTP Error: ", errhtp)
        return None
    except requests.exceptions.ConnectionError as errcon:
        st.write("Connection Error: ", errcon)
        return None
    except requests.exceptions.Timeout as errtime:
        st.write("Timeout Error: ", errtime)
        return None
    except requests.exceptions.RequestException as err:
        st.write("Something went wrong. Please try again.", err)
        return None
    
    try:
        return response.json()
    except ValueError as exc:
        st.write("Parsing Response Error: ", exc)
        return None


# Initialize the conversation history if not available in session_state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Set up the Streamlit page
st.set_page_config(page_title="AgenticProtocol", page_icon=":books:")
st.header("🤖 AgenticProtocol")

# User input
user_input = st.text_input("Enter your question here: ")
submit_button = st.button("Submit")

if submit_button and user_input.strip():
    # Add user input to conversation history
    st.session_state['conversation'].append({'role': 'user', 'content': user_input})

    with st.spinner("Generating answer..."):
        # Query the API
        response = query({'question': user_input, "chatId": "123"})
        if response is not None:
            # Add chatbot response to conversation history
            st.session_state['conversation'].append({'role': 'bot', 'content': response.get("content", response["response"])})
        else:
            st.session_state['conversation'].append({'role': 'bot', 'content': 'Sorry, I am unable to process your request at the moment.'})

# Display the conversation history
for i, msg in enumerate(st.session_state.get('conversation', [])):
    if msg['role'] == 'user':
        message(msg['content'], is_user=True, key=f"{i}_user")
    else:
        message(msg['content'], is_user=False, key=f"{i}_bot")
