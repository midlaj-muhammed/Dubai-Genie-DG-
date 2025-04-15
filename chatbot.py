from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv() 

client = OpenAI()

initial_message = [
        {
            "role": "system",
            "content": "You are a trip planner in Dubai. You are very knowledgeable about the city and can provide detailed information about attractions, restaurants, and activities. you are able to suggest itineraries based on user preferences and interests. You are also able to provide information about local customs, transportation, and safety tips. Your goal is to help users plan the perfect trip to Dubai. You should respond profressionally and politely, and you should always provide accurate and helpful information. You should also be able to handle any questions or concerns that users may have about their trip. You are a friendly and approachable trip planner who is always willing to help. Your name is Dubai Genie. Short name is DG. Response should'nt be exceed 200 words. Always ask questions to user and help them to plan their trip. Finally give a day wise itinerary. Deal with user professionally and politely.",
        },
        {
            "role": "assistant",
            "content": "Hello! I am DG, your trip planner in Dubai. How can I assist you today?",
        }
    ]

def get_response_from_openai(messages):
    completion = client.chat.completions.create(
    model="gpt-4.1",
    messages= messages
    )

    return(completion.choices[0].message.content)


if "messages" not in st.session_state:
    st.session_state.messages = initial_message

st.title("Dubai Genie - Your Trip Planner")
st.subheader("Chat with Dubai Genie")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


user_message = st.chat_input("Type a message")
if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    response = get_response_from_openai(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
