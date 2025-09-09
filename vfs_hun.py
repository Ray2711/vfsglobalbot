  
from re import A
from seleniumbase import SB
from csv_create import append_to_csv
from send_msg import send_telegram_message, send_to_db
from random_email import (get_random_email, get_password)
import pyautogui
import random
import time

 
with SB(uc=True, headless2=False) as sb:
    url = "https://visa.vfsglobal.com/kaz/en/hun/login"
    login = get_random_email()
    password = get_password()

    

    sb.activate_cdp_mode(url)
    sb.sleep(10)
    sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
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
            #sb.minimize_window()
            
            pyautogui.click()
            sb.sleep(10)
            sb.click(".btn-brand-orange")
            sb.sleep(10)
            sb.cdp.click('button:contains("Start New Booking")')
            loggedin = True
            
        except:
            print("1")
            tries += 1
            sb.open(url)
            sb.sleep(3)
            login = get_random_email()
    sb.sleep(5)
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("Application Ce")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Almaty")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("appointment category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Short")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("sub")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Tourist")')
    sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    #send_telegram_message("Dates for Visa centre of " +sb.get_text("//mat-select[contains(., 'Almaty')]") +"\n" +dates)
    send_telegram_message("Вен Алм " +"\n" +dates)
    send_to_db("Вен Алм " +"\n" +dates)
    append_to_csv("Вен Алм", dates)



