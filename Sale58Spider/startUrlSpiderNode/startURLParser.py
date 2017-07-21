# -*- coding:utf-8 -*-

import requests
import urlparse
from bs4 import BeautifulSoup
from multiprocessing.managers import BaseManager


class URLParser(object):

    def __init__(self):
        BaseManager.register("cateUrl_result")

        self.url_list = []
        server_add = "192.168.164.129"
        print "Connect to server %s..." % server_add

        self.conn = BaseManager(address=(server_add, 8001), authkey="zhouxiaoxi")
        self.conn.connect()

        self.cateUrl_store = self.conn.cateUrl_result()

    def parse(self, response):
        try:
            soup = BeautifulSoup(markup=response, features="lxml")
            categroise = soup.select("ul.ym-submnu > li > b")
            if categroise:
                for categroy in categroise:
                    if categroy.a.get("href") == "/shebei.shtml" or categroy.a.get("href") == "/tongxunyw/":
                        continue
                    url = urlparse.urljoin(base="http://cd.58.com/", url=categroy.a.get("href"))
                    if url and (url not in self.url_list):
                        self.url_list.append(url)
                        self.cateUrl_store.put(url)
                    else:
                        continue
                self.conn.shutdown()
            else:
                self.conn.shutdown()
                return None
        except Exception, e:
            print e
            print "Get categrop links failed. "
            self.conn.shutdown()
            return


# if __name__ == '__main__':
#     parser = URLParser()
#     url = "http://cd.58.com/sale.shtml?PGTID=0d100000-0006-601e-3f98-ccce91675238&ClickID=1"
#     web_data = requests.get(url=url)
#     if web_data.status_code == 200:
#         parser.parse(response=web_data.text)
#     else:
#         print "Over."