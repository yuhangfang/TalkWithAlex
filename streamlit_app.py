import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
description = """
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
"""
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": description, "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
