# -*- coding:utf-8 -*-

import requests
import random
import time
from bs4 import BeautifulSoup


class detailParser(object):

    def parse(self, response):
        soup = BeautifulSoup(markup=response, features="lxml")

        title = soup.title.text
        price = soup.select("div.price_li > span > i") if soup.find_all(name=["span"], attrs={"class": "price_now"}) else soup.select("span.price.c_f50")
        if price:
            price = price[0].text
        else:
            price = None
        localtion = list(soup.select(".c_25d a")[0].stripped_strings) if soup.find_all(name=["span"], attrs={"class": "c_25d"}) else soup.select("div.palce_li > span > i")
        if not isinstance(localtion, list):
            if localtion:
                localtion = localtion[0].text
            else:
                localtion = None
        date = soup.select(".time")[0].text if soup.find_all(name=["li"], attrs={"class": "time"}) else None
        detail_data = {
            "Title": title,
            "price": price,
            "localtion": localtion,
            "date": date
        }
        time.sleep(random.randint(1, 5))
        return detail_data



# if __name__ == '__main__':
#     parser = detailParser()
    # url = "http://cd.58.com/diannao/23167388609311x.shtml" \
    #       "?adtype=1&PGTID=0d300023-0006-60d1-4585-5a8ef5b3a94f" \
    #       "&entinfo=23167388609311_0" \
    #       "&psid=112093789196598592751749340" \
    #       "&iuType=_undefined&ClickID=2"
    # url = "http://zhuanzhuan.58.com/detail/883234004685422599z.shtml?fullCate=5%2C39&fullLocal=102&from=pc"
    # web_data = requests.get(url=url)
    # print web_data.status_code
    #
    # parser.parse(response=web_data.text)