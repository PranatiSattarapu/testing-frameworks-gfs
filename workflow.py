from dotenv import load_dotenv
load_dotenv()


import json
import csv
from pathlib import Path
from io import StringIO
from google import genai
from google.genai import types
from anthropic import Anthropic
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)


# ===============================
# Configuration
# ===============================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
GUIDELINE_STORE_NAME = os.getenv("GUIDELINE_STORE_NAME")
PATIENT_DATA_FOLDER = "user_data"

client = genai.Client(api_key=GEMINI_API_KEY)
claude = Anthropic(api_key=CLAUDE_API_KEY)

# ===============================
# Patient Data Helpers
# ===============================
def csv_to_llm_text(csv_data):
    output = []
    csvfile = StringIO(csv_data)
    reader = csv.DictReader(csvfile)

    if reader.fieldnames:
        output.append("HEADERS: " + " | ".join(reader.fieldnames))
        output.append("-" * 50)

    for i, row in enumerate(reader):
        row_details = [
            f"{k.strip()}={str(v).strip()}"
            for k, v in row.items()
            if v and str(v).strip()
        ]
        output.append(f"ROW {i+1}: " + ", ".join(row_details))

    return "\n".join(output)


def load_local_patient_data(folder_path=PATIENT_DATA_FOLDER):
    patient_text = []
    path = Path(folder_path)

    if not path.is_dir():
        return "\n--- PATIENT DATA: NONE FOUND ---\n"

    for file_path in path.iterdir():
        if not file_path.is_file() or file_path.name.startswith("."):
            continue

        try:
            raw = file_path.read_text(encoding="utf-8")

            if file_path.suffix.lower() == ".json":
                content = json.dumps(json.loads(raw), indent=2)
            elif file_path.suffix.lower() == ".csv":
                content = csv_to_llm_text(raw)
            else:
                content = raw

            patient_text.append(
                f"\n\n--- PATIENT FILE: {file_path.name} ---\n{content}"
            )

        except Exception as e:
            print(f"⚠️ Failed to read {file_path.name}: {e}")

    return "\n".join(patient_text) if patient_text else "\n--- PATIENT DATA: NONE FOUND ---\n"

# ===============================
# MAIN WORKFLOW (NO FALLBACK)
# ===============================
def generate_response(user_query, framework_override):
    print("\n🔍 Starting generate_response")

    if not framework_override or not framework_override.get("content"):
        raise ValueError(
            "No framework provided. User must define a framework in the UI."
        )

    framework_text = framework_override["content"]
    framework_name = framework_override.get("name", "UI Framework")

    print(f"🧠 Using framework: {framework_name}")
    logging.info("FRAMEWORK | source=UI | name=%s | length=%d",
             framework_name,
             len(framework_text))


    system_prompt = f"""
You MUST strictly follow everything defined in the framework.
Do NOT override format, tone, or safety rules.

=== FRAMEWORK START: {framework_name} ===
{framework_text}
=== FRAMEWORK END ===
"""

    # ===============================
    # Load patient data
    # ===============================
    patient_text = load_local_patient_data()
    if patient_text.strip():
        logging.info("PATIENT_DATA | source=local_files | chars=%d",
                    len(patient_text))
    else:
        logging.warning("PATIENT_DATA | NONE")

    # ===============================
    # Gemini FileSearch (Guidelines)
    # ===============================
    guideline_text = "No guideline chunks retrieved."
    sources = set()

    retrieval_prompt = f"""
You MUST use the File Search tool.
Do NOT answer from general knowledge.

Search ADA clinical practice guidelines relevant to:

Query: {user_query}

Patient context:
{patient_text[:600]}
"""
    logging.info(
        "FILESEARCH | store=%s | query_chars=%d",
        GUIDELINE_STORE_NAME,
        len(user_query)
    )

    try:
        rag_resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=retrieval_prompt,
            config=types.GenerateContentConfig(
                tools=[{
                    "fileSearch": {
                        "fileSearchStoreNames": [GUIDELINE_STORE_NAME]
                    }
                }],
                max_output_tokens=2000,
                temperature=0.2
            )
        )

        if rag_resp.candidates and rag_resp.candidates[0].grounding_metadata:
            
            chunks = rag_resp.candidates[0].grounding_metadata.grounding_chunks

            logging.info(
                "FILESEARCH_RESULT | chunks_retrieved=%d",
                len(chunks)
            )

            retrieved = []

            for c in chunks:
                logging.info(
                    "GUIDELINE_CHUNK | source=%s | text_chars=%d",
                    c.retrieved_context.title,
                    len(c.retrieved_context.text)
                )
                retrieved.append(
                    f"[From: {c.retrieved_context.title}]\n"
                    f"{c.retrieved_context.text}"
                )
                sources.add(c.retrieved_context.title)

            guideline_text = "\n\n---\n\n".join(retrieved)

    except Exception as e:
        print("⚠️ Gemini FileSearch error:", e)

    # ===============================
    # Claude Final Answer
    # ===============================
    final_prompt = f"""
=== PATIENT DATA ===
{patient_text}

=== RETRIEVED GUIDELINES ===
{guideline_text}

User question:
{user_query}
"""
    logging.info("CLAUDE | final_synthesis | input_chars=%d",
             len(final_prompt))

    claude_resp = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        system=system_prompt,
        messages=[{"role": "user", "content": final_prompt}]
    )

    return claude_resp.content[0].text
