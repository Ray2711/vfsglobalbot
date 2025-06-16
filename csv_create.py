import csv
import re
from datetime import datetime

CSV_PATH = "appointments.csv"

def append_to_csv(city: str, dates_str: str):
    """
     Appends a row with this info:
      scraped_at, city, available_date

      Now why would you want it? What data would we gather from it? What valuable appointment dates insight could we possibly muster?  I dont know. But my bum ahh chief somehow knows. Wow.
    """
    # каждая строка — потенциальная дата
    rows = [line.strip() for line in dates_str.splitlines() if line.strip()]

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for text in rows:
            # 1) пытаемся найти DD-MM-YYYY
            m = re.search(r'\b\d{2}-\d{2}-\d{4}\b', text)
            if m:
                date_str = m.group(0)
                try:
                    dt = date_str
                except ValueError:
                    dt = "No dates"  # на всякий случай
            else:
                    dt = text

            writer.writerow([
                datetime.now().isoformat(),       # scraped_at
                city,                             # city
                dt.isoformat() if isinstance(dt, datetime) else dt
            ])