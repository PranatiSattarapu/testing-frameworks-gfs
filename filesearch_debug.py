# import google.genai as genai

# # ⚠️ PASTE ONE OF YOUR API KEYS HERE
# API_KEY = "AIzaSyBhQRAhH7Q-_T1J0iUVY8hSXBGmE52tQzk" 

# def list_supported_models():
#     """Lists all models accessible by the client."""
#     try:
#         # Initialize client (uses the newer google-genai style)
#         client = genai.Client(api_key=API_KEY)
#         print("✅ Listing all available model IDs:")
        
#         # Iterate through all Model objects and print their names
#         for model in client.models.list():
#             # Simply print the model name attribute, which always exists.
#             print(f"  - {model.name}")
        
#     except Exception as e:
#         # This will still catch quota or authentication errors
#         print(f"❌ An error occurred while listing models: {e}")

# if __name__ == "__main__":
#     list_supported_models()


import google.genai as genai
from google.genai import types

# ⚠️ PASTE YOUR ACTUAL API KEY HERE
# This must be the key that authenticated successfully
API_KEY = "AIzaSyBhQRAhH7Q-_T1J0iUVY8hSXBGmE52tQzk"

# The lightest, most cost-effective model you found
LIGHTEST_MODEL_ID = "models/gemini-2.5-flash-lite"

# The question you want to ask the model
QUESTION = "What is the capital of France and briefly explain why it's famous?"

def run_simple_query():
    """Initializes the client and sends a single, simple question to the Gemini API."""
    try:
        # 1. Initialize Client
        client = genai.Client(api_key=API_KEY)
        
        print(f"✅ Sending question to model: {LIGHTEST_MODEL_ID}...")
        
        # 2. Generate Content
        # We pass the model ID and the text content (question)
        response = client.models.generate_content(
            model=LIGHTEST_MODEL_ID,
            contents=QUESTION
        )
        
        # 3. Print the result
        print("\n--- Model Response ---")
        print(response.text)
        print("\n----------------------")
        print("🎉 SUCCESS! Your Gemini API is working for content generation.")

    except Exception as e:
        # This will catch your quota (429) or other API errors
        print("\n❌ API Request Failed.")
        print(f"Error: {e}")
        print("\nIf the error is 429 RESOURCE_EXHAUSTED, the key is valid but quota is the issue.")

if __name__ == "__main__":
    run_simple_query()