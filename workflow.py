from anthropic import Anthropic
import io
from drive_manager import list_data_files, get_drive_service, get_framework_content, api_get_file_content
import os

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_response(user_query):
    """Combine framework, drive content, and user query, then get Claude's answer (with logging)."""
    print("\n🔍 Starting generate_response()")
    service = get_drive_service()
    files = list_data_files()

    print(f"📂 Total files found: {len(files)}")
    for f in files:
        print(f"   - {f['name']}  (source: {f.get('source','unknown')}, mimeType: {f.get('mimeType','?')})")

    # --- 1. Get the framework (the structured instructions) ---
    framework_text = get_framework_content()

    
    system_prompt = f"""
    You MUST strictly follow the framework provided below.
    Do NOT ignore, modify, or override any part of it.

    === FRAMEWORK START ===
    {framework_text}
    === FRAMEWORK END ===
    """
    if framework_text.strip():
        print("✅ Framework content loaded successfully.")
        print(f"📏 Framework length: {len(framework_text)} characters")
        # Check if it's actually text or binary garbage
        if framework_text[:50].isprintable():
            print(f"🧱 Framework preview:\n{framework_text[:400]}...\n")
        else:
            print("⚠️ Framework appears to be BINARY data, not text!")
            print(f"🔍 First bytes (hex): {framework_text[:50].encode('utf-8', errors='ignore')}")
    else:
        print("⚠️ Framework content is EMPTY or not accessible!")
    
    # --- 2. Fetch patient data + guidelines text ---
    combined_text = ""
    for f in files:
        # Only include patient data and guidelines in the user message
        if f.get('source') in ['patient_data', 'guidelines']:
            content = api_get_file_content(service, f["id"], f["mimeType"])
            combined_text += f"\n\n---\nDocument: {f['name']}\n{content}"
            preview = content[:200] if isinstance(content, str) else str(content)[:200]
            print(f"\n📄 Preview of {f['name']}:\n{preview}\n")
    
    print("🧠 Sending prompt to Claude...")

    # --- 3. Build the user message with clear structure ---
    user_message = f"""Here is the user's health data and relevant guidelines:

{combined_text}

---

User's question: {user_query}"""

    # --- 4. Send to Claude ---
    response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    system=system_prompt,
    messages=[{"role": "user", "content": user_message}],
)

    return response.content[0].text