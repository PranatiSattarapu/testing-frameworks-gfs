import streamlit as st
from drive_manager import list_data_files
from workflow import generate_response

# --- Streamlit Configuration ---
st.set_page_config(page_title="Health Tutor Console", layout="wide")
st.title("Prompt Refinement Console")

# --- Initialize Session State ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {"Session 1": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Session 1"

# --- Sidebar: Document Management (Read-Only) ---
st.sidebar.header("📂 Current Document Context")

files = list_data_files()

if not files:
    st.sidebar.info("No documents found in the shared folder yet.")
else:
    st.sidebar.markdown("**Documents informing the context:**")
    for f in files:
        st.sidebar.markdown(f"📄 " + f["name"])

st.divider()

# --- Main Area: Chat Interface ---
# --- Main Chat Interface ---

active_messages = st.session_state.sessions[st.session_state.current_session]

# 1️⃣ CHAT MESSAGES (always on top)
for message in active_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 2️⃣ QUICK QUESTIONS (always ABOVE chat input)
st.markdown("### Quick Questions")

preset_questions = [
    "Prepare me for my doctor's visit",
    "What's my health summary?",
    "What should I ask my doctor?",
    "Summarize my recent metrics",
]

cols = st.columns(len(preset_questions))

if "preset_query" not in st.session_state:
    st.session_state.preset_query = None

for i, q in enumerate(preset_questions):
    if cols[i].button(q, key=f"preset_{i}"):
        st.session_state.preset_query = q
        st.rerun()


# 3️⃣ CHAT INPUT (always at the bottom)
chat_input = st.chat_input("Enter your medical question:")

# Decide final query
query = None
if st.session_state.preset_query:
    query = st.session_state.preset_query
    st.session_state.preset_query = None
elif chat_input:
    query = chat_input


# 4️⃣ PROCESS QUERY
if query:
    active_messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Claude is thinking..."):
            answer = generate_response(query)

        st.markdown(answer)

    active_messages.append({"role": "assistant", "content": answer})
    st.session_state.sessions[st.session_state.current_session] = active_messages
