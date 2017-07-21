# -*- coding:utf-8 -*-

import pymongo
class DataOutPut(object):
    def __init__(self):
        self.data = {}
        self.client = pymongo.MongoClient("localhost", 27017)
        self.mTimeMovie = self.client["mTimeMovie"]
        self.movie = self.mTimeMovie["movie"]

    def store_data(self, datas):
        for temp in datas:
            self.data[temp] = temp
        self.movie.insert_one(self.data)