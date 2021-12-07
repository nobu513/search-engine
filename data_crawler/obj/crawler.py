from selenium import webdriver
import os
from dotenv import load_dotenv
import time
from selenium.webdriver.remote.webelement import WebElement


load_dotenv()

class Clawler:
    def __init__(self, start_page=1):
        self.base_url = os.getenv('BASE_URL')
        self.next_page_xpath = '/html/body/nav/div/ul/li[4]/a'
        self.driver: WebElement = webdriver.Firefox()
        self._start_page = start_page

    def load(self):
        self.driver.get(self.base_url)
        input_page_info_path = '/html/body/nav/div/ul/li[3]/form/p[1]/input'
        # どのページから収集をはじめるのか情報を入力する。
        time.sleep(5)
        input_element = self.driver.find_element_by_xpath(input_page_info_path)
        input_element.send_keys(self._start_page)
        input_element.submit()

    def __del__(self):
        time.sleep(4)
        try:
            self.driver.quit()
        except:
            print("ブラウザ終了時にエラーが発生しました。")

    
    def click_element_by_xpath():
        pass

    def image_to_text():
        pass

    def move_to_next_page():
        pass

    def get_date():
        pass

    def get_place():
        pass

    def get_text():
        pass

    def connect_pages():
        pass

    def login():
        pass


