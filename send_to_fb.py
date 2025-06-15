import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import os

load_dotenv()


# --- Configuration ---
# Replace with the path to your downloaded service account key
SERVICE_ACCOUNT_KEY_PATH = os.getenv("DB_KEY")

DATABASE_URL = DB_URL = os.getenv("DB_URL")

# The path within your database where you want to work
TARGET_PATH = "/dates"


def send_to_fb(field, data_to_update) -> None:
    # --- Initialize Firebase Admin SDK ---
    try:
        # Check if Firebase app is already initialized
        # This prevents errors if you run the script multiple times in the same session
        firebase_admin.get_app()
    except ValueError:
        # Initialize the app with the service account key and database URL
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })


    # --- Get a reference to the target path and perform the update ---
    try:
        ref = db.reference(TARGET_PATH)
        ref.update({ field : data_to_update})


    except Exception as e:
        print(f"An error occurred: {e}")

