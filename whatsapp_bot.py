from typing import Tuple

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from qr_gen import generate_qr_code

import env

class WhatsappBot():
    browser: webdriver.Chrome

    def __init__(self):
        pass

    def open(self, auth = False) -> bool:
        self.browser = webdriver.Chrome()
        self.browser.get('https://web.whatsapp.com/')

        if auth:
            for i in range(env.TRY_AUTH):
                print(f"Try {i}/{env.TRY_AUTH}")
                # Checking whether the authorization page is open or not 
                if self.waiting_appear_object((By.CSS_SELECTOR, '[data-icon="new-chat-outline"]')):
                    return True
                if not self.get_qr_auth():
                    break
                sleep(env.TRY_AUTH_SLEEP)
            else:
                return False

        if self.waiting_appear_object((By.CSS_SELECTOR, '[data-icon="new-chat-outline"]'), env.LOAD_HOME_PAGE):
            return True
        return False

    def get_qr_auth(self) -> bool:
        
        if self.waiting_appear_object((By.TAG_NAME, 'circle',)):
            if not self.waiting_disappear_object((By.TAG_NAME, 'circle',)):
                return False

        # Find data ref for gen qr code
        data_ref_value = None
        try:
            element = self.browser.find_element(By.CSS_SELECTOR, 'div[data-ref]')
            data_ref_value = element.get_attribute("data-ref")
            print(data_ref_value)
        except Exception as e:
            print(str(e))
            return False

        if data_ref_value:
            generate_qr_code(data_ref_value)
            return True
        return False

    def waiting_appear_object(self, element: Tuple[str, str], timeout=10) -> bool:
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(element)
            )
            print(f"Element {element} appeared")
            return True
        except:
            print(f"Element {element} dont appeared in the allotted time")
            return False
        
    def waiting_disappear_object(self, element: Tuple[str, str], timeout=10) -> bool:
        try:
            circle = self.browser.find_element(*element)
            WebDriverWait(self.browser, timeout).until(
                EC.invisibility_of_element_located(circle)
            )
            print(f"Element {element} is gone")
            return True
        except:
            print(f"Element {element} dont disappeared in the allotted time or is he gone")
            return False