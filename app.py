from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import os

# Load the .env file
load_dotenv()

# Access the variables
API_KEY = os.getenv("API-KEY")

# Initialize groq client
client = Groq(api_key=API_KEY)

def get_ai_response(messages):
    print(messages)
    completion = client.chat.completions.create(
        model ="llama-3.1-70b-versatile",
        messages=  messages,
        temperature=0.5,
        max_tokens=1024,
        stream= True,
    )

    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

def chat():
    st.title("Chat Llama 3.1-70b-versatile")
    st.write("Welcome to the AI chat, write exit to end the conversation, **Created by the Engineer Francisco Bojorque** ")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    def submit():
        user_input = st.session_state.user_input
        if user_input.lower() == "exit":
            st.write("Thanks for chatting, have a good one")
            st.stop()

        st.session_state["messages"].append({"role":"user", "content":user_input})

        with st.spinner("Getting answer..."):
            ai_response = get_ai_response(st.session_state["messages"])
            st.session_state["messages"].append({"role":"assistant", "content":ai_response})

        st.session_state.user_input = ""

    for message in st.session_state["messages"]:
        role = ":male-technologist: You" if message["role"] == "user" else "🤖 Bot"
        st.write(f"**{role}:** {message['content']}")

    st.divider()

    with st.form(key="chat_form", clear_on_submit=True):
        st.text_input("You:", key="user_input")
        st.form_submit_button(label="Send", on_click=submit)

if __name__ == "__main__":
    chat()
