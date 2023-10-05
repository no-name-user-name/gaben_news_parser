import io
import os
import time
from pprint import pprint
from time import sleep

import requests
from PIL import Image
from bs4 import BeautifulSoup as bs
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from config import admins
from gaben.bot import get_bot
from gaben.database import DataBase
from gaben.utils import clear_text_format, set_tags, image_to_byte_array, catcherError


class Parser:
    def __init__(self, is_headless=True, profile='main'):
        self.db = DataBase()

        self.s = requests.Session()
        self.s.headers = {}

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

        self.topic_img: str = ''
        self.topic_tags = ''
        self.topic_link: str = ''
        self.topic_name: str = ''
        self.topic_post: str = ''

    def __get_content_request(self, url):
        return bs(self.s.get(url).content, features="html.parser")

    def __get_content_chromedriver(self, url):
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

    def __check_is_old(self, url):
        if self.db.get_news(url) is None:
            self.db.add_news(url)
            return False
        return True

    def start(self):
        self.playisgame(),
        self.goha(),
        self.freesteam(),
        self.coopland(),
        self.coopland('https://coop-land.ru/tags/%E1%E5%F2%E0-%F2%E5%F1%F2/'),
        self.rbkgames(),
        self.vgtimes()
        self.cq(),
        self.pickabu(),
        self.belongplay()

    @catcherError
    def make_post(self, delay=5):
        bot = get_bot()

        if 'data:image' in self.topic_img or self.topic_img == '':
            self.topic_img = open('content/no.png', 'rb')

        elif '.webp' in self.topic_img:
            content = requests.get(self.topic_img).content
            image_bytes = io.BytesIO(content)
            img = Image.open(image_bytes).convert("RGB")
            self.topic_img = image_to_byte_array(img)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('✅', callback_data='post-publish'))

        bot.send_photo(
            chat_id=admins,
            photo=self.topic_img,
            caption=f"{self.topic_tags}\n\n"
                    f"<b>{self.topic_name}</b>\n\n"
                    f"{self.topic_post}\n\n"
                    f"<a href='{self.topic_link}'>[<i>Источник</i>]</a>",
            disable_notification=True,
            reply_markup=markup
        )
        sleep(delay)

    @catcherError
    def playisgame(self, debug=False):
        soup = self.__get_content_request('https://playisgame.com/halyava/')
        items = soup.find("div", class_="pp-posts-skin-news").find_all("div", class_="pp-grid-item-wrap")

        for each in items:
            self.topic_link = each.find('a')['href']
            self.topic_img = each.find('img')['src']
            self.topic_name = clear_text_format(each.find('h2').text)

            if debug:
                topic_soup = self.__get_content_request(self.topic_link)
                topic_post_full = clear_text_format(
                    topic_soup.find('div', class_='elementor-widget-theme-post-content') \
                        .find('div', class_='elementor-widget-container').text)
                self.topic_post = topic_post_full.split('\n')[0]
                self.topic_tags = set_tags(self.topic_name + '\n' + topic_post_full)
                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})
                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                topic_soup = self.__get_content_request(self.topic_link)
                topic_post_full = clear_text_format(
                    topic_soup.find('div', class_='elementor-widget-theme-post-content') \
                        .find('div', class_='elementor-widget-container').text)
                self.topic_post = topic_post_full.split('\n')[0]
                self.topic_tags = set_tags(self.topic_name + '\n' + topic_post_full)
                self.make_post()

    @catcherError
    def goha(self, debug=False):
        soup = self.__get_content_request('https://gamemag.ru/news/tags/halyava')
        items = soup.find("div", class_="news__wrap").find_all("div", class_="news-item")

        for each in items:
            try:
                self.topic_link = 'https://gamemag.ru' + each.find('a', class_='news-item__link')['href']
                self.topic_name = clear_text_format(each.find('a', class_="news-item__text").text)
                topic_post_full = clear_text_format(each.find('div', class_="news-description").text)
                self.topic_post = topic_post_full.split('\n')[0]
                self.topic_img = 'https://gamemag.ru/' + each.find('img', class_='news-item__img')['src']

                if debug:
                    self.topic_tags = set_tags(self.topic_name + topic_post_full)
                    pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                            'topic_img': self.topic_img, 'topic_tags': self.topic_tags})

                    self.make_post()
                    continue

                if not self.__check_is_old(self.topic_link):
                    self.topic_tags = set_tags(self.topic_name + topic_post_full)
                    self.make_post()


            except TypeError:
                print("ERROR GOSHA")
                continue

    @catcherError
    def freesteam(self, debug=False):
        soup = self.__get_content_request('https://freesteam.ru/')
        items = soup.find_all("div", class_="post-box")

        for each in items:
            self.topic_link = each.find('a')['href']
            self.topic_name = clear_text_format(each.find('h2', class_='entry-title').find('a').text)

            if debug:
                topic_soup = self.__get_content_request(self.topic_link)
                topic_post_full = clear_text_format(topic_soup.find('div', class_='entry-content').text)
                self.topic_post = clear_text_format(
                    topic_post_full.replace('Рекламный блок. Sponsored Links.', ' ').split('\n\n')[0])
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.topic_img = topic_soup.find('div', class_='post-thumb').find('img')['data-src']

                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})

                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                topic_soup = self.__get_content_request(self.topic_link)
                topic_post_full = clear_text_format(topic_soup.find('div', class_='entry-content').text)
                self.topic_post = clear_text_format(
                    topic_post_full.replace('Рекламный блок. Sponsored Links.', ' ').split('\n\n')[0])
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.topic_img = topic_soup.find('div', class_='post-thumb').find('img')['data-src']
                self.make_post()

    @catcherError
    def coopland(self, url='https://coop-land.ru/tags/%F0%E0%E7%E4%E0%F7%E0+%EA%EB%FE%F7%E5%E9/', debug=False):
        soup = self.__get_content_request(url)
        items = soup.find_all("article", class_="news")

        for each in items:
            self.topic_link = each.find('a', class_='big-link')['href']
            self.topic_name = clear_text_format(each.find('h2', class_='title').text)
            self.topic_post = clear_text_format(each.find('div', class_='preview-text').text)
            self.topic_tags = set_tags(self.topic_name + self.topic_post)

            if debug:
                topic_soup = self.__get_content_request(self.topic_link)
                self.topic_img = 'https://coop-land.ru' + \
                                 topic_soup.find('div', class_='full-story-content').find('img')['data-src']

                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})

                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                topic_soup = self.__get_content_request(self.topic_link)
                self.topic_img = 'https://coop-land.ru' + \
                                 topic_soup.find('div', class_='full-story-content').find('img')['data-src']
                self.make_post()

    @catcherError
    def rbkgames(self, debug=False):
        soup = self.__get_content_request('https://rbkgames.com/freebie/')
        items = soup.find_all("div", class_="archive-item")

        for each in items:
            self.topic_link = 'https://rbkgames.com' + each.find('a')['href']
            self.topic_name = clear_text_format(each.find('h3').text)
            self.topic_img = 'https:' + each.find('img')['data-src']

            if 'RBK Games' in self.topic_name or 'Акция' in self.topic_name:
                continue

            if debug:
                topic_post_full = clear_text_format(
                    self.__get_content_request(self.topic_link).find('div', class_='content-description').text
                )
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.topic_post = topic_post_full.split('\n')[0]

                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})

                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                topic_post_full = clear_text_format(
                    self.__get_content_request(self.topic_link).find('div', class_='content-description').text
                )
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.topic_post = topic_post_full.split('\n')[0]
                self.make_post()

    @catcherError
    def vgtimes(self, debug=False):
        soup = self.__get_content_chromedriver('https://vgtimes.ru/free/')
        items = soup.find_all("li", class_="hc")

        for each in items:
            self.topic_link = each.find('a')['href']
            self.topic_name = clear_text_format(each.find('span').text)
            self.topic_img = each.find('img')['src']
            self.topic_post = clear_text_format(each.find('div', class_='item-text').text)

            if debug:
                topic_soup = self.__get_content_chromedriver(self.topic_link)
                topic_post_full = clear_text_format(topic_soup.find('div', class_='news_item').text)
                self.topic_tags = set_tags(self.topic_name + topic_post_full)

                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})
                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                topic_soup = self.__get_content_chromedriver(self.topic_link)
                topic_post_full = clear_text_format(topic_soup.find('div', class_='news_item').text)
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.make_post()

    @catcherError
    def cq(self, debug=False):
        soup = self.__get_content_request('https://cq.ru/tags/halyava')
        items = soup.find_all("a", class_="a-item")

        for each in items:
            self.topic_name = clear_text_format(each.find('div', class_='a-item__title').text)
            self.topic_link = each['href']
            self.topic_post = clear_text_format(each.find('div', class_='a-item__excerpt').text)
            self.topic_img = each.find('img')['srcset'].split(' ')[0]

            if debug:
                topic_post_full = clear_text_format(
                    self.__get_content_request(self.topic_link).find('div', class_='post-content').text
                )
                self.topic_tags = set_tags(self.topic_name + topic_post_full)

                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})

                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                topic_post_full = clear_text_format(
                    self.__get_content_request(self.topic_link).find('div', class_='post-content').text
                )
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.make_post()

    @catcherError
    def pickabu(self, debug=False):
        soup = self.__get_content_request('https://pikabu.ru/community/steam')
        items = soup.find_all("div", class_="story__main")

        for each in items:
            self.topic_name = clear_text_format(each.find('h2', class_='story__title').text)

            if each.find('a', class_='story__sponsor') is not None:
                continue

            self.topic_link = each.find('a', class_='story__title-link')['href']
            self.topic_post = clear_text_format(each.find('div', class_='story-block_type_text').text)
            try:
                self.topic_img = each.find('img', class_='story-image__image')['data-src']
            except TypeError:
                self.topic_img = ''

            if debug:
                try:
                    topic_post_full = clear_text_format(
                        self.__get_content_request(self.topic_link).find('div', class_='story__content-inner').text
                    )
                except AttributeError:
                    topic_post_full = self.topic_post
                self.topic_tags = set_tags(self.topic_name + topic_post_full)

                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})

                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                try:
                    topic_post_full = clear_text_format(
                        self.__get_content_request(self.topic_link).find('div', class_='story__content-inner').text
                    )
                except AttributeError:
                    topic_post_full = self.topic_post
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.make_post()

    @catcherError
    def belongplay(self, debug=False):
        soup = self.__get_content_request('https://belongplay.ru/category/freegames/')
        items = soup.find_all("article")

        for each in items:
            self.topic_name = clear_text_format(each.find('h2', class_='entry-title').text)
            self.topic_link = each.find('a')['href']
            self.topic_img = each.find('img')['src']
            self.topic_post = clear_text_format(each.find('div', class_='entry-summary').text)

            if debug:
                topic_post_full = clear_text_format(
                    self.__get_content_request(self.topic_link).find('div', class_='content-area').text
                )
                self.topic_tags = set_tags(self.topic_name + topic_post_full)

                pprint({'topic_name': self.topic_name, 'topic_post': self.topic_post, 'topic_link': self.topic_link,
                        'topic_img': self.topic_img, 'topic_tags': self.topic_tags})

                self.make_post()
                continue

            if not self.__check_is_old(self.topic_link):
                topic_post_full = clear_text_format(
                    self.__get_content_request(self.topic_link).find('div', class_='content-area').text
                )
                self.topic_tags = set_tags(self.topic_name + topic_post_full)
                self.make_post()
