from seleniumbase import SB
from send_msg import send_telegram_message
from random_email import (get_random_email, get_password)
from captcha import cf_manual_solver
with SB(uc=True) as sb:
    url = "https://visa.vfsglobal.com/kaz/en/ltu/login"
    login = get_random_email()
    password = get_password()

    

    sb.activate_cdp_mode(url)
    sb.sleep(10)
    sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
    ##CLOUDFLARE 
    cf_manual_solver(sb)

    ##END CLOUDFLARE
    sb.sleep(1)
    sb.cdp.press_keys("#email", login)
    sb.cdp.press_keys("#password", password)
    sb.sleep(1)
    sb.click(".btn-brand-orange")
    sb.sleep(10)
    sb.cdp.click('button:contains("Start New Booking")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("Application Ce")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Almaty"):not(:contains("Consulate"))')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("appointment category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("others")')
    sb.sleep(5)
    #sb.cdp.click('mat-select:contains("sub")')
    #sb.sleep(1)
    #sb.cdp.click('mat-option:contains("others")')
    #sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    #send_telegram_message("Dates for Visa centre of " +sb.get_text("//mat-select[contains(., 'application')]") + "\n"+dates)
    send_telegram_message("Лит Алм" +"\n" +dates)
    sb.cdp.click('mat-select:contains("center-")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Astana")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("Select your appointment category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Visa C")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("sub")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("others")')
    sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    #send_telegram_message("Dates for Visa centre of " +sb.get_text("//mat-select[contains(., 'application')]") + "\n"+ +dates)
    send_telegram_message("Лит Аст" +"\n" +dates)
    


