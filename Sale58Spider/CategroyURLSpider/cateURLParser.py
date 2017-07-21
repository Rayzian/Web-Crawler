# -*- coding:utf-8 -*-

import time
import urlparse
from bs4 import BeautifulSoup
from multiprocessing.managers import BaseManager
from myHTMLDownloader import HTMLDownloader

class cateParser(object):
    def __init__(self):
        BaseManager.register("detailUrl_result")

        server_add = "192.168.164.129"
        print "Connect to server %s..." % server_add

        self.conn = BaseManager(address=(server_add, 8001), authkey="zhouxiaoxi")
        self.conn.connect()

        self.cateUrl_store = self.conn.detailUrl_result()
        self.downloader = HTMLDownloader()

    def parse(self, response):
        try:
            soup = BeautifulSoup(markup=response, features="lxml")
            target_div = soup.find_all(name=["a"], attrs={"class": "t"})
            if not target_div:
                return None
            # print target_div
            for div in target_div:
                print div.get("href")
                self.cateUrl_store.put(div.get("href"))

            # is_next = soup.find(name=["a"], attrs={"class": "next"}).get("href")
            # if not is_next:
            #     print "No next page"
            #     return None
            # next_page = urlparse.urljoin(base="http://cd.58.com", url=is_next)
            # response = self.downloader.downloader(url=next_page)
            # return self.parse(response=response)
        except Exception, e:
            print e
            print "Crawl link failed."
            return
