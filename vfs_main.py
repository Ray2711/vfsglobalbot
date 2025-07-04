from seleniumbase import SB
from csv_create import append_to_csv
from send_msg import (send_telegram_message, send_telegram_message_error, send_telegram_message_ping, send_to_db)
from random_email import (get_random_email, get_password)
 

def vfs_checkdates(link,city1,city2,abb1,abb2, isImportant: bool , isImportant2: bool) -> None:
    try:
        with SB(uc=True, headless2=False) as sb:
            url = link
            login = get_random_email()
            password = get_password()
            sb.execute_cdp_cmd("Network.clearBrowserCache", {})

            

            sb.activate_cdp_mode(url)
            sb.set_window_size(1280,720)
            sb.sleep(15)
            sb.cdp.click_if_visible("#onetrust-accept-btn-handler")
            ##CLOUDFLARE 
            #cf_manual_solver(sb)
            sb.uc_gui_click_captcha()
            ##END CLOUDFLARE
            sb.sleep(1)
            sb.cdp.press_keys("#email", login)
            sb.cdp.press_keys("#password", password)
            sb.sleep(1)
            sb.click(".btn-brand-orange")
            sb.sleep(10)
            sb.minimize_window()
            
            sb.cdp.click('button:contains("Start New Booking")')
            sb.sleep(5)
            app_el = sb.cdp.find_element('mat-select:contains("pplication")')
            cat_el = sb.cdp.find_element('mat-select:contains("appointment category")')
            sub_el = sb.cdp.find_element('mat-select:contains("sub")')
            #Select city 1
            app_el.click()
            sb.sleep(1)
            #sb.cdp.click(f'mat-option:contains("{city1}"):not(:contains("Consulate")):not(:contains("Embassy"))')
            sb.click_xpath(f'//mat-option[not(contains(., "Consulate")) and not(contains(., "Embassy")) and not(contains(., "Embassy-Astana")) and contains(., "{city1}")]')
            sb.sleep(5)
            #sb.cdp.click('mat-select:contains("appointment category")')
            cat_el.click()
            sb.sleep(1)
            options = ["others", "Short", "Visa C", "Visa", "Czech_Kazakhstan" ]

            for option in options:
                try:
                    sb.cdp.click(f'mat-option:contains("{option}")',timeout=2)
                    print(f"Selected option: {option}")
                    break
                except Exception as e:
                    print(f"Failed to select option '{option}': {e}")

            sb.sleep(5)
            #sb.cdp.click('mat-select:contains("sub")')
            sub_el.click()
            subs = ["Tourist", "Short", "Other", "other", "Visa C", "Visa" ]

            for option in subs:
                try:
                    sb.cdp.click(f'mat-option:contains("{option}")',timeout=2)
                    print(f"Selected option: {option}")
                    break
                except Exception as e:
                    print(f"Failed to select option '{option}': {e}")
            sb.sleep(1)
            dates = sb.cdp.get_text("div.border-info")
            #send_telegram_message("Dates for Visa centre of " +sb.get_text("//mat-select[contains(., 'application')]") + "\n"+dates)
            
            if isImportant:
                send_telegram_message_ping(abb1 +"\n" +dates)
            else:
                send_telegram_message(abb1 +"\n" +dates)
            send_to_db(abb1 +"\n" +dates)
            append_to_csv(abb1,dates)
            #Select city 2
            app_el.click()
            sb.sleep(1)
            sb.cdp.click(f'mat-option:contains("{city2}"):not(:contains("Consulate"))')
            sb.sleep(5)
            #sb.cdp.click('mat-select:contains("appointment category")')
            cat_el.click()
            sb.sleep(1)
            options = ["others", "Short", "Visa C","Czech_Kazakhstan" ]

            for option in options:
                try:
                    sb.cdp.click(f'mat-option:contains("{option}")',timeout=2)
                    print(f"Selected option: {option}")
                    break
                except Exception as e:
                    print(f"Failed to select option '{option}': {e}")

            sb.sleep(5)
            #sb.cdp.click('mat-select:contains("sub")')
            sub_el.click()
            subs = ["Tourist", "Short", "Other", "other", "Visa C" , "Schengen" ]

            for option in subs:
                try:
                    sb.cdp.click(f'mat-option:contains("{option}")',timeout=2)
                    print(f"Selected option: {option}")
                    break
                except Exception as e:
                    print(f"Failed to select option '{option}': {e}")
            sb.sleep(1)
            dates = sb.cdp.get_text("div.border-info")
            
            if isImportant2:
                send_telegram_message_ping(abb2 +"\n" +dates)
            else:
                send_telegram_message(abb2 +"\n" +dates)
            send_to_db(abb2 +"\n" +dates)
            append_to_csv(abb2,dates)
    except Exception as e:
        send_telegram_message_error(f"Error in : {link} : \n Couldn't get dates " )


