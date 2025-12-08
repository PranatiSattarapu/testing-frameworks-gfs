# import os
# import time
# from google import genai
# from google.genai import types

# # 1. Your Gemini API Key
# GEMINI_API_KEY = "AIzaSyCUY-giT7f_fBSgAxCwgCCLEtaElknki6"
# # 2. The local path to the folder containing all your guidelines (e.g., PDFs, TXT, DOCX)
# LOCAL_DOCS_FOLDER = "./guidelines"
# # ----------------------------------------

# # The name you want for the File Search Store (The RAG knowledge base)
# STORE_DISPLAY_NAME = "guidelines"

# def upload_local_documents_to_store():
#     """
#     1. Creates a Gemini File Search Store named "guidelines".
#     2. Iterates over a local folder and uploads all files to the store for indexing.
#     """
    
#     # 1. Initialize Client
#     client = genai.Client(api_key=GEMINI_API_KEY)
    
#     # 2. Check if the local folder exists and has files
#     if not os.path.isdir(LOCAL_DOCS_FOLDER):
#         print(f"❌ ERROR: Document folder not found at '{LOCAL_DOCS_FOLDER}'.")
#         print("Please create this folder and place your guideline files inside.")
#         return

#     local_files = [f for f in os.listdir(LOCAL_DOCS_FOLDER) if os.path.isfile(os.path.join(LOCAL_DOCS_FOLDER, f))]
#     if not local_files:
#         print(f"⚠️ WARNING: No files found in '{LOCAL_DOCS_FOLDER}'. Nothing to upload.")
#         return
    
#     # 3. Create the File Search Store 
#     print(f"1. Creating File Search Store: {STORE_DISPLAY_NAME}...")
#     file_search_store = client.file_search_stores.create(
#         config={'display_name': STORE_DISPLAY_NAME}
#     )
#     print(f"   ✅ Store created! Full Name: {file_search_store.name}")
#     print(f"   ⚠️ COPY THIS ID for your main application: {file_search_store.name}\n")

#     upload_operations = []
    
#     # 4. Upload and Index each file
#     for name in local_files:
#         local_path = os.path.join(LOCAL_DOCS_FOLDER, name)
        
#         print(f"2. Uploading and processing file: {name}")

#         try:
#             # client.file_search_stores.upload_to_file_search_store handles 
#             # file upload, chunking, and embedding in one step.
#             operation = client.file_search_stores.upload_to_file_search_store(
#                 file=local_path,
#                 file_search_store_name=file_search_store.name,
#                 config={
#                     'display_name': name,
#                 }
#             )
#             upload_operations.append(operation)
#             print("   - Upload started (indexing in progress)...")
#         except Exception as e:
#             print(f"   ❌ Failed to upload {name}: {e}. Skipping.")
#             continue
            

#     # 5. Wait for all indexing operations to complete
#     print("\n3. Waiting for all indexing operations to complete. This may take a few minutes...")
#     for i, op in enumerate(upload_operations):
#         op_name = op.name
#         print(f"   - Waiting for Operation {i+1}/{len(local_files)}: {op_name}")
#         while not op.done:
#             # Poll every 5 seconds to check status
#             time.sleep(5)
#             op = client.operations.get(op)
#         print(f"   ✅ Operation {i+1} completed!")

#     print("\n\n🎉 ALL GUIDELINES SUCCESSFULLY INDEXED!")
#     print(f"Your final store ID is: {file_search_store.name}")
#     print("\n--- Copy this ID and use it in your main RAG application code. ---")


# if __name__ == "__main__":
#     upload_local_documents_to_store()

#     #fileSearchStores/guidelines-okada4hag5zj


from google import genai
from google.genai import types

API_KEY = "AIzaSyAtQP0ClNvyDTsNEzOIsBarDFYucWJoZ9Y"

def check_gemini_key():
    try:
        client = genai.Client(api_key=API_KEY)
        resp = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="ping",
            config=types.GenerateContentConfig(max_output_tokens=1),
        )
        print("✅ Key is valid (request succeeded).")
    except Exception as e:
        print("❌ Key is invalid or has no quota.")
        print(e)

if __name__ == "__main__":
    check_gemini_key()
