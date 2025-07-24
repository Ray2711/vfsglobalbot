from seleniumbase import SB
from seleniumbase.fixtures.page_actions import wait_for_element_visible
import imap
import asyncio
import nest_asyncio
import os
from dotenv import load_dotenv
import pyautogui
import random
import time

from random_email import get_random_email, get_password
from send_msg import send_telegram_message, send_telegram_message_error
from send_to_fb import send_to_firestore

load_dotenv()

async def task(link,city1,abb1,country):
        with SB(uc=True, headless2=False,port=9222) as sb:
                url = link
                login = get_random_email()
                password = get_password()
                sb.activate_cdp_mode(url)
                sb.set_window_size(1280,720)
                sb.wait_for_element_visible("#onetrust-accept-btn-handler")
                sb.cdp.click("#onetrust-accept-btn-handler")
                sb.wait_for_element_visible("#email")
            ##CLOUDFLARE 
            #cf_manual_solver(sb)
            
            ##END CLOUDFLARE
                sb.sleep(1)
                sb.maximize_window()
                loggedin = False
        
                while(loggedin == False):
                        try:
                                sb.cdp.press_keys("#email", login)
                                sb.cdp.press_keys("#password", password)
                                sb.sleep(6)
                                #sb.minimize_window()
                                sb.uc_gui_click_captcha()
                                pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y - 10, duration=random.uniform(0.1, 0.3), tween=pyautogui.easeOutQuad)
                                time.sleep(random.uniform(0.05, 0.15))
                                pyautogui.click()
                                sb.sleep(5)
                                sb.cdp.click(".btn-brand-orange")
                                sb.sleep(10)
                                loggedin = True
                        except:
                                sb.cdp.gui_click_element("a.c-brand-orange")
                                pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y - 10, duration=random.uniform(0.1, 0.3), tween=pyautogui.easeOutQuad)
                                time.sleep(random.uniform(0.05, 0.15))
                                pyautogui.click()
                                sb.sleep(10)
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
                sb.sleep(5)
                sb.cdp.click('button:contains("Continue")')
                sb.sleep(10)

                #DOING THE ZAPIS PART
                count = 0
                
                sb.type('[placeholder*="FIRST NAME" i]', 'NUUSIKKD')
                sb.type('[placeholder*="LAST NAME" i]', 'DSGLSLDLFL')
                sb.type('[placeholder*="PASSPORT NUMBER" i]', 'N23323234')

                mat_selects = sb.find_elements('mat-select')

                try:    
                        
                        #sb.click_xpath(
                        #'(//div[div[contains(normalize-space(.), "Current Nationality")]]//mat-select)[1]'
                        #)
                        mat_selects[0].click()
                        sb.click(f'mat-option:contains("M")',timeout=2)
                        mat_selects[1].click()
                        sb.click(f'mat-option:contains("KAZAKHSTAN")',timeout=2)
                except Exception as e:
                        
                        print(e)
                        mat_selects[0].click()
                        sb.cdp.click(f'mat-option:contains("KAZAKHSTAN")',timeout=2)
                        
                

                sb.type('[placeholder*="44" i]', "7")
                sb.type('[placeholder*="0123456" i]', "77777777777")
                sb.type('[placeholder*="EMAIL" i]', "test@test.com")
                

                try:
                    #  #     sb.click_xpath('//div[div[contains(normalize-space(.), "Gender")]]//mat-select')
                        #  sb.cdp.click(f'mat-option:contains("{applicant['gender']}")',timeout=2)
                        sb.send_keys("#dateOfBirth", "01/01/1990")
                        sb.send_keys("#passportExpirtyDate", "01/01/2035")
                except Exception as e:
                        print(e)
                
                
                
                sb.sleep(30)

                sb.click('button:contains("Save")')
                                
                sb.sleep(10)

                #If alls done then continue

                sb.click('button:contains("Continue")')
                sb.sleep(10)

                #try OTP getting
                try:
                        sb.cdp.click('button:contains("OTP")')

                        OTP = imap.main(country,10)
                        
                        sb.type("input", OTP)
                        sb.cdp.click('button:contains("Verify")')
                        sb.sleep(10)
                        sb.cdp.click('button:contains("Continue")')
                        sb.sleep(10)
                except Exception as e:
                        print("error on OTP")
                        print(e)    
                ##
               
                available_dates_elements = sb.find_elements('.date-availiable')
                available_dates = []
                for el in available_dates_elements:
                    date_attr = el.get_attribute('data-date')
                    if date_attr:
                        available_dates.append(date_attr)
                available_dates_str = "Available Dates: " + ", ".join(available_dates)
                print(available_dates_str)
                send_telegram_message_error(abb1 + " "+available_dates_str)
                send_to_firestore("list_appointment_dates","vfs",abb1,available_dates_str)
               
                sb.sleep(30)


if __name__ == "__main__":
        nest_asyncio.apply()
        while True:
                asyncio.run(task("https://visa.vfsglobal.com/kaz/en/ltu/login","Astana","Лит Аст","ltu"))