from seleniumbase import SB
from send_msg import send_telegram_message

def visam() -> None:
    with SB(uc=True, headless2=False) as sb:
        #url = link
        url = "https://kz-appointment.visametric.com/kz"
        sb.activate_cdp_mode(url)
        sb.set_window_size(1280,720)
        sb.uc_gui_click_captcha()
        sb.sleep(4)
        #sb.wait_for_element_visible("img.imageCaptcha")
        print("aboba")
        print(sb.cdp.get_page_source())
        sb.sleep(30)