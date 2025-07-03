import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore # Import Firestore
from dotenv import load_dotenv
import os

load_dotenv()


SERVICE_ACCOUNT_KEY_PATH = os.getenv("DB_KEY")

# --- Initialize Firebase Admin SDK (only once) ---
def initialize_firebase_app():
    """Initializes the Firebase Admin SDK if not already initialized."""
    try:
        firebase_admin.get_app()
        print("Firebase app already initialized.")
    except ValueError:
        # Initialize the app with the service account key
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
        print("Firebase app initialized.")

# Call initialization once when the script starts
initialize_firebase_app()

def send_to_firestore(collection_name: str, document_id: str, field: str, value) -> None:
    """
    Sends a specific field and its value to a Firestore document.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document within the collection.
        field (str): The name of the field to update or add.
        value (any): The value to set for the specified field.
    """
    try:
        # Get a Firestore client instance
        db = firestore.client()

        # Create a dictionary for the update, where the key is the field name
        data_to_update = {field: value}

        # Get a reference to the specific document
        doc_ref = db.collection(collection_name).document(document_id)

        # Use set with merge=True to update the specific field.
        # If the document or field does not exist, it will be created.
        doc_ref.set(data_to_update, merge=True)
        print(f"Successfully sent '{field}: {value}' to document '{document_id}' in collection '{collection_name}'.")

    except Exception as e:
        print(f"An error occurred while sending to Firestore: {e}")
