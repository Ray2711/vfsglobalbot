import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cf_manual_solver(sb) -> None:
    driver = sb.driver  # Get raw WebDriver instance from SeleniumBase
    captcha_frame_regex = re.compile(r'cf-chl-widget-.{3,6}')

    try:
        matching_elements = driver.find_elements(By.XPATH, "//*[contains(@id, 'cf-chl-widget-')]")
        for element in matching_elements:
            element_id = element.get_attribute("id")
            if captcha_frame_regex.match(element_id) and 'Cloudflare security challenge' in element.accessible_name:
                cf_captcha_frame = element
                break
        else:
            print("⚠️ Captcha iframe not found.")
            return

        WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it(cf_captcha_frame))
        captcha_checkbox = driver.find_element(By.CLASS_NAME, 'ctp-checkbox-label')
        captcha_checkbox.click()
        driver.switch_to.default_content()
        print("✅ Captcha checkbox clicked.")
        
    except Exception as err:
        print("❌ CAPTCHA solving failed:", err)
