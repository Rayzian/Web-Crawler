# -*- coding:utf-8 -*-

from multiprocessing.managers import BaseManager
from myHTMLDownloader import HTMLDownloader
from startURLParser import URLParser

class spiderWorker(object):

    def __init__(self):

        self.downloader = HTMLDownloader()
        self.parser = URLParser()

        print "startURLSpiderNode init end."

    def crawl(self, url):
        try:
            response = self.downloader.downloader(url=url)
            if not response:
                print "URL is null."
                return None

            self.parser.parse(response=response)

        except Exception, e:
            print e
            print "Crwal failed."
            return None


# if __name__ == '__main__':
#     spider = spiderWorker()
#     url = "http://cd.58.com/sale.shtml?PGTID=0d100000-0006-60e8-bf1f-ef2320c160c9&ClickID=1"
#     spider.crawl(url=url)