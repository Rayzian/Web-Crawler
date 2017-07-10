# -*- coding: utf-8 -*-

import re
import json
from MyHTMLDownloader import myHTMLDownLoader

class myHTMLParser(object):
    def __init__(self):
        self.datas = {}


    def parse_urls(self, web_data):
        pattern = re.compile(r'http://movie.mtime.com/(\d+)/', re.IGNORECASE)
        urls = pattern.findall(web_data)
        if not urls:
            return None
        return list(set(urls))

    def parse_json(self, web_data, root_url):
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(web_data)[0]
        if result:
            value = json.loads(result)
            try:
                is_release = value.get("value").get("isRelease")
            except Exception, e:
                print e
                print None

            if is_release:
                if not value.get("value").get("hotValue"):
                    return self._parser_release(value=value, root_url=root_url)
                else:
                    return self._parser_no_release(value=value, root_url=root_url, is_release=2)
            else:
                return self._parser_no_release(value=value, root_url=root_url)


    def _parser_release(self, value, root_url):
        try:
            self.datas["is_release"] = 1
            self.datas["movie_rating"] = value.get("value").get("movieRating")
            self.datas["box_office"] = value.get("value").get("boxOffice ")
            self.datas["movie_title"] = value.get("value").get("movieTitle")

            self.datas["rpicture_final"] = self.datas["movie_rating"].get("RPictureFinal")
            self.datas["rstory_final"] = self.datas["movie_rating"].get("RStoryFinal")
            self.datas["rdirector_final"] = self.datas["movie_rating"].get("RDirectorFinal")
            self.datas["rother_final"] = self.datas["movie_rating"].get("ROtherFinal")
            self.datas["rating_final"] = self.datas["movie_rating"].get("RatingFinal")
            self.datas["movie_id"] = self.datas["movie_rating"].get("MovieId")
            self.datas["user_count"] = self.datas["movie_rating"].get("Usercount")
            self.datas["attitude_count"] = self.datas["movie_rating"].get("AttitudeCount")

            self.datas["total_box_office"] = self.datas["box_office"].get("TotalBoxOffice")
            self.datas["total_box_office_unit"] = self.datas["box_office"].get("TotalBoxOfficeUnit")
            self.datas["today_box_office"] = self.datas["box_office"].get("TodayBoxOffice")
            self.datas["today_box_office_unit"] = self.datas["box_office"].get("TodayBoxOfficeUnit")
            self.datas["show_days"] = self.datas["box_office"].get("ShowDays")

            try:
                self.datas["rank"] = self.datas["box_office"].get("Rank")
            except Exception, e:
                self.datas["rank"] = 0

            return self.datas

        except Exception, e:
            print root_url, value
            print e
            return None


    def _parser_no_release(self, root_url, value, is_release=0):
        try:
            self.datas["is_release"] = is_release
            self.datas["movie_rating"] = value.get("value").get("movieRating")
            self.datas["movie_title"] = value.get("value").get("movieTitle")

            self.datas["rpicture_final"] = self.datas["movie_rating"].get("RPictureFinal")
            self.datas["rstory_final"] = self.datas["movie_rating"].get("RStoryFinal")
            self.datas["rdirector_final"] = self.datas["movie_rating"].get("RDirectorFinal")
            self.datas["rother_final"] = self.datas["movie_rating"].get("ROtherFinal")
            self.datas["rating_final"] = self.datas["movie_rating"].get("RatingFinal")
            self.datas["movie_id"] = self.datas["movie_rating"].get("MovieId")
            self.datas["user_count"] = self.datas["movie_rating"].get("Usercount")
            self.datas["attitude_count"] = self.datas["movie_rating"].get("AttitudeCount")

            try:
                self.datas["rank"] = value.get("value").get("hotValue").get("Ranking")
            except Exception, e:
                self.datas["rank"] = 0

            return self.datas

        except Exception, e:
            print root_url, value
            return None