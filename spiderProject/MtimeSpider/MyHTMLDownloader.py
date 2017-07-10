# -*- coding: utf-8 -*-

import requests

class myHTMLDownLoader(object):
    def downloader(self, url):
        if not url:
            return None

        header = {"user_agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"}

        web_data = requests.get(url=url, headers=header)
        if web_data.status_code == 200:
            # web_data.encoding = "utf-8"
            return web_data.text
        else:
            return None