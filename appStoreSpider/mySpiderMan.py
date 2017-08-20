# -*- coding: utf-8 -*-

from appStoreSpider.myDataOut import MyDataOut
from appStoreSpider.myHTMLDownloader import MyHTMLDownloader
from appStoreSpider.myHTMLParser import MyHTMLParser


class spiderMan(object):
    def __init__(self, url):
        self.downloader = MyHTMLDownloader()
        self.parser = MyHTMLParser(url)

    def crawl(self, url):
        response = self.downloader.downloader(url)

        if response:
            self.parser.app_parser(response=response)
        else:
            return None


if __name__ == '__main__':
    for url in ["https://www.apple.com/itunes/charts/paid-apps/",
                "https://www.apple.com/itunes/charts/free-apps/"]:
        spider = spiderMan(url=url)
        spider.crawl(url)
