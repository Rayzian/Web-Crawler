# -*- coding:utf-8 -*-

import pymongo


class DataOutPut(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.saleTabel = self.client["saleTabel"]
        self.staff = self.saleTabel["staff"]

    def store_data(self, data):
        if not data:
            return
        self.staff.insert_one(data)
