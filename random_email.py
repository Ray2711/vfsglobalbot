import os
import random
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
WAITLIST_EMAIL = os.getenv("WAITLIST_EMAIL")
PASSWORD = os.getenv("PASSWORD")

#Assuming all password are the same.
# Enter your emails here, if you have more than one
EMAILS = [email.strip() for email in EMAIL.split(',')]
# OH NOOO I PUSHED MY EMAILS ON MAIN OH NOOOOO idk atp 

def get_random_email():
    """
    Returns a random email from the list.
    """
    if not EMAILS:
        raise ValueError("Email list is empty.")
    return random.choice(EMAILS)


def get_waitlist_email():
    if not WAITLIST_EMAIL:
        raise ValueError("Waitlist email is empty.")
    return WAITLIST_EMAIL

def get_password():
    return PASSWORD
