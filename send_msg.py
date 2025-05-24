  
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
USERNAME = os.getenv("MENTION")
DB_URL = os.getenv("DB_URL")
DB_KEY = os.getenv("DB_KEY")

MAKE_URL = os.getenv("MAKE_URL")

def send_telegram_message(text: str) -> None:
    """
    Sends a message to a Telegram chat using a bot token from environment variables.

    Args:
        text (str): Message text to send.

    Returns:
        dict: Response from the Telegram API.
    """
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("BOT_TOKEN or CHAT_ID is not set in the .env file")
    #formatted_text = re.sub(r"(?<!\n) Earliest", r"\nEarliest", text)
    match = re.search(r'\b\d{2}-\d{2}-\d{4}\b', text)
    
    if match:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text[:7]+" "+match.group() , "disable_notification": True}
        response = requests.post(url, json=payload)
        return response.json()
    else:
        print("No date found in the text.")


def send_telegram_message_ping(text :str):
    """
    Sends a message to a Telegram chat using a bot token from environment variables.

    Args:
        text (str): Message text to send.

    Returns:
        dict: Response from the Telegram API.
    """
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("BOT_TOKEN or CHAT_ID is not set in the .env file")
    #formatted_text = re.sub(r"(?<!\n) Earliest", r"\nEarliest", text)
    match = re.search(r'\b\d{2}-\d{2}-\d{4}\b', text)
    
    if match:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text[:7]+" "+match.group()+ f" @{USERNAME}", "disable_notification": False}
        response = requests.post(url, json=payload)
        return response.json()
    else:
        print("No date found in the text.")

def send_to_db(text :str):
    """
    Sends a message to a Telegram chat using a bot token from environment variables.

    Args:
        text (str): Message text to send.

    Returns:
        dict: Response from the Telegram API.
    """
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("BOT_TOKEN or CHAT_ID is not set in the .env file")
    #formatted_text = re.sub(r"(?<!\n) Earliest", r"\nEarliest", text)
    match = re.search(r'\b\d{2}-\d{2}-\d{4}\b', text)
    dates = ""
    if match:
        dates = match.group()
    else:
        dates = "No dates"
    url = f"{DB_URL}"
    payload = {"appointmentCenter": text[:7], "closestAppointment":dates}
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json', 'x-api-key': DB_KEY })
    return response.json()