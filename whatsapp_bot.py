from typing import Tuple

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from qr_gen import decode_qr_from_base64
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
                print(f"Попытка {i}/{env.TRY_AUTH}")
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

        # Находим элемент canvas
        try:
            canvas = self.browser.find_element(By.TAG_NAME, 'canvas')
        except Exception as e:
            print(str(e))
            return False

        qr_code_data = decode_qr_from_base64(canvas.screenshot_as_base64)
        print(qr_code_data)
        generate_qr_code(qr_code_data)
        return True

    def waiting_appear_object(self, element: Tuple[str, str], timeout=10) -> bool:
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(element)
            )
            print(f"Элемент {element} появился")
            return True
        except:
            print(f"Элемент {element} не появился за отведенное время")
            return False
        
    def waiting_disappear_object(self, element: Tuple[str, str], timeout=10) -> bool:
        try:
            circle = self.browser.find_element(*element)
            WebDriverWait(self.browser, timeout).until(
                EC.invisibility_of_element_located(circle)
            )
            print(f"Элемент {element} исчез")
            return True
        except:
            print(f"Элемент {element} не исчез за отведенное время или его нет")
            return False