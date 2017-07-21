# -*- coding:utf-8 -*-

from multiprocessing.managers import BaseManager
from myHTMLDownloader import HTMLDownloader
from cateURLParser import cateParser

class spiderWorker(object):
    def __init__(self):
        BaseManager.register("cateUrl_result")
        BaseManager.register("detailUrl_result")

        server_add = "192.168.164.129"
        print "Connect to server %s..." % server_add

        self.conn = BaseManager(address=(server_add, 8001), authkey="zhouxiaoxi")

        self.conn.connect()
        self.categroy_url = self.conn.cateUrl_result()
        self.detail_url = self.conn.detailUrl_result()

        self.downloader = HTMLDownloader()
        self.parser = cateParser()

        print "cateHTMLSpiderNode init finish."

    def crawl(self):
        while True:
            try:
                if not self.categroy_url.empty():
                    url = self.categroy_url.get(time=10)

                    if url == "end":
                        print "Control node notifies the categroy link crawler to stop working."
                        self.categroy_url.put("end")
                        return

                    print "The categroy link crawler is parsing %s " % url
                    content = self.downloader.downloader(url=url)
                    if content:
                        self.parser.parse(content)
                    else:
                        print "parsing %s is failed." % url
                        self.detail_url.put("end")
                        return

            except EOFError, e:
                print e
                print "The Categroy link crawler failed."
                return

            except Exception, e:
                print e
                print "Crawl failed."

if __name__ == '__main__':
    spider = spiderWorker()
    spider.crawl()


