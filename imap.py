import imaplib
import email
from email.header import decode_header
import re
import email.utils
import datetime
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()
IMAP_SERVER   = "imap.mail.ru"
IMAP_PORT     = 993
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
PASSWORD      = os.getenv("PASSWORD_EMAIL")

def decode_subject(subject):
    """Decode non-ASCII email subjects."""
    if not subject:
        return ""
    decoded, encoding = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or "utf-8", errors="replace")
    return decoded

def extract_otp(text):
    """Ищет в тексте ровно 6 цифр подряд."""
    m = re.search(r"\b\d{6}\b", text)
    return m.group(0) if m else None

def get_email_date(msg):
    """Парсит Date-заголовок в datetime."""
    date_str = msg.get("Date", "")
    tup = email.utils.parsedate_tz(date_str)
    return datetime.datetime.fromtimestamp(email.utils.mktime_tz(tup)) if tup else datetime.datetime.min

def get_email_text(msg):
    """Извлекает текстовую часть письма."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace")
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace")
    return ""

def main(country, max_attempts=None):
    if not EMAIL_ADDRESS or not PASSWORD:
        print("ERROR: EMAIL_ADDRESS or PASSWORD not set")
        return

    # Открываем соединение и логинимся один раз
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ADDRESS, PASSWORD)
    print("✅ Logged in")
    mail.select("inbox")

    attempts = 0
    while True:
        attempts += 1
        if max_attempts and attempts > max_attempts:
            print("🚫 Max attempts reached, exiting.")
            break

        # Ищем только новые письма с конкретным Subject и From
        email_ids = []
        for sender in ("donotreply@vfsglobal.com", "donotreply@vfshelpline.com"):
            status, data = mail.search(
                None,
                f'UNSEEN FROM "{sender}" SUBJECT "One Time Password"'
            )
            if status == "OK":
                email_ids += data[0].split()
            else:
                print(f"⚠️  Search error for {sender}")

        email_ids = list(set(email_ids))
        if not email_ids:
            print(f"{datetime.datetime.now()} — нет новых OTP, жду 10 секунд…")
            time.sleep(10)
            continue

        # Парсим и фильтруем по country
        candidates = []
        for eid in email_ids:
            status, msg_data = mail.fetch(eid, "(RFC822)")
            if status != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            text = get_email_text(msg)
            if not re.search(country, text, re.IGNORECASE):
                # не то письмо — отмечаем как прочитанное, чтобы не гонять в каждом цикле
                mail.store(eid, "+FLAGS", "\\Seen")
                continue
            date = get_email_date(msg)
            candidates.append((eid, date, msg, text))

        if not candidates:
            print(f"{datetime.datetime.now()} — нет OTP для '{country}', жду 10 секунд…")
            time.sleep(10)
            continue

        # Берем самое свежее
        candidates.sort(key=lambda x: x[1], reverse=True)
        eid, date, msg, text = candidates[0]
        otp = extract_otp(text)
        if otp:
            print(f"🎉 Найден OTP: {otp}")
            mail.store(eid, "+FLAGS", "\\Seen")
            mail.logout()
            return otp
        else:
            print(f"{datetime.datetime.now()} — нет 6-значного кода в письме, жду 10 секунд…")
            mail.store(eid, "+FLAGS", "\\Seen")
            time.sleep(10)

if __name__ == "__main__":
    # По умолчанию бесконечно, можно передать max_attempts
    otp = main(country="cze", max_attempts=None)