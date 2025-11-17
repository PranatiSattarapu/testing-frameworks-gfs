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

# --- Main Chat Interface ---
active_messages = st.session_state.sessions[st.session_state.current_session]

# Containers
chat_container = st.container()      # history
bottom_container = st.container()    # quick questions + chat input

# ---------------- CHAT HISTORY ----------------
with chat_container:
    for message in active_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ---------------- BOTTOM AREA ----------------
with bottom_container:

    st.markdown("### Quick Questions")

    preset_questions = [
        "Prepare me for my doctor's visit",
        "What's my health summary?",
        "What should I ask my doctor?",
        "Summarize my recent metrics",
    ]

    cols = st.columns(len(preset_questions))

    # Track clicked preset question
    if "preset_query" not in st.session_state:
        st.session_state.preset_query = None

    for i, q in enumerate(preset_questions):
        if cols[i].button(q):
            st.session_state.preset_query = q
            st.rerun()

    # Always-visible chatbox
    chatbox_input = st.chat_input("Enter your medical question:")

# Decide final query
query = None

if st.session_state.preset_query:
    query = st.session_state.preset_query
    st.session_state.preset_query = None  # reset after use
elif chatbox_input:
    query = chatbox_input

# ---------------- PROCESS QUERY ----------------
if query:
    # Add user message
    active_messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("Claude is thinking..."):
            answer = generate_response(query)
        st.markdown(answer)

    # Add assistant response to session
    active_messages.append({"role": "assistant", "content": answer})
    st.session_state.sessions[st.session_state.current_session] = active_messages
