import os
import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs


class WebDriver:
    def __init__(self, is_headless, profile):
        temp_dir_path = os.getcwd() + '\\_temp\\' + 'profile_' + profile
        os.makedirs(temp_dir_path, exist_ok=True)
        options = ChromeOptions()
        options.add_argument(f"--user-data-dir={temp_dir_path}")
        if is_headless:
            options.add_argument('--headless')
        options.page_load_strategy = 'eager'
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(5)

    def get_content(self, url) -> bs:
        self.driver.get(url)
        total_page_height = self.driver.execute_script("return document.body.scrollHeight")
        browser_window_height = self.driver.get_window_size(windowHandle='current')['height']

        current_position = self.driver.execute_script('return window.pageYOffset')
        while total_page_height - current_position > browser_window_height:
            self.driver.execute_script(
                f"window.scrollTo({current_position}, {250 + current_position});"
            )
            current_position = self.driver.execute_script('return window.pageYOffset')
            time.sleep(0.01)
        time.sleep(1)
        return bs(self.driver.page_source, features="html.parser")

    def __del__(self):
        if self.driver:
            self.driver.quit()
