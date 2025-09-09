import datetime
from seleniumbase import SB
from csv_create import append_to_csv
from send_msg import (send_telegram_message, send_telegram_message_error, send_telegram_message_ping, send_to_db)
from random_email import (get_random_email, get_password, get_waitlist_email)

from dotenv import load_dotenv
import os

import pyautogui
import random
import time

load_dotenv()

def vfs_checkdates(link,city1,city2,abb1,abb2, isImportant: bool , isImportant2: bool , group_id1 = 0, group_id2 = 0) -> None:
    try:
        with SB(uc=True, locale="en") as sb:
            url = link
            login = get_waitlist_email()
            password = get_password()
            REPORTERRORS = os.getenv("REPORTERRORS") == "True"
            #sb.execute_cdp_cmd("Network.clearBrowserCache", {})

            

            sb.activate_cdp_mode(url)
            sb.sleep(10)
            sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
            ##CLOUDFLARE 
            #cf_manual_solver(sb)
            
            ##END CLOUDFLARE
            sb.sleep(1)
            sb.maximize_window()
            loggedin = False
            tries = 0 
 
            while(loggedin == False and tries < 10):
                try:
                    sb.cdp.press_keys("#email", login)
                    sb.cdp.press_keys("#password", password)
                    sb.sleep(6)
                    #sb.minimize_window()
                    sb.uc_gui_click_captcha()
                    pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y - 10, duration=random.uniform(0.1, 0.3), tween=pyautogui.easeOutQuad)
                    time.sleep(random.uniform(0.05, 0.15))
                    pyautogui.click()
                    sb.sleep(10)
                    sb.click(".btn-brand-orange")
                    sb.sleep(10)
                    sb.wait_for_element_visible('button:contains("Start New Booking")')
                    loggedin = True
                    tries += 1
                except:
                    sb.cdp.gui_click_element("a.c-brand-orange")
                    pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y - 10, duration=random.uniform(0.1, 0.3), tween=pyautogui.easeOutQuad)
                    time.sleep(random.uniform(0.05, 0.15))
                    pyautogui.click()
                    sb.sleep(10)
                    login = get_random_email()
            
            if(tries >= 9):
                send_telegram_message_error(abb1 + " could not log in. May be blocked")

            try:
                # 1. Locate the card that contains the reference number
                card = f'div.card:contains("{group_id1}")'

                # 2. Inside that card, click the “Book Now” span
                sb.click(f'{card} span:contains("Book Now")')


                            # 1. Month & Year from the header
                header_text = sb.get_text("h2.fc-toolbar-title").strip()
                month_name, year = header_text.split()
                month_num = datetime.strptime(month_name, "%B").month

                # 2. All numbers inside divs with class "date-availiable"
                numbers = [
                    int(el.text)
                    for el in sb.find_elements("div.date-availiable .fc-daygrid-day-number")
                ]
                numbers.sort()

                # 3. Full list as one string
                all_dates_str = "\n".join(
                    f"{day:02d} {month_name} {year}" for day in numbers
                )

                # 4. First date as DD-MM-YYYY
                first_date = f"{numbers[0]:02d}-{month_num:02d}-{year}" \
                    if numbers else None

            # Variables now ready for use
                print(all_dates_str)
                print(first_date)
            except Exception as e:
                print(e)
                send_telegram_message_error(f" {abb1} no dates " )
            
            
            #send_to_db(abb2 +"\n" +dates)
            #append_to_csv(abb2,dates)
    except Exception as e:
        print(e)
        if(REPORTERRORS):
            send_telegram_message_error(f"Error in : {link} : \n Couldn't get dates " )


