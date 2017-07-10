# -*- coding:utf-8 -*-

import time
import pymongo
from spiderObject.MtimeSpider.MyHTMLDownloader import myHTMLDownLoader
from spiderObject.MtimeSpider.MyHTMLParser import myHTMLParser

class spiderMan(object):
    def __init__(self):
        self.downloader = myHTMLDownLoader()
        self.parser = myHTMLParser()
        self.client = pymongo.MongoClient("localhost", 27017)
        self.mTimeMovie = self.client["mTimeMovie"]
        self.movie = self.mTimeMovie["movie"]

    def crawl(self, root_url):
        response = self.downloader.downloader(url=root_url)
        movieId_list = self.parser.parse_urls(web_data=response)

        for id in movieId_list:
            print "Crawling --> ", id
            try:
                local_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
                detail_url = "http://service.library.mtime.com/Movie.api" \
                             "?Ajax_CallBack=true" \
                             "&Ajax_CallBackType=Mtime.Library.Services" \
                             "&Ajax_CallBackMethod=GetMovieOverviewRating" \
                             "&Ajax_CrossDomain=1" \
                             "&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2F{}%2F" \
                             "&t={}" \
                             "&Ajax_CallBackArgument0={}".format(id, local_time, id)

                detail_response = self.downloader.downloader(url=detail_url)
                datas = self.parser.parse_json(root_url=detail_url, web_data=detail_response)

                if datas:
                    if datas["is_release"] == 1:
                        data = {
                                "movieID": datas["movie_id"],
                                "movieTitle": datas["movie_title"],
                                "IsRelease": True,
                                "RPictureFinal": datas["rpicture_final"],
                                "RStoryFinal": datas["rstory_final"],
                                "RDirectorFinal": datas["rdirector_final"],
                                "ROtherFinal": datas["rother_final"],
                                "RatingFinal": datas["rating_final"],
                                "UserCount": datas["user_count"],
                                "AttitudeCount": datas["attitude_count"],
                                "TotleBoxOffice": datas["total_box_office"] + datas["total_box_office_unit"],
                                "BoxOffice": datas["box_office"],
                                "TodayBoxOffice": datas["today_box_office"] + datas["today_box_office_unit"],
                                "ShowDays": datas["show_days"],
                                "Rank": datas["rank"]
                            }
                    else:
                        data = {
                            "movieID": datas["movie_id"],
                            "movieTitle": datas["movie_title"],
                            "IsRelease": False,
                            "RPictureFinal": datas["rpicture_final"],
                            "RStoryFinal": datas["rstory_final"],
                            "RDirectorFinal": datas["rdirector_final"],
                            "ROtherFinal": datas["rother_final"],
                            "RatingFinal": datas["rating_final"],
                            "UserCount": datas["user_count"],
                            "AttitudeCount": datas["attitude_count"],
                            "Rank": datas["rank"]
                        }
                    self.movie.insert_one(data)
            except Exception, e:
                print e
                print "Crawl failed --> ", id
                time.sleep(2)
                continue
            print "Crawl finished --> ", id
            time.sleep(2)


if __name__ == '__main__':
    spider = spiderMan()
    root_url = r'http://theater.mtime.com/China_Sichuan_Province_Chengdu/'
    spider.crawl(root_url=root_url)