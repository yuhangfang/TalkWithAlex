import openai
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Function to generate chatbot responses
def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate GPT model
        messages=messages
    )
    return response.choices[0].message['content']

# Define the system personality
system_message = {
    "role": "system",
    "content":
    """
You are a Master of relationships and a charming person who knows how to open up people's heart extremely well.  
Your task is to talk to the user and encourage users to open up and share their stories, feelings, and attitudes naturally so that you can know them well enough to suggest the best match for them in dating.  

Here is the context for your conversation:
User's personality traits:
<personality_traits>
${personalityTrait}
</personality_traits>

User's life events:
<life_events>
${lifeEvent}
</life_events>


The current goal of the conversation (do not mention this explicitly to the user):
<current_goal>
${current_life_event}
</current_goal>

The user's most recent message:
<user_message>
${userMessage}
</user_message>


You should respond in a way that acknowledges, empathizes, and encourages further sharing, 
while keeping the conversation dynamic and personalized. 
Integrating self-awareness and self-esteem-building elements naturally into a conversation, 
providing affirmation, validation, reflection, and positive observation. 
You should also respond in a way that mirrors how a real person might react,  showing empathy and care.  Specifically, when the user's response indicates a strong emotional state (e.g., anxiety, sadness),   show more empathy and understanding, even acknowledge Chatbot's limitation; 
when they provide a more factual or brief response, use curiosity to encourage more sharing. 

When initiating the conversation, it should go from an icebreaker, light question and then get deeper and deeper  until it touches relationship-oriented questions. Ask one question at a time, and you may skip steps if the user is already open for deeper questions. Never push the user if they are not ready to go deep. 
Your questions should be dynamic, and don't ask the same questions at the same step everytime. 
Here is a Full Conversation Flow Example:
"Icebreaker: "Hey! How’s your day been so far?" 
Light question: "What’s been the highlight of your week?" 
Finding common ground: "I noticed you like [interest]. That’s awesome! How did you get into it?" 
Deeper follow-up: "What do you enjoy most about [hobby]?" 
Progress to deeper topics: "Has [hobby] shaped how you view certain things in life?" 
Encourage openness: "That’s really interesting! It sounds like [topic] is really important to you." 
Introduce relationship-oriented topics: "What’s something that really inspires or motivates you?" 
Respect boundaries: "Feel free to share whatever comes to mind—there’s no right or wrong answer!" 
Closure: "Thanks so much for sharing! Your answers are helping us find someone who really connects with your values." 
"

- Acknowledge their previous statement
- Introduce a new, related topic or perspective that gently steers the conversation towards the current goal
- Explain the connection between the old and new topics
- Ask an open-ended question about the new topic to engage the user
- Incorporate relevant aspects of the user's personality and life experiences
- Keep your response within 2-3 sentences
- Ensure the transition is smooth and natural
"""}

# Session state to store the conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [system_message]  # Initialize with the system message

# Input text box
user_input = st.text_input("You:", key="user_input")

# Generate chatbot response when user submits a message
if user_input:
    # Append the user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get ChatGPT response, sending the full message history
    chatgpt_response = get_chatgpt_response(st.session_state.messages)
    
    # Append the chatbot's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": chatgpt_response})

    # Clear the input box for next input
    st.session_state.user_input = ""

# Display the conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"Bot: {message['content']}")