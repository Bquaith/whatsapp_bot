from typing import Tuple
from typing import Optional

from random import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mini_lib import generate_qr_code
from mini_lib import is_phone_number

import env

class WhatsappBot():
    browser: webdriver.Chrome
    _use_prof: bool
    _chrome_options: Options

    def __init__(self, use_prof = True, headless = False):
        self.use_prof = use_prof
        self._chrome_options = Options()
        self._chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        if self.use_prof:
            self._chrome_options = Options()
            self._chrome_options.add_argument(f"user-data-dir={env.PATH_TO_PROF}")  # Указываем путь к профилю
            self._chrome_options.add_argument("profile-directory=Default") 
        if headless:
            self._chrome_options.add_argument("--headless")
            

    def open(self, auth = False) -> bool:
        self.browser = webdriver.Chrome(options=self._chrome_options)
        self.browser.get('https://web.whatsapp.com/')

        if auth:
            for i in range(env.TRY_AUTH):
                print(f"Try {i}/{env.TRY_AUTH}")
                # Checking whether the authorization page is open or not 
                if self.find_default_homepage_element():
                    return True
                if not self.get_qr_auth():
                    break
                sleep(env.TRY_AUTH_SLEEP)
            else:
                return False

        if self.waiting_appear_object((By.CSS_SELECTOR, '[data-icon="new-chat-outline"]'), env.LOAD_HOME_PAGE):
            return True
        return False
    
    def close(self):
        self.browser.quit()

    def find_default_homepage_element(self):
        return self.waiting_appear_object((By.CSS_SELECTOR, '[data-icon="new-chat-outline"]'), env.LOAD_HOME_PAGE)

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

    def waiting_appear_object(self, element: Tuple[str, str], timeout=10) -> Optional[WebElement]:
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(element)
            )
            print(f"Element {element} appeared")
            return self.browser.find_element(*element)
        except:
            print(f"Element {element} dont appeared in the allotted time")
            return None
        
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
        
    def open_known_recipient(self, user_name: str) -> bool:
        if not self.waiting_appear_object((By.CSS_SELECTOR, '[data-icon="new-chat-outline"]')):
            return False
        
        # Find search icon where we can find users in home page
        search = self.browser.find_element(By.CSS_SELECTOR, 'span[data-icon="search"]')
        search.click()
        sleep(env.MAGIC_SLEEP)

        # Place for finding users in home page
        write_place = self.browser.find_element(By.CSS_SELECTOR, 'p[class="selectable-text copyable-text x15bjb6t x1n2onr6"]')
        for i in user_name:
            write_place.send_keys(i)
            sleep(random())

        if not is_phone_number(user_name):
            # Find user in table
            element = self.browser.find_element(By.XPATH, f'//span[@dir="auto" and @title="{user_name}"]')
            if element:
                element.click()
                return True
            return False
        else:
            # Searches for the first occurrence by number
            element = self.browser.find_element(By.CSS_SELECTOR, 'div[role="gridcell"]')
            if element:
                element.click()
                return True
            return False
        
    def open_user_by_number(self, user_phone: str, massage = "") -> bool:
        # Open user using whatsapp api and if we wont, send massage
        self.browser.get(f"https://web.whatsapp.com/send?phone={user_phone}&text={massage}")
        if not self.find_default_homepage_element():
            return False

        if massage:
            element = self.waiting_appear_object((By.CSS_SELECTOR, 'span[data-icon="send"]'))
            if element:
                element.click()

        return True

    def send_text(self, massage: str):
        # There are two identical tags on the page for prompting users and for sending messages.
        write_place = self.browser.find_elements(By.CSS_SELECTOR, 'p[class="selectable-text copyable-text x15bjb6t x1n2onr6"]')[1]
        for i in massage:
            write_place.send_keys(i)
            sleep(random())

        element = self.waiting_appear_object((By.CSS_SELECTOR, 'span[data-icon="send"]'))
        if element:
            element.click()