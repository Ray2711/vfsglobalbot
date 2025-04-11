from seleniumbase import SB
from captcha import cf_manual_solver
from send_msg import send_telegram_message
from random_email import get_random_email
with SB(uc=True) as sb:
    url = "https://visa.vfsglobal.com/kaz/en/fra/login"
    login = get_random_email()
    password = "Almaty123!"


    sb.activate_cdp_mode(url)
    sb.sleep(10)
    sb.cdp.click_if_visible("#onetrust-accept-btn-handler")

    ##CLOUDFLARE 
    cf_manual_solver(sb)

    ##END CLOUDFLARE
    sb.cdp.press_keys("#email", login)
    sb.cdp.press_keys("#password", password)
    sb.sleep(2)
    sb.click(".btn-brand-orange")
    sb.sleep(20)
    sb.cdp.click('button:contains("Start New Booking")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("Application Centre")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Almaty")')
    sb.sleep(5)
    #sb.cdp.click('mat-select:contains("appointment category")')
    #sb.sleep(1)
    #sb.cdp.click('mat-option:contains("Short")')
    #sb.sleep(5)
    sb.cdp.click('mat-select:contains("sub-category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Short Stay")')
    sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    #send_telegram_message("Dates for Visa centre of " +sb.get_text("//mat-select[contains(., 'Application Ce')]") +"\n" +dates)
    send_telegram_message("Фра Алм " +"\n" +dates)
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("Application Centre")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Astana")')
    sb.sleep(5)
    #sb.cdp.click('mat-select:contains("appointment category")')
    #sb.sleep(1)
    #sb.cdp.click('mat-option:contains("Short")')
    #sb.sleep(5)
    sb.cdp.click('mat-select:contains("sub-category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Short Stay")')
    sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    #send_telegram_message("Dates for Visa centre of " +sb.get_text("#mat-select-0") +"\n" +dates)
    send_telegram_message("Фра Аст " +"\n" +dates)


