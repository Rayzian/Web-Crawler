# -*- coding:utf-8 -*-

import pymongo


class MyDataOut(object):
    def __init__(self, url):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db, self.sheet = self._check_data(url)
        self.table = self.db[self.sheet]

    def save_data(self, datas):
        self.table.insert(dict(datas))

    def _check_data(self, url):
        if "/cn/" in url:
            if "free-apps" in url:
                sheet = "FreeApps"
                return self.client["CNApp"], sheet
            elif "paid-apps" in url:
                sheet = "PaidApps"
                return self.client["CNApp"], sheet

        elif "/jp/" in url:
            if "free-apps" in url:
                sheet = "FreeApps"
                return self.client["JPApp"], sheet
            elif "paid-apps" in url:
                sheet = "PaidApps"
                return self.client["JPApp"], sheet

        else:
            if "free-apps" in url:
                sheet = "FreeApps"
                return self.client["USApp"], sheet
            elif "paid-apps" in url:
                sheet = "PaidApps"
                return self.client["USApp"], sheet
