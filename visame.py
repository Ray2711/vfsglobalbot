from seleniumbase import SB
from send_msg import send_telegram_message, send_to_db
from solver2captcha import solveCaptcha

def visam() -> None:
    with SB(uc=True, headless2=False) as sb:
        #url = link
        url = "https://kz-appointment.visametric.com/kz"
        sb.activate_cdp_mode(url)
        sb.set_window_size(1280,720)
        sb.uc_gui_click_captcha()
        sb.sleep(4)
        sb.wait_for_element_visible("img.imageCaptcha")
        imgsrc = sb.get_attribute("img.imageCaptcha", "src")
        solve = solveCaptcha(imgsrc)
        
        sb.type('#mailConfirmCodeControl', solve)
        sb.click("#confirmationbtn")
        sb.sleep(3)
        sb.select_option_by_text("#country", "Schengen Visa",timeout=5)
        sb.select_option_by_text("#visitingcountry", "Germany",timeout=5)
        sb.select_option_by_text("#city", "Almaty",timeout=5)
        sb.select_option_by_text("#office", "Almaty",timeout=5)
        sb.select_option_by_text("#officetype", "NORMAL",timeout=5)
        sb.select_option_by_index("#totalPerson", 1,timeout=5)
        dates = sb.cdp.get_text("#drs")
        #print(dates)
        send_telegram_message("Гер Алм " + dates)
        send_to_db("Гер Алм " + dates)
        sb.select_option_by_text("#city", "Astana",timeout=5)
        sb.select_option_by_text("#office", "Astana",timeout=5)
        sb.select_option_by_text("#officetype", "NORMAL",timeout=5)
        sb.select_option_by_index("#totalPerson", 1,timeout=5)
        dates = sb.cdp.get_text("#drs")
       # print(dates)
        send_telegram_message("Гер Аст " + dates)
        send_to_db("Гер Аст " + dates)