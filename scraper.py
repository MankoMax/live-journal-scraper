import requests
from bs4 import BeautifulSoup
from PIL import Image
import os.path
from urlhelpers import cut_link, post_from_link
from fake_useragent import UserAgent
from dotenv import load_dotenv
import os

load_dotenv()

HTTP_PROXY = os.getenv("HTTP_PROXY")
HTTPS_PROXY = os.getenv("HTTPS_PROXY")

class Scrapper:
    
    def __init__(self, calendar_page):
        self.calendar_page = calendar_page
        self.urls = []
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random
            }

        self.proxies = {
            'http': HTTP_PROXY,
            'https': HTTPS_PROXY,
            } 

                
    def get_calendar_years(self):
        urls = []
        req = requests.get(self.calendar_page, proxies=self.proxies, headers=self.headers)
        soup = BeautifulSoup(req.text, "html.parser")
        text = soup.select("div.entry-text")
        for i in text:
            for link in i.find_all('a'):
                res = cut_link(link.get('href'))
                if res not in urls:
                    urls.append(res)
        return urls


    def get_calendar_month(self, urls_list):
        urls = []
        for i in urls_list:
            req = requests.get(i, proxies=self.proxies, headers=self.headers)
            soup = BeautifulSoup(req.text, "html.parser")
            text = soup.select("caption")
            for i in text:
                for link in i.find_all('a', class_="month", id=False):
                    res = link.get('href')
                    if res not in urls:
                        urls.append(res)
        return urls


    def get_calendar_days(self, urls_list):
        urls = []
        for i in urls_list:
            req = requests.get(i, proxies=self.proxies, headers=self.headers)
            soup = BeautifulSoup(req.text, "html.parser")
            text = soup.select("dt")
            for i in text:
                for link in i.find_all('a'):
                    res = link.get('href')
                    if res not in urls:
                        urls.append(res)
        return urls


    def get_posts_links(self, urls_list):
        urls = []
        for i in urls_list:
            req = requests.get(i, proxies=self.proxies, headers=self.headers)
            soup = BeautifulSoup(req.text, "html.parser")
            text = soup.select("dt.entry-title")
            for i in text:
                for link in i.find_all('a'):
                    res = link.get('href')
                    if res not in urls:
                        urls.append(res)
        return urls


    def save_post(self, url):
        path = os.makedirs(f'{os.path.abspath(os.curdir)}\posts\{post_from_link(url)}')
        count = 0
        req = requests.get(url, proxies=self.proxies, headers=self.headers)
        soup = BeautifulSoup(req.text, "html.parser")
        headings = soup.find_all('h1')
        texts = soup.find_all('div', class_="b-singlepost-bodywrapper", id=False)

        with open(f"posts/{post_from_link(url)}/{post_from_link(url)}.txt", mode='w', encoding="utf-8") as f:

            for heading in headings:
                f.write(f'{heading.get_text()}\n')

            for text in texts:
                f.write(f'\n{text.get_text()}')
                
        text = soup.select("div.b-singlepost-bodywrapper")
        
        for i in text:
            for link in i.find_all('img'):
                count += 1
                res = link.get('src')
                print(res)
                if '.png' or '.jpg' in res:
                    img = Image.open(requests.get(res, stream = True).raw)
                    img.save(f"posts/{post_from_link(url)}/{count}.png")
        print(f'Post {url} is saved!')
    