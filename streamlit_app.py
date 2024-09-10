from openai import OpenAI
import streamlit as st

# Sidebar for API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# Chat title and description
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Define system message for personality
system_message = {
    "role": "system",
    "content": "You are an empathetic and friendly assistant. You help users with their questions in a thoughtful and supportive manner."
}

# Initialize message history with system personality if it's not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [system_message]

# Display all messages in the conversation
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Append user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get response from OpenAI API, including the system message and conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=st.session_state.messages
    )
    
    # Extract assistant's message and append to the conversation history
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    # Display assistant's message
    st.chat_message("assistant").write(msg)
