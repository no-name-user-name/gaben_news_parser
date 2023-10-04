import os
from time import sleep

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import admins
from gaben.bot import get_bot
from gaben.database import DataBase
from gaben.utils import clear_text_format, set_tags


class Parser:
    def __init__(self):
        self.db = DataBase()

        self.s = requests.Session()
        self.s.headers = {}

        # options = uc.ChromeOptions()
        # prof_id = '1'
        # path = f'_temp/profile{prof_id}'
        # options.add_argument(f'--user-data-dir={os.path.abspath(path)}')
        # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-popup-blocking")
        # options.page_load_strategy = 'eager'
        # options.add_argument('--disable-gpu')
        # options.headless = True
        # self.driver = uc.Chrome(options=options)

        self.topic_img: str = ''
        self.topic_tags = ''
        self.topic_link: str = ''
        self.topic_name: str = ''
        self.topic_post: str = ''

    def __get_content_request(self, url):
        html = self.s.get(url).content
        soup = bs(html, features="html.parser")
        return soup

    # def __get_content_chrome(self, url):
    #     self.driver.get(url)
    #     html = self.driver.page_source
    #     soup = bs(html, features="html.parser")
    #     return soup

    def __check_is_old(self, url):
        if self.db.get_news(url) is None:
            return False
        return True

    def start(self):
        self.igromania(),
        self.playisgame(),
        self.goha(),
        self.freesteam(),
        self.coopland(),
        self.coopland('https://coop-land.ru/tags/%E1%E5%F2%E0-%F2%E5%F1%F2/'),
        self.rbkgames(),
        self.cq(),

    def make_post(self, delay=5):
        bot = get_bot()

        if 'data:image' in self.topic_img:
            self.topic_img = open('content/no.png', 'rb')

        elif '.webp' in self.topic_img:
            self.topic_img = open('content/no.png', 'rb')

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('✅', callback_data='post-publish'))

        bot.send_photo(
            chat_id=admins,
            photo=self.topic_img,
            caption=f"{self.topic_tags}\n\n"
                    f"<b>{self.topic_name}</b>\n"
                    f"{self.topic_post}\n\n"
                    f"<a href='{self.topic_link}'>[<i>Источник</i>]</a>",
            disable_notification=True,
            reply_markup=markup
        )
        sleep(delay)

    def igromania(self):
        soup = self.__get_content_request('https://www.igromania.ru/news/sale/')
        items = soup.find_all("div", class_="aubl_item")

        for each in items:
            topic_link = 'https://www.igromania.ru' + each.find('a', class_="aubli_img")['href']
            topic_name = each.find('a', class_="aubli_name").text + '\n'
            topic_desc = each.find('div', class_="aubli_desc").text

            if not self.__check_is_old(topic_link):
                self.db.add_news(url=topic_link)

                topic_html = requests.get(topic_link).content
                topic_soup = bs(topic_html, features="html.parser")
                topic_post = topic_soup.find('div', class_='universal_content')
                topic_post.find('div', class_='uninote').decompose()
                topic_post = clear_text_format(topic_post.text)
                topic_img = topic_soup.find('div', class_='main_pic_container').find('img')['src']

                self.topic_tags = set_tags(topic_name + '\n' + topic_post)
                self.topic_post = topic_desc
                self.topic_name = topic_name
                self.topic_link = topic_link
                self.topic_img = topic_img
                self.make_post()

    def playisgame(self):
        soup = self.__get_content_request('https://playisgame.com/halyava/')
        items = soup.find("div", class_="pp-posts-skin-news").find_all("div", class_="pp-grid-item-wrap")

        for each in items:
            topic_link = each.find('a')['href']
            topic_img = each.find('img')['src']
            topic_name = clear_text_format(each.find('h2').text)
            # topic_desc = each.find('div', class_="pp-post-excerpt").text

            if not self.__check_is_old(topic_link):
                self.db.add_news(topic_link)

                topic_html = requests.get(topic_link).content
                topic_soup = bs(topic_html, features="html.parser")
                topic_post = topic_soup.find('div', class_='elementor-widget-theme-post-content').find(
                    'div', class_='elementor-widget-container')

                try:
                    topic_post.find('figure').decompose()
                except:
                    pass

                topic_post = '\n' + clear_text_format(topic_post.text).split('\n')[0]

                self.topic_tags = set_tags(topic_name + '\n' + topic_post)
                self.topic_post = topic_post
                self.topic_name = topic_name
                self.topic_link = topic_link
                self.topic_img = topic_img
                self.make_post()

    def goha(self):
        soup = self.__get_content_request('https://gamemag.ru/news/tags/halyava')
        items = soup.find("div", class_="news__wrap").find_all("div", class_="news-item")

        for each in items:
            try:
                topic_link = 'https://gamemag.ru' + each.find('a', class_='news-item__link')['href']
                topic_name = clear_text_format(each.find('a', class_="news-item__text").text)
                topic_desc = each.find('div', class_="news-description").text
                topic_img = 'https://gamemag.ru/' + each.find('img', class_='news-item__img')['src']

                if not self.__check_is_old(topic_link):
                    self.db.add_news(topic_link)

                    self.topic_tags = set_tags(topic_name + topic_desc)
                    self.topic_post = '\n' + clear_text_format(topic_desc).split('\n')[0]
                    self.topic_name = topic_name
                    self.topic_link = topic_link
                    self.topic_img = topic_img
                    self.make_post()


            except TypeError:
                print("ERROR GOSHA")
                continue

    def freesteam(self):
        soup = self.__get_content_request('https://freesteam.ru/')
        items = soup.find_all("div", class_="post-box")

        for each in items:
            topic_link = each.find('a')['href']
            topic_name = clear_text_format(each.find('h2', class_='entry-title').find('a').text)

            if not self.__check_is_old(topic_link):
                self.db.add_news(topic_link)
                topic_html = requests.get(topic_link).content
                topic_soup = bs(topic_html, features="html.parser")
                topic_post = topic_soup.find('div', class_='entry-content').text
                topic_post = clear_text_format(topic_post)
                split_post = '\n' + topic_post.replace('Рекламный блок. Sponsored Links.', ' ').split('\n\n')[0]
                topic_img = topic_soup.find('div', class_='post-thumb').find('img')['data-src']

                self.topic_tags = set_tags(topic_name + topic_post)
                self.topic_post = split_post
                self.topic_name = topic_name
                self.topic_link = topic_link
                self.topic_img = topic_img
                self.make_post()

    def coopland(self, url='https://coop-land.ru/tags/%F0%E0%E7%E4%E0%F7%E0+%EA%EB%FE%F7%E5%E9/'):
        soup = self.__get_content_request(url)
        items = soup.find_all("article", class_="news")

        for each in items:
            topic_link = each.find('a', class_='big-link')['href']
            topic_name = clear_text_format(each.find('h2', class_='title').text)
            topic_desc = '\n' + clear_text_format(each.find('div', class_='preview-text').text)

            if not self.__check_is_old(topic_link):
                self.db.add_news(topic_link)
                topic_html = requests.get(topic_link).content
                topic_soup = bs(topic_html, features="html.parser")
                topic_img = 'https://coop-land.ru' + topic_soup.find('div', class_='full-story-content').find('img')[
                    'data-src']

                self.topic_tags = set_tags(topic_name + topic_desc)
                self.topic_post = topic_desc
                self.topic_name = topic_name
                self.topic_link = topic_link
                self.topic_img = topic_img
                self.make_post()

    def rbkgames(self):
        soup = self.__get_content_request('https://rbkgames.com/freebie/')
        items = soup.find_all("div", class_="archive-item")

        for each in items:
            topic_link = 'https://rbkgames.com' + each.find('a')['href']
            topic_name = clear_text_format(each.find('h3').text)
            topic_img = 'https:' + each.find('img')['data-src']

            if 'RBK Games' in topic_name or 'Акция' in topic_name:
                continue

            if not self.__check_is_old(topic_link):
                self.db.add_news(topic_link)

                topic_html = requests.get(topic_link).content
                topic_soup = bs(topic_html, features="html.parser")
                topic_post = '\n' + \
                             clear_text_format(topic_soup.find('div', class_='content-description').text).split(
                                 '\n')[0]

                self.topic_tags = set_tags(topic_name + topic_post)
                self.topic_post = topic_post
                self.topic_name = topic_name
                self.topic_link = topic_link
                self.topic_img = topic_img
                self.make_post()

    def gameout(self):
        soup = self.__get_content_request('https://gameout.ru/freebies-and-giveaways/')
        items = soup.find_all("article", class_="post-grid__item")

        for each in items:
            topic_link = each.find('a')['href']
            topic_name = clear_text_format(each.find('h2', class_='posts__title').find('a').text)

            if not self.__check_is_old(topic_link):
                self.db.add_news(topic_link)

                topic_html = requests.get(topic_link).content
                topic_soup = bs(topic_html, features="html.parser")
                topic_post = '\n' + clear_text_format(
                    topic_soup.find('div', class_='post__content').find_all('p')[0].text)
                topic_post_full = topic_soup.find('div', class_='post__content').text
                topic_img = topic_soup.find('figure', class_='post__thumbnail').find('img')['src']

                self.topic_tags = set_tags(topic_name + topic_post_full)
                self.topic_post = topic_post
                self.topic_name = topic_name
                self.topic_link = topic_link
                self.topic_img = topic_img
                self.make_post()

    def cq(self):
        soup = self.__get_content_request('https://cq.ru/tags/halyava')
        items = soup.find_all("a", class_="a-item")

        for each in items:
            topic_link = each['href']
            topic_name = clear_text_format(each.find('div', class_='a-item__title').text)
            topic_desc = '\n' + clear_text_format(each.find('div', class_='a-item__excerpt').text)
            topic_img = 'https://cq.ru' + each.find('img')['srcset'].split(' ')[0]

            if not self.__check_is_old(topic_link):
                self.db.add_news(topic_link)

                topic_html = requests.get(topic_link).content
                topic_soup = bs(topic_html, features="html.parser")
                topic_post_full = topic_soup.find('div', class_='post-content').text

                self.topic_tags = set_tags(topic_name + topic_post_full)
                self.topic_post = topic_desc
                self.topic_name = topic_name
                self.topic_link = topic_link
                self.topic_img = topic_img
                self.make_post()

    # def topmmogames(self):
    #     soup = self.__get_content_chrome('https://topmmogames.org/gift/')
    #     items = soup.find_all("div", class_="row")
    #
    #     for each in items:
    #         try:
    #             topic_link = 'https://topmmogames.org' + each.find('a')['href']
    #             topic_name = clear_text_format(each.find('h3').find('a').text)
    #             topic_desc = each.find_all('div', class_='col-12')[1]
    #             topic_img = 'https://topmmogames.org' + each.find('img')['data-src']
    #
    #             try:
    #                 topic_desc.find('div', class_='m-b-10').decompose()
    #             except:
    #                 pass
    #             try:
    #                 topic_desc.find('div', class_='m-t-10').decompose()
    #             except:
    #                 pass
    #             try:
    #                 topic_desc.find('div', class_='text-uppercase').decompose()
    #             except:
    #                 pass
    #
    #             topic_desc = topic_desc.find_all('div')
    #             out_txt = ''
    #             for each_div in topic_desc:
    #                 out_txt = out_txt + each_div.text + '\n'
    #             topic_desc = '\n' + clear_text_format(out_txt)
    #
    #             if not self.__check_is_old(topic_link):
    #                 self.db.add_news(topic_link)
    #
    #                 self.topic_tags = set_tags(topic_name + topic_desc)
    #                 self.topic_post = ''
    #                 self.topic_name = topic_name
    #                 self.topic_link = topic_link
    #                 self.topic_img = topic_img
    #                 self.make_post()
    #
    #         except Exception as e:
    #             print(f'Error: {e}')
