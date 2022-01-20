import re
import os
import requests
from requests import Session
from bs4 import BeautifulSoup as bs
from pprint import pprint
from time import sleep

import undetected_chromedriver as uc

from utils.bot_functions import get_bot
from config import group, tags
from database import db
from utils.decorators import catcherError
from utils.base_functions import log

delay = 5

@catcherError
class Parser():
    def __init__(self):
        options = uc.ChromeOptions()
        prof_id = '1'
        path = f'_temp/profile{prof_id}'
        options.add_argument(f'--user-data-dir={os.path.abspath(path)}')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-popup-blocking")
        options.page_load_strategy = 'eager'
        options.add_argument('--disable-gpu')
        options.headless=True
        self.driver = uc.Chrome(options=options)

    def __get_content_request(self, url):
        html = requests.get(url).content
        soup = bs(html,features="html.parser")
        return soup

    def __get_content_chrome(self, url):
        self.driver.get(url)
        html = self.driver.page_source
        soup = bs(html,features="html.parser")
        return soup

    def __clear_text_format(self, txt):
        txt = txt.replace('\n\n','\n').replace('\t','')
        if txt[0:1] == '\n':
            txt = txt[1:]

        while txt[-1] == '\n':
            txt = txt[0:-1]

        while txt[-1] == ' ':
            txt = txt[0:-1]

        while txt[0] == ' ':
            txt = txt[1:]

        return txt

    def start(self):
        try:
            sources = [
                self.igromania(),
                self.playisgame(),
                self.goha(), 
                self.freesteam(), 
                self.coopland(),
                self.coopland('https://coop-land.ru/tags/%E1%E5%F2%E0-%F2%E5%F1%F2/'),
                self.rbkgames(), 
                self.gameout(),
                self.cq(),
                self.topmmogames()
            ]
            # sources = [self.topmmogames()]
            
        except Exception as e:
            log(e)
    
    @catcherError
    def igromania(self):
        soup = self.__get_content_request('https://www.igromania.ru/news/sale/')
        items = soup.find_all("div", class_="aubl_item")

        for each in items:
            topic_link = 'https://www.igromania.ru' + each.find('a',class_="aubli_img")['href']
            topic_name = each.find('a',class_="aubli_name").text + '\n'
            topic_desc = each.find('div',class_="aubli_desc").text

            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            topic_html = requests.get(topic_link).content
            topic_soup = bs(topic_html,features="html.parser")
            topic_post = topic_soup.find('div',class_='universal_content')
            topic_post.find('div', class_='uninote').decompose()
            topic_post = self.__clear_text_format(topic_post.text)
            topic_img = topic_soup.find('div',class_='main_pic_container').find('img')['src']            

            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post':topic_desc,
                'tags':self.__set_tags(topic_name + '\n' + topic_post)
            })

    @catcherError
    def playisgame(self):
        soup = self.__get_content_request('https://playisgame.com/halyava/')
        items = soup.find("div", class_="pp-posts-skin-news").find_all("div", class_="pp-grid-item-wrap")

        for each in items:
            topic_link = each.find('a')['href']
            topic_img = each.find('img')['src']
            topic_name = self.__clear_text_format(each.find('h2').text)
            topic_desc = each.find('div',class_="pp-post-excerpt").text
            
            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            topic_html = requests.get(topic_link).content
            topic_soup = bs(topic_html,features="html.parser")
            topic_post = topic_soup.find('div',class_='elementor-widget-theme-post-content').find('div',class_='elementor-widget-container')
            try:
                topic_post.find('figure').decompose()
            except:
                pass
            topic_post = '\n' + self.__clear_text_format(topic_post.text).split('\n')[0] 

            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post':topic_post,
                'tags':self.__set_tags(topic_name + topic_post)
            })

    @catcherError
    def goha(self):
        soup = self.__get_content_request('https://gamemag.ru/news/tags/halyava')
        items = soup.find("div", class_="news__wrap").find_all("div", class_="news-item")

        for each in items:
            topic_link = 'https://gamemag.ru' + each.find('a',class_='news-item__link')['href']
            topic_name = self.__clear_text_format(each.find('a',class_="news-item__text").text)
            topic_desc = each.find('div',class_="news-description").text
            topic_img = 'https://gamemag.ru/' + each.find('img',class_='news-item__img')['src']
            
            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post': '\n' + self.__clear_text_format(topic_desc).split('\n')[0],
                'tags':self.__set_tags(topic_name + topic_desc)
            })

    @catcherError
    def freesteam(self):
        soup = self.__get_content_request('https://freesteam.ru/')
        items = soup.find_all("div", class_="post-box")

        for each in items:
            topic_link = each.find('a')['href']
            topic_name = self.__clear_text_format(each.find('h2', class_='entry-title').find('a').text)
            
            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            topic_html = requests.get(topic_link).content
            topic_soup = bs(topic_html,features="html.parser")

            topic_post = topic_soup.find('div',class_='entry-content').text
            topic_post = self.__clear_text_format(topic_post)
            split_post = '\n' + topic_post.replace('Рекламный блок. Sponsored Links.',' ').split('\n\n')[0]
            topic_img = topic_soup.find('div',class_='post-thumb').find('img')['data-src']

            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post':split_post,
                'tags':self.__set_tags(topic_name + topic_post)
            })

    @catcherError
    def coopland(self, url='https://coop-land.ru/tags/%F0%E0%E7%E4%E0%F7%E0+%EA%EB%FE%F7%E5%E9/'):
        soup = self.__get_content_request(url)
        items = soup.find_all("article", class_="news")

        for each in items:
            topic_link = each.find('a', class_='big-link')['href']
            topic_name = self.__clear_text_format(each.find('h2', class_='title').text)
            topic_desc = '\n'+self.__clear_text_format(each.find('div', class_='preview-text').text)
            
            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            topic_html = requests.get(topic_link).content
            topic_soup = bs(topic_html,features="html.parser")

            topic_img = topic_soup.find('div',class_='full-story-content').find('img')['data-src']

            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post':topic_desc,
                'tags':self.__set_tags(topic_name + topic_desc)
            })

    @catcherError
    def rbkgames(self):
        soup = self.__get_content_request('https://rbkgames.com/freebie/')
        items = soup.find_all("div", class_="archive-item")

        for each in items:
            topic_link = 'https://rbkgames.com' + each.find('a')['href']
            topic_name = self.__clear_text_format(each.find('h3').text)
            topic_img = 'https:' + each.find('img')['data-src']
            
            if 'RBK Games' in topic_name or 'Акция' in topic_name:
                continue

            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            topic_html = requests.get(topic_link).content
            topic_soup = bs(topic_html,features="html.parser")
            topic_post = '\n' + self.__clear_text_format(topic_soup.find('div',class_='content-description').text).split('\n')[0]

            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post':topic_post,
                'tags':self.__set_tags(topic_name + topic_post)
            })

    @catcherError
    def gameout(self):
        soup = self.__get_content_request('https://gameout.ru/freebies-and-giveaways/')
        items = soup.find_all("article", class_="post-grid__item")

        for each in items:
            topic_link = each.find('a')['href']
            topic_name = self.__clear_text_format(each.find('h2', class_='posts__title').find('a').text)
            
            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            topic_html = requests.get(topic_link).content
            topic_soup = bs(topic_html,features="html.parser")
            topic_post = '\n' + self.__clear_text_format(topic_soup.find('div',class_='post__content').find_all('p')[0].text)
            topic_post_full = topic_soup.find('div',class_='post__content').text 
            topic_img = topic_soup.find('figure',class_='post__thumbnail').find('img')['src']
            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post':topic_post,
                'tags':self.__set_tags(topic_name + topic_post_full)
            })

    @catcherError
    def cq(self):
        soup = self.__get_content_request('https://cq.ru/tags/halyava')
        items = soup.find_all("a", class_="a-item")

        for each in items:
            topic_link = each['href']
            topic_name = self.__clear_text_format(each.find('div', class_='a-item__title').text)
            topic_desc = '\n' + self.__clear_text_format(each.find('div',class_='a-item__excerpt').text)
            topic_img = each.find('img')['srcset'].split(' ')[0]
            
            if self.__check_is_old(topic_link):
                continue
            else:
                db.add_news(topic_link)

            topic_html = requests.get(topic_link).content
            topic_soup = bs(topic_html, features="html.parser")
            topic_post_full = topic_soup.find('div',class_='post-content').text 

            self.__post_news({
                'topic_name':topic_name,
                'topic_img':topic_img,
                'topic_link':topic_link,
                'topic_post':topic_desc,
                'tags':self.__set_tags(topic_name + topic_post_full)
            })

    @catcherError
    def topmmogames(self):
        soup = self.__get_content_chrome('https://topmmogames.org/gift/')
        items = soup.find_all("div", class_="row")

        for each in items:
            try:
                topic_link = 'https://topmmogames.org' + each.find('a')['href']
                topic_name = self.__clear_text_format(each.find('h3').find('a').text)
                topic_desc = each.find_all('div',class_='col-12')[1]
                topic_img = 'https://topmmogames.org'+each.find('img')['data-src']
                
                try:
                    topic_desc.find('div', class_='m-b-10').decompose()
                except:
                    pass
                try:
                    topic_desc.find('div', class_='m-t-10').decompose()
                except:
                    pass
                try:
                    topic_desc.find('div', class_='text-uppercase').decompose()
                except:
                    pass

                topic_desc = topic_desc.find_all('div')
                out_txt = ''
                for each_div in topic_desc:
                    out_txt = out_txt + each_div.text + '\n'
                topic_desc = '\n' + self.__clear_text_format(out_txt) 
                
                if self.__check_is_old(topic_link):
                    continue
                else:
                    db.add_news(topic_link)

                self.__post_news({
                    'topic_name':topic_name,
                    'topic_img':topic_img,
                    'topic_link':topic_link,
                    'topic_post':'',
                    'tags':self.__set_tags(topic_name + topic_desc)
                })
            except:
                pass     

    def __post_news(self, data):
        bot = get_bot()
        try:
            # print(data)
            if '.webp' in data['topic_img']:
                data['topic_img'] = open('content/no.png', 'rb')

            bot.send_photo(
                chat_id=group,
                photo=data['topic_img'],
                caption=f"{data['tags']}\n<b>{data['topic_name']}</b>\n{data['topic_post']}\n<a href='{data['topic_link']}'>[<i>Источник</i>]</a>",
                parse_mode='HTML'
            )
        except Exception as e:
            log('** Не удалость запостить новость:\nError: ' + str(e)+str(data)+'\n\n')
        sleep(delay)
        # pass

    def __check_is_old(self, url):
        if db.get_news(url) == None:
            return False
        else:
            return True

    def __set_tags(self, data):
        data_tags = []
        out = ''
        for each_tag in tags:
            if re.search(each_tag,data):
                data_tags.append(tags[each_tag])   
        x = data_tags
        data_tags = sorted(set(x), key=lambda d: x.index(d))
        for each in data_tags:
            out = out + each + ' '
        return out

