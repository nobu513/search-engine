# -*- coding: utf-8 -*-

from selenium import webdriver
import os
from dotenv import load_dotenv
import time
from selenium.webdriver.remote.webelement import WebElement
from data_crawler.config.config import BASE_DIR
from bs4 import BeautifulSoup
import requests
from data_crawler.common_utils.columns import BOOK_COLUMNS
import re

load_dotenv()

class Clawler: 
    def __init__(self, start_page=0, end_page=2): # start, endは偶数指定に統一する。結局奇数にしたところで偶数ページも一緒に読み込むため。
        self.base_url = os.getenv('BASE_URL')
        self.next_page_xpath = '/html/body/nav/div/ul/li[4]/a'
        # self.driver: WebElement = webdriver.Firefox()
        self._start_page = start_page
        self._end_page = end_page
        self.regex_page_num = re.compile(r"[0-9]+$")
        self.regex_num = re.compile(r"[0-9]+")
        self.regex_book_num = re.compile(r"제[0-9]+편")
        self.regex_num_and_dot = re.compile(r"[0-9]+\.") # ex) 1.        


    def load(self):
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        input_page_info_path = '/html/body/nav/div/ul/li[3]/form/p[1]/input'
        # どのページから収集をはじめるのか情報を入力する。
        time.sleep(5)
        input_element = self.driver.find_element_by_xpath(input_page_info_path)
        input_element.send_keys(self._start_page)
        input_element.submit()

    def start_crawler(self):
        records = []
        cur_book_title = "" # 現在の篇タイトル
        cur_chapter_title = "" # 現在の章タイトル

        for page_num in range(self._start_page, self._end_page+2, 2): # 偶数、奇数ページを見開き一ページにして取得するので１つ飛ばしする。
            """
            BOOK_COLUMNS = (
                "book",
                "chapter_title",
                "sub_title",
                "doc",
                "place",
                "posted_at",
                "convention_name",
                "author",
                "page",
                "img_url",
            )
            """
            record = dict.fromkeys(BOOK_COLUMNS)
            res = requests.get(self.base_url+str(page_num)).text
            bs = BeautifulSoup(res, "html.parser")
            # 左側のページに篇タイトルがある。
            left_content = self._clean_text(bs.find("div", id="smcaltsR").p.text.replace('\xeb', "\'"))
            book_title = ""
            # 右側のページに章タイトルがある。
            # また、右側の文字数が急に小さくなることを基準にして（大体５１文字くらい）
            # book_titleを変える。
            # また、場所、日にちなどの情報をもとにしてChapterのはじまるページであることを探知して、
            # chapter_titleも其のタイミングで変える。
            right_content = self._clean_text(bs.find("div", id="smcaltsL").p.text)
            chapter_title = ""
    
    def _clean_text(self, text):
        """
        変な文字コードをなくしていく。今の所遭遇したやつ↓
        ・シングルクオーテーションのへんてこバージョン\xeb
        """
        text = text.replace("\xeb", "\'")
        text = text.replace("\xea", "\'")

        return text

    def _is_top_of_chapter(self, text):
        """
        날짜, 장소などが存在していることを目印に、章のはじまりのページであるかを判断する。
        """
        if "날 짜" in text and "장 소" in text and "행 사" in text:
            return True

    def _is_top_of_book(self, text):
        """
        主に右側ページの文字数によって、篇の変わり目であるかを取得する。
        右側のページかつ、１８ページ以上１６３２ページ以下であるならば、この条件だけで特定できる。
        """
        if len(text) <= 100:
            return True
        return False

    def _get_book_title(self, text):
        """
        _is_top_of_bookがTrueの時に使う。
        例↓
        17페이지 내용 : 제1편 참평화의 근본원리 1 __ 13. 5. 16. 343 Page17
        """
        # まず、篇の番号を取得する。例の場合は１。
        book_num_str = self.regex_book_num.search(text).group() # ex) 제1편
        book_num = self.regex_num.search(book_num_str).group() # ex) 1
        # 次に、これらの情報をもとにSplitしながら篇のタイトルを取得していく。
        book_title = text.split(book_num_str)[1].split(book_num)[0].strip()
        return book_title

    def _get_chapter_titles(self, text):
        """以下のデータから、リストの中にタイトルだけ格納したい。
        18페이지 내용 : 1. 하나님과 인간을 위한 이상세계 ……………… 19 2. 인간에 대한 하나님의 소망 …………………… 32 3. 위하여 사는 세계………………………………… 53 4. 인류의 새로운 장래……………………………… 71 5. 위하여 사는 생애………………………………… 86 6. 참평화의 근본원리 ……………………………… 96 7. 참다운 평화세계 ……………………………… 104 8. 구원섭리사의 원리관 ………………………… 112 9. 하나님의 조국광복 …………………………… 127 10. 하나님과 인류가 찾아가는 평화의 나라와 세계…………………………… 137 11. 벅찬 감사와 사랑을 담아 …………………… 148 12. 평화의 근원은 하나님………………………… 153 13. 하나님의 조국과 하나의 세계 ……………… 168 14. 하나님과 평화통일세계 ……………………… 178 15. 하나님의 조국과 평화왕국시대……………… 188 16. 위하여 사는 생활로 평화세계 창건하자 …… 195 | 차 례 | 제1편 참평화의 근본원리 1 __ 13. 5. 16. 343 Page18"""
        chapter_titles = []
        text = self._clean_text(text)
        text = text.split("…")
        text = list(filter(lambda x: len(x) > 1, text))
        text = text[:-1]

        for item in text:
            num_and_dot = self.regex_num_and_dot.search(item).group()
            title = item.split(num_and_dot)[1].strip()
            chapter_titles.append(title)

        return chapter_titles
        
        

    def _get_page_num(self, text):
        """
        本文Page22
        みたいに、ページの情報はきまって最後の最後にある。
        """
        return self.regex_page_num.search(text).group()

    def _remove_meta_info(self, text, chapter_title, chapter_num):
        """
        あとでページ同士をつなげることを考えて、前後のメタ情報（ページ数、篇タイトル、章タイトル）
        を取り除いておく。対象は以下の通り。

        >> 毎ページはじめにある
        19페이지 내용 : 

        >> 毎ページおわりにある
        1 __ 16. 4. 1. 636 Page25

        >> 章のはじめのページの終わりにある
        19 하나님과 인간을 위한 이상세계 1 날 짜 1972년 2월 4일 장 소 미국 뉴욕 Lincoln Center 행 사 미국·유럽 9개 도시 순회강연 1 __ 16. 4. 1. 630 Page19

        >> 普段のページの終わりにある
        1. 하나님과 인간을 위한 이상세계 25 1 __ 16. 4. 1. 636 Page25
        """        
        page_num = self._get_page_num(text)
        text = text.split(":", 1)[1] # ex) 19페이지 내용 : 

        page_dot_chaptertitle = str(chapter_num) + ". " + chapter_title
        text = text.split(page_dot_chaptertitle)[0]

        page_and_chapter_title = str(page_num) + " " + chapter_title
        text = text.split(page_and_chapter_title)[0]

        return text.strip()



