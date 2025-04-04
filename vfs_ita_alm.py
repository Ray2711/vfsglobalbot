from seleniumbase import SB
 
from send_msg import send_telegram_message
with SB(uc=True) as sb:
    url = "https://visa.vfsglobal.com/kaz/en/ita/login"
    login = "nurasyl.tagayev@bk.ru"
    password = "Almaty123!"

    info = "Italy in Almaty"

    sb.activate_cdp_mode(url)
    sb.sleep(10)
    sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
    sb.sleep(5)
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
    sb.cdp.click('mat-select:contains("appointment category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Short")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("sub-category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Tourist")')
    sb.sleep(5)
    dates = sb.cdp.get_text("div.border-info")
    send_telegram_message("Dates for Visa centre of"+ info+" " + dates)



