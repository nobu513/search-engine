from selenium import webdriver
import os
from dotenv import load_dotenv
import time
from selenium.webdriver.remote.webelement import WebElement
from data_crawler.config.config import BASE_DIR
import pyscreenshot 
import PIL
import easyocr


load_dotenv()

class Clawler:
    def __init__(self, start_page=24):
        self.base_url = os.getenv('BASE_URL')
        self.next_page_xpath = '/html/body/nav/div/ul/li[4]/a'
        self.driver: WebElement = webdriver.Firefox()
        self._start_page = start_page


    def load(self):
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        input_page_info_path = '/html/body/nav/div/ul/li[3]/form/p[1]/input'
        # どのページから収集をはじめるのか情報を入力する。
        time.sleep(5)
        input_element = self.driver.find_element_by_xpath(input_page_info_path)
        input_element.send_keys(self._start_page)
        input_element.submit()

    def __del__(self):
        time.sleep(5)
        try:
            self.driver.quit()
        except:
            print("ブラウザ終了時にエラーが発生しました。")

    def _screenshot(self): 
        """
        bboxで、Mac１６インチの場合の最適な縦横比を求める。
        特に、左のページと右のページを別々に取得することに注意する。
        """
        # # upperは右も左も同じ値。
        upper = 300
        # まずは、左
        pyscreenshot.grab(bbox=(150,upper,150 + 1100, upper + 1650)).save(os.path.join(BASE_DIR, 'images/a.png'))
        # 次に、右
        pyscreenshot.grab(bbox=(1300,upper,1300+1100, upper + 1650)).save(os.path.join(BASE_DIR, 'images/b.png'))


    def image_to_text(self):
        """
        _screenshot()から得た画像をテキストデータにして返す関数。
        以下のような配列がひたすら並ぶ。
        ([[551, 259], [1003, 259], [1003, 301], [551, 301]], "나다. '사람' 하게 되면 남자 여자틀", 0.4922785613501426), 
        2つ目のインデックスに文字列が入るので、とりあえず、そいつらをつなげれば良さげ。
        
        """
        reader = easyocr.Reader(['en', 'ko'])
        bounds = reader.readtext(os.path.join(BASE_DIR, 'images/a.png'))
        text = ""
        for bound in bounds:
            text += str(bound[1])
        print(bounds)
        print("-" * 10)
        print(text)


    def click_element_by_xpath():
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


