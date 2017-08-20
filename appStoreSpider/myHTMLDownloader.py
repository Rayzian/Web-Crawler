# -*- coding:utf-8 -*-

import time
import random
import requests


class MyHTMLDownloader(object):
    def downloader(self, url):
        time.sleep(random.randint(1, 3))
        web_data = requests.get(url)

        if web_data.status_code == 200:
            return web_data.text
        else:
            return None
