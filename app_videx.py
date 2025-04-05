from seleniumbase import SB
from send_msg import send_telegram_message
from random_email import (get_random_email, get_password)
from captcha import cf_manual_solver
with SB(uc=True) as sb:
    url = "https://videx.diplo.de/videx/visum-erfassung/videx-kurzfristiger-aufenthalt"
    sb.activate_cdp_mode(url)
    #sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
    sb.sleep(5)
    sb.cdp.press_keys("#antragsteller\\.familienname", "Ivanov")
    sb.select_option_by_value("#antragsteller\\.geburtsland", "KAZ")
    sb.sleep(10)
    


