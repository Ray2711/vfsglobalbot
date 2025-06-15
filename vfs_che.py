from seleniumbase import SB
from send_msg import send_telegram_message, send_to_db
from random_email import (get_random_email, get_password)
 
with SB(uc=True, headless2=False) as sb:
    url = "https://visa.vfsglobal.com/kaz/en/che/login"
    login = get_random_email()
    password = get_password()

    

    sb.activate_cdp_mode(url)
    sb.sleep(10)
    sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
    ##CLOUDFLARE 
    sb.uc_gui_click_captcha()
    ##END CLOUDFLARE
    sb.sleep(5)
    sb.cdp.press_keys("#email", login)
    sb.cdp.press_keys("#password", password)
    sb.sleep(2)
    sb.click(".btn-brand-orange")
    sb.sleep(20)
    sb.cdp.click('button:contains("Start New Booking")')
    sb.sleep(5) 
    sb.cdp.click('mat-select:contains("Application Ce")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Almaty")')
    sb.sleep(5)
    #sb.cdp.click('mat-select:contains("appointment category")')
   # sb.sleep(1)
    #sb.cdp.click('mat-option:contains("C/D")')
    #sb.sleep(5)
    sb.cdp.click('mat-select:contains("sub-category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Tourist")')
    sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    send_telegram_message("Шве Алм " +"\n" +dates)
    send_to_db("Шве Алм  " +dates )
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("Application Ce")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Application Center-Astana")')
    sb.sleep(5)
    #sb.cdp.click('mat-select:contains("appointment category")')
    #sb.sleep(1)
    #sb.cdp.click('mat-option:contains("C/D")')
    #sb.sleep(5)
    sb.cdp.click('mat-select:contains("sub")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Tourist")')
    sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    send_telegram_message("Шве Аст " +"\n" +dates)
    send_to_db("Шве Аст  " +dates )


