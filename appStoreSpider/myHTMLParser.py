# -*- coding:utf-8 -*-

import re
from bs4 import BeautifulSoup
from appStoreSpider.myHTMLDownloader import MyHTMLDownloader
from appStoreSpider.myDataOut import MyDataOut


class MyHTMLParser(object):
    def __init__(self, url):
        self.pattern1 = re.compile(r'<li><strong>(\S+)</strong>')
        self.size_pattern = re.compile(r'<span class="label">Size: </span>(\w+\s\w+)</li>')
        self.screenshots_pattren = re.compile(r'src="(\S+)"')
        self.save = MyDataOut(url)
        self.downloader = MyHTMLDownloader()

    def app_parser(self, response):
        soup = BeautifulSoup(response, features="lxml")

        lis = soup.select("div > section > ul > li") if soup.select("div > section > ul > li") else soup.select(
            "div > section > div > ul > li")
        for li in lis[:30]:
            app_rant = re.findall(pattern=self.pattern1, string=str(li))[0]
            print app_rant
            app_name = li.select("a")[1].get_text()
            print app_name
            app_type = li.select("a")[2].get_text()
            print app_type
            app_url = li.select("a")[0].get("href")
            print app_url

            appDetail_response = self.downloader.downloader(url=app_url)
            data = self.app_detail_parser(response=appDetail_response)

            data["app_rant"] = app_rant
            data["app_name"] = app_name
            data["app_type"] = app_type
            data["app_url"] = app_url

            self.save.save_data(datas=data)

    def app_detail_parser(self, response):
        soup = BeautifulSoup(response, features="lxml")

        img = soup.find(name="img", attrs={"class": "artwork"})
        if img:
            print img.get("src-swap")

        description = soup.find(name="p", attrs={"itemprop": "description"})
        if description:
            print description.get_text()

        updated = soup.find(name="span", attrs={"itemprop": "datePublished"})
        if updated:
            print updated.get_text()

        uls = soup.find(name="div", attrs={"class": "lockup product application"})
        size = re.findall(pattern=self.size_pattern, string=str(uls))
        if size:
            print size

        divs = soup.find(name="div", attrs={"class": "toggle"})
        screen_shots = re.findall(pattern=self.screenshots_pattren, string=str(divs))
        if screen_shots:
            print screen_shots

        info = {
            "img": img.get("src-swap"),
            "description": description.get_text(),
            "updated": updated.get_text(),
            "size": size,
            "screen_shots": screen_shots
        }

        return info
