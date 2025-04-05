from seleniumbase import SB
from send_msg import send_telegram_message
from random_email import (get_random_email, get_password)
with SB(uc=True) as sb:
    url = "https://visa.vfsglobal.com/kaz/en/ita/login"
    login = get_random_email()
    password = get_password()

    

    sb.activate_cdp_mode(url)
    sb.sleep(10)
    sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
    ##CLOUDFLARE 
    sb.sleep(2)  # подстраховка

    try:
        # Переключаемся в iframe по частичному URL
        frames = sb.driver.find_elements("tag name", "iframe")
        for frame in frames:
            src = frame.get_attribute("src")
            if src and "https://challenges.cloudflare.com/cdn-cgi" in src:
                sb.driver.switch_to.frame(frame)
                break

        # Ждём появления элемента .mark и кликаем по нему
        sb.wait_for_element_visible(".cb-c", timeout=5)
        sb.sleep(15)  # Cloudflare задержка
        sb.click(".cb-c")

        sb.driver.switch_to.default_content()

    except Exception as e:
        print("Cloudflare challenge not found or failed:", e)


    ##END CLOUDFLARE
    sb.sleep(5)
    sb.cdp.press_keys("#email", login)
    sb.cdp.press_keys("#password", password)
    sb.sleep(2)
    sb.click(".btn-brand-orange")
    sb.sleep(10)
    sb.cdp.click('button:contains("Start New Booking")')
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
    send_telegram_message("Dates for Visa centre of " +sb.get_text("//mat-select[contains(., 'Application Ce')]") + "\n" + dates)
    sb.cdp.click('mat-select:contains("Application Ce")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Astana")')
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
    send_telegram_message("Dates for Visa centre of " +sb.get_text("//mat-select[contains(., 'Application Ce')]") + "\n"+ + dates)
    


