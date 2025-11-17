import streamlit as st
from drive_manager import list_data_files, get_drive_service, api_get_files_in_folder, FOLDER_ID_PATIENT_DATA
from workflow import generate_response # Assuming this is your Claude integration
# st.write("Google key loaded:", "GOOGLE_SERVICE_ACCOUNT" in st.secrets)

# service = get_drive_service()
# st.write("Drive service object:", service)

# st.write("Google key exists:", "GOOGLE_SERVICE_ACCOUNT" in st.secrets)

# service = get_drive_service()
# st.write("Drive service object:", service)

# if service:
#     st.write("Patient Data Folder:", api_get_files_in_folder(service, FOLDER_ID_PATIENT_DATA))
# --- Streamlit Configuration ---
st.set_page_config(page_title="Health Tutor Console", layout="wide")
st.title("Prompt Refinement Console")

# --- 1. Initialize Session State for Multi-Session Chat ---
if "sessions" not in st.session_state:
    # Key is session name, value is the list of messages
    st.session_state.sessions = {"Session 1": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Session 1"


# --- Sidebar: Document Management (Read-Only) ---
st.sidebar.header("📂 Current Document Context")

# Fetch files from Drive (Read-only view)
files = list_data_files() 

if not files:
    st.sidebar.info("No documents found in the shared folder yet.")
else:
    # Note: We are just displaying the files, not allowing deletion from Drive here.
    st.sidebar.markdown("**Documents informing the context:**")
    for f in files:
        st.sidebar.markdown(f"📄 {f['name']}")

st.divider()

# --- Main Area: Chat Interface ---
# st.header(f"💬 Prompt Refinement: {st.session_state.current_session}")

# Get the messages for the active session
# --- Main Area: Chat Interface ---

active_messages = st.session_state.sessions[st.session_state.current_session]

# TOP: chat history
chat_container = st.container()

# BOTTOM: preset questions + chatbox
bottom_container = st.container()

# -------------------- CHAT HISTORY --------------------
with chat_container:
    for message in active_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# -------------------- BOTTOM FIXED AREA --------------------
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

    # Always show chatbox
    chatbox_input = st.chat_input("Enter your medical question:")

# -------------------- DECIDE FINAL QUERY --------------------
query = None

if st.session_state.preset_query:
    query = st.session_state.preset_query
    st.session_state.preset_query = None
elif chatbox_input:
    query = chatbox_input

# -------------------- PROCESS QUERY --------------------
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


