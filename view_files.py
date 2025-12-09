#script to view files under a store name

from google import genai
from google.genai import types
import os
MY_API_KEY = "AIzaSyAtQP0ClNvyDTsNEzOIsBarDFYucWJoZ9Y" 

client = genai.Client(api_key=MY_API_KEY)

YOUR_STORE_NAME = "fileSearchStores/guidelines-okada4hag5zj" 
# -----------------


try:
    print(f"📄 Listing documents in store: {YOUR_STORE_NAME}\n")
    
    # Use the file_search_stores.documents.list() method
    documents_iterator = client.file_search_stores.documents.list(
        parent=YOUR_STORE_NAME
    )
    
    found_docs = False
    for doc in documents_iterator:
        found_docs = True
        print(f"  - Document Name:  {doc.name}")
        print(f"    Display Name:   {doc.display_name}")
        print(f"    State:          {doc.state.name}")
        print("-" * 40)
        
    if not found_docs:
        print("No documents found in this File Search Store.")

except Exception as e:
    print(f"An error occurred (check if the store name is correct): {e}")


#-------------------------------------------------------
#script to view all stores

# from google import genai
# import os

# client = genai.Client(api_key="AIzaSyAtQP0ClNvyDTsNEzOIsBarDFYucWJoZ9Y")

# def list_file_search_stores():
#     """Lists all File Search Stores and their document counts."""
#     print("🔍 Listing All File Search Stores:")
#     print("--------------------------------------------------")
    
#     try:
#         # Use the list() method on the file_search_stores object
#         stores_iterator = client.file_search_stores.list()
        
#         found_stores = False
#         for store in stores_iterator:
#             found_stores = True
#             print(f"  Display Name:     {store.display_name}")
#             # The NAME is the unique resource ID needed for deletion
#             print(f"  Resource Name:    {store.name}") 
#             print(f"  Active Documents: {store.active_documents_count}")
#             print("-" * 50)
            
#         if not found_stores:
#             print("No File Search Stores found.")
            
#     except Exception as e:
#         print(f"An error occurred while listing stores: {e}")

# if __name__ == "__main__":
#     list_file_search_stores()

#-------------------------------------------------------
#script to delete a store


# from google import genai
# import os

# # Ensure your GEMINI_API_KEY is set in your environment
# client = genai.Client(api_key="AIzaSyAtQP0ClNvyDTsNEzOIsBarDFYucWJoZ9Y")

# def delete_file_search_store():
#     """Deletes a specified File Search Store and all its contents."""

#     # 1. REPLACE THE VALUE BELOW with the 'Resource Name' from the listing script.
#     # It must be the full string, e.g., "fileSearchStores/your-store-id-12345"
#     STORE_TO_DELETE_NAME = input(
#         "Enter the EXACT Resource Name of the store to DELETE (e.g., fileSearchStores/store-id): "
#     ).strip()

#     if not STORE_TO_DELETE_NAME or not STORE_TO_DELETE_NAME.startswith("fileSearchStores/"):
#         print("Invalid store name format. Deletion cancelled.")
#         return

#     print(f"\n--- WARNING: PERMANENT DELETION ---")
#     print(f"You are about to delete the store: {STORE_TO_DELETE_NAME}")
#     print("This will permanently remove the store AND all indexed documents.")
    
#     confirmation = input("Type 'CONFIRM DELETE' to proceed: ").strip()

#     if confirmation == "y":
#         try:
#             # Use the delete() method with force=True to remove documents as well
#             client.file_search_stores.delete(
#                 name=STORE_TO_DELETE_NAME,
#                 config={"force": True}
#             )
#             print(f"\n✅ Successfully initiated deletion for: {STORE_TO_DELETE_NAME}")
#             print("Deletion is an asynchronous operation and may take a moment to fully process.")
#             print("You can re-run the listing script to confirm its eventual removal.")
#         except Exception as e:
#             print(f"\n❌ An error occurred during deletion: {e}")
#     else:
#         print("\nDeletion cancelled by user.")


# if __name__ == "__main__":
#     delete_file_search_store()