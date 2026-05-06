import streamlit as st
import asyncio
import json
import os
from dotenv import load_dotenv
from agent_logic import process_query

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="AI Agent", layout="centered")

st.title("🤖 AI Agent")


# Configuration from Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.3-70b-versatile"

# Initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = []
if "viewing_index" not in st.session_state:
    st.session_state.viewing_index = None

# Sidebar for History (ChatGPT style)
with st.sidebar:
    # Most prominent action at the top
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.viewing_index = None
        st.rerun()
    
    st.divider()
    st.subheader("Recent")
    
    if st.session_state.history:
        # Scrollable list of buttons
        for i, chat in enumerate(reversed(st.session_state.history)):
            # Use the first few words as a keyword/title
            words = chat['input'].split()
            title = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
            
            # Real index in the original list
            real_idx = len(st.session_state.history) - 1 - i
            
            # Highlight the active chat
            is_active = st.session_state.viewing_index == real_idx
            if st.button(f"💬 {title}", key=f"nav_{real_idx}", use_container_width=True):
                st.session_state.viewing_index = real_idx
                st.rerun()
        
        st.divider()
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.history = []
            st.session_state.viewing_index = None
            st.rerun()
    else:
        st.info("No recent searches.")

# Main Chat Interface
if not GROQ_API_KEY:
    st.error("Missing `GROQ_API_KEY` environment variable. Please set it in a `.env` file.")
    st.stop()

# Determine what to display
display_chat = None
if st.session_state.viewing_index is not None and st.session_state.viewing_index < len(st.session_state.history):
    display_chat = st.session_state.history[st.session_state.viewing_index]
elif st.session_state.history:
    # Default to the most recent if nothing selected but history exists
    display_chat = st.session_state.history[-1]
    st.session_state.viewing_index = len(st.session_state.history) - 1

# Display the dialogue
if display_chat:
    with st.container():
        st.caption(f"Viewing: {display_chat['input'][:50]}...")
        with st.chat_message("user"):
            st.markdown(display_chat['input'])
        with st.chat_message("assistant"):
            st.markdown(display_chat.get("result", "No result found."))
            with st.expander("Technical Details (JSON)"):
                st.json(display_chat)
else:
    # Welcome screen
    with st.chat_message("assistant"):
        st.markdown("Hello! I'm your AI Agent. Ask me a math question or anything else to get started!")

# Input at the bottom
user_input = st.chat_input("Ask me something...")

if user_input:
    # Create a new search entry
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("Processing..."):
        response_json = asyncio.run(process_query(user_input, MODEL_NAME, GROQ_API_KEY, BASE_URL))
    
    # Update history and set as active view
    st.session_state.history.append(response_json)
    if len(st.session_state.history) > 10: # Increased history limit
        st.session_state.history = st.session_state.history[-10:]
    
    st.session_state.viewing_index = len(st.session_state.history) - 1
    st.rerun()

