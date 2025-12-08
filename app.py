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

if "active_framework" not in st.session_state:
    st.session_state.active_framework = None

if "preset_query" not in st.session_state:
    st.session_state.preset_query = None

# ===============================
# Sidebar: Framework Input (NO SAVE)
# ===============================
st.sidebar.divider()
st.sidebar.header("🧩 Prompt Framework")

framework_text = st.sidebar.text_area(
    "Framework (used as system prompt)",
    height=350,
    placeholder="""
Role & Context:
You are a digital health assistant helping users prepare for medical appointments.

Rules:
- Do not provide diagnoses
- Summarize clearly in bullet points
- Cite guideline sources when available
- Use patient data only from provided context
"""
)

if st.sidebar.button("✅ Use this framework"):
    if framework_text.strip():
        st.session_state.active_framework = {
            "name": "UI Framework",
            "content": framework_text
        }
        st.sidebar.success("Framework is now active")
    else:
        st.sidebar.error("Framework cannot be empty")

if st.session_state.active_framework:
    st.sidebar.info("✅ A custom framework is currently active")

# ===============================
# Sidebar: Document Context (read-only)
# ===============================
st.sidebar.divider()
st.sidebar.header("📂 Current Document Context")

files = list_data_files()
if not files:
    st.sidebar.info("No documents found in the shared folder yet.")
else:
    for f in files:
        st.sidebar.markdown(f"📄 {f['name']}")

# ===============================
# Main Area: Chat Interface
# ===============================
active_messages = st.session_state.sessions[st.session_state.current_session]

# 1️⃣ Chat history
for message in active_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2️⃣ Preset questions
st.markdown("### Quick Questions")

preset_questions = [
    "Summarize health status over the last 30 days",
    "What's my health summary?",
    "What should I ask my doctor?",
    "Summarize my recent metrics",
]

cols = st.columns(len(preset_questions))

for i, q in enumerate(preset_questions):
    if cols[i].button(q, key=f"preset_{i}"):
        st.session_state.preset_query = q
        st.rerun()

# 3️⃣ Chat input
chat_input = st.chat_input("Enter your medical question:")

query = None
if st.session_state.preset_query:
    query = st.session_state.preset_query
    st.session_state.preset_query = None
elif chat_input:
    query = chat_input

# 4️⃣ Process query
if query:
    active_messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = generate_response(
                query,
                st.session_state.active_framework
            )

        st.markdown(answer)

    active_messages.append({"role": "assistant", "content": answer})
    st.session_state.sessions[
        st.session_state.current_session
    ] = active_messages
