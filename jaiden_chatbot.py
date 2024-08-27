# jaiden_chatbot.py
import streamlit as st
import openai
import time
import os

# Setup Page
st.set_page_config(page_title="Jaiden Chatbot", page_icon = ":school:", layout="wide")
ASSISTANT_ID = "asst_EuaJrNvnmaWnl5xSVlAyx1wy"
THREAD_ID = "thread_YCfmhdqnyweBBRRwJliBG1bJ"

# Openai Client
api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error('OpenAi API Key was not found. Please set it in Streamlit secrets or as an enviromental varible')
    st.stop()
client = openai.OpenAI(api_key=api_key)

# Creating Chat
st.image('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/0a290752-d7eb-45e3-aa31-8e71b544cde0/delg895-160a4606-e9ba-4c93-8278-8cebdeb269ba.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzBhMjkwNzUyLWQ3ZWItNDVlMy1hYTMxLThlNzFiNTQ0Y2RlMFwvZGVsZzg5NS0xNjBhNDYwNi1lOWJhLTRjOTMtODI3OC04Y2ViZGViMjY5YmEuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.4cwQHbWwfiPYfJbvL-Dn6s-6xKGdSdzPbkw_UtGW3AM')
st.title("Jaiden Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []

# responses
def get_assistant_response(assistant_id,thread_id, user_input):
    try:
        # user message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
            )

        # Thinking
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
            )
        
        # Waiting
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)

        # Responses
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        # Latest Response
        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f'Error getting assistant reponse: {str(e)}')
        return "I'm sorry, but an error occurred while processing your request."

# Displaying Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User And Ai responses
prompt = st.chat_input("Ask me anything!")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_assistant_response(
            ASSISTANT_ID,
            THREAD_ID,
            prompt
            )
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role":"assistant","content":full_response})

# Display Id
st.sidebar.write(f'Assistant ID: {ASSISTANT_ID}')
st.sidebar.write(f'Thread ID: {THREAD_ID}')
