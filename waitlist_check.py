from datetime import datetime
from seleniumbase import SB
from csv_create import append_to_csv
from send_msg import (send_telegram_message, send_telegram_message_error, send_telegram_message_ping, send_to_db)
from random_email import (get_random_email, get_password, get_waitlist_email)

from dotenv import load_dotenv
import os

import pyautogui
import random
import time

from send_to_fb import send_to_firestore

load_dotenv()


def vfs_checkdates(link,abb1, isImportant: bool,acc_email, group_id1 = 0) -> None:
    REPORTERRORS = os.getenv("REPORTERRORS") == "True"
    try:
        with SB(uc=True, locale="en") as sb:
            url = link
            login = acc_email
            password = get_password()
            
            #sb.execute_cdp_cmd("Network.clearBrowserCache", {})
            

            
            
            sb.activate_cdp_mode(url)
            sb.sleep(15)
            sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
            ##CLOUDFLARE 
            #cf_manual_solver(sb)
            
            ##END CLOUDFLARE
            sb.sleep(1)
            sb.maximize_window()
            loggedin = False
            tries = 0 
            sb.uc_gui_click_captcha()
            pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y - 10, duration=random.uniform(0.1, 0.3), tween=pyautogui.easeOutQuad)
            time.sleep(random.uniform(0.05, 0.15))
            pyautogui.click()
 
            while(loggedin == False and tries < 10):
                try:
                    sb.cdp.press_keys("#email", login)
                    sb.cdp.press_keys("#password", password)
                    sb.sleep(2)
                    
                    pyautogui.click()
                    sb.sleep(10)
                    sb.click(".btn-brand-orange")
                    sb.sleep(10)
                   # sb.cdp.find_element('button:contains("Start New Booking")')
                    sb.cdp.find_element(f'div:contains("{group_id1}") span:contains(" Book Now ")')
                    loggedin = True
                   
                except Exception as e:

                    print(e)
                    tries += 1
                    sb.open(url)
                    sb.sleep(3)
                    
            
            if(tries >= 9):
                send_telegram_message_error(abb1 + " could not log in. May be blocked")
            card = sb.cdp.find_element(f'div:contains("{group_id1}") span:contains(" Book Now ")')
            card.click()
            month = ""
            for i in range(2):
                try:
                    print(f'try {i}')
                    sb.sleep(10)
                    # 1. Month & Year from the header
                    header_text = sb.get_text("h2.fc-toolbar-title").strip()
                    month_name, year = header_text.split()
                    #month_num = datetime.strptime(month_name, "%B").month
                    month = month_name
                    print(header_text)
                    # 2. All numbers inside divs with class "date-availiable"
                    available_dates_elements = sb.find_elements('.date-availiable')
                    available_dates = []
                    dates_to_db = []
                    for el in available_dates_elements:
                        date_attr = el.get_attribute('data-date')
                        if date_attr:
                            available_dates.append(f"{date_attr[-2:]} {month_name} {year}")
                            dates_to_db.append(date_attr)
                    available_dates_str = "Available Dates: " + ", ".join(available_dates)
                    print(available_dates_str)
                    send_telegram_message_error(abb1 + " "+available_dates_str)
                    send_to_firestore("list_appointment_dates","vfs",abb1,dates_to_db)
                    append_to_csv(abb1,dates_to_db)
                except Exception as e:
                    print(e)
                    send_telegram_message_error(f" {abb1} {month} no dates " )
                    sb.click(".fc-next-button")
            
            
            
    except Exception as e:
        print(e)
        if(REPORTERRORS):
            send_telegram_message_error(f"Error in : {link} : \n Couldn't get dates " )


