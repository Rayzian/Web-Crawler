# -*- coding:utf-8 -*-

from multiprocessing.managers import BaseManager
from myHTMLDownloader import HTMLDownloader
from detailHTMLParser import detailParser

class spiderWorker(object):

    def __init__(self):
        BaseManager.register("detailUrl_result")
        BaseManager.register("dataStore_result")

        server_add = "192.168.164.129"
        print "Connect to server %s..." % server_add

        self.m = BaseManager(address=(server_add, 8001), authkey="zhouxiaoxi")
        self.m.connect()
        self.detail_url = self.m.detailUrl_result()
        self.data_store = self.m.dataStore_result()

        self.downloader = HTMLDownloader()
        self.parser = detailParser()

        print "detailSpiderNode init finish."

    def crawl(self):
        while True:
            try:
                if not self.detail_url.empty():
                    url = self.detail_url.get(timeout=10)
                    print "The crawler is parsing %s " % url
                    response = self.downloader.downloader(url=url)
                    if response:
                        data = self.parser.parse(response=response)
                        self.data_store.put(data)
                else:
                    break
            except Exception, e:
                print e
                print "Crawl failed."
        return None


if __name__ == '__main__':
    spider = spiderWorker()
    spider.crawl()