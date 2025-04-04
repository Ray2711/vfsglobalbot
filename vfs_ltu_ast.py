from seleniumbase import SB
from send_msg import send_telegram_message
from random_email import get_random_email

with SB(uc=True) as sb:
    url = "https://visa.vfsglobal.com/kaz/en/ltu/login"
    login = get_random_email()
    password = "Almaty123!"

    info = "Lithuania in Astana"

    
    sb.activate_cdp_mode(url)
    sb.sleep(10)
    sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
    sb.sleep(10)

    # Ввод email и пароля
    sb.cdp.press_keys("#email", login)
    sb.cdp.press_keys("#password", password)

    # Небольшая задержка
    sb.sleep(2)

    # Клик по кнопке входа
    sb.click(".btn-brand-orange")

    sb.sleep(10)

    sb.cdp.click('button:contains("Start New Booking")')

    sb.sleep(5)

    sb.cdp.click('mat-select:contains("Choose your Application Centre")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("Lithuania Visa application center- Almaty")')
    sb.sleep(5)
    sb.cdp.click('mat-select:contains("Select your appointment category")')
    sb.sleep(1)
    sb.cdp.click('mat-option:contains("others")')
    sb.sleep(5)
    #sb.cdp.click('mat-select:contains("Select your appointment category")')
    #sb.sleep(1)
    #sb.cdp.click('mat-option:contains("others)')
    dates = sb.cdp.get_text("div.border-info")
    print(dates)
    sb.sleep(1)
    dates = sb.cdp.get_text("div.border-info")
    send_telegram_message("Dates for Visa centre of "+ info+" " + dates)
    

