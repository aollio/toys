#!/usr/bin/env python3
import json
import re

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class HtmlParser:
    def parse_url(self, page_url, response):
        pattern = re.compile(r'(http://movie.mtime.com/(\d+)/)')
        urls = pattern.findall(response)
        if urls is not None:
            return list(set(urls))
        else:
            return None

    def parse_json(self, page_url, response):
        """
        解析响应
        :param page_url:
        :param response:
        :return:
        """
        # 将 "=" 和 "；"之间的内容提取出来
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(response)[0]
        if result is not None:
            # 使用json模块加载字符串
            value = json.loads(result)
            try:
                is_release = value.get('value').get('isRelease')
            except Exception as e:
                print(e)
                return
            if is_release:
                if value.get('value').get('hotValue') == None:
                    return self._parse_release(page_url, value)
                else:
                    return self._parse_no_release(page_url, value, is_release=2)

            else:
                return self._parse_no_release(page_url, value)

    def _parse_release(self, page_url, value: dict):
        """
        解析已经上映的影片
        :param page_url
        :param value: json data
        """
        try:
            is_release = 1
            movie_rating = value.get('value').get('movieRating')
            box_office = value.get('value').get('boxOffice')
            movie_title = value.get('value').get('movieTitle')

            rpicture_final = movie_rating.get('RPictureFinal')
            rstory_final = movie_rating.get('RStoryFinal')
            rdirector_final = movie_rating.get('RDirectorFinal')
            rother_final = movie_rating.get('ROtherFinal')
            rating_final = movie_rating.get('RatingFinal')

            movie_id = movie_rating.get('MovieId')
            user_count = movie_rating.get('Usercount')
            attitude_count = movie_rating.get('AttitudeCount')

            total_box_office = box_office.get('TotalBoxOffice')
            total_box_office_unit = box_office.get('TotalBoxOfficeUnit')
            today_box_office = box_office.get('TodayBoxOffice')
            today_box_office_unit = box_office.get('TodayBoxOfficeUnit')

            show_days = box_office.get('ShowDays')

            try:
                rank = box_office.get('Rank')
            except Exception as e:
                rank = 0

            # 返回所提取的内容
            return (movie_id, movie_title, rating_final,
                    rother_final, rpicture_final, rdirector_final,
                    rstory_final, user_count, attitude_count,
                    total_box_office + total_box_office_unit,
                    today_box_office + today_box_office_unit,
                    rank, show_days, is_release)

        except Exception as e:
            print(e, page_url, value)
            return None

    def _parse_no_release(self, page_url, value, is_release=0):
        """
        解析未上映的电影信息
        :param page_url:
        :param value:
        :param is_release:
        :return:
        """
        try:
            movie_rating = value.get('value').get('movieRating')
            movie_title = value.get('value').get('movieTitle')

            rpicture_final = movie_rating.get('RPictureFinal')
            rstory_final = movie_rating.get('RStoryFinal')
            rdirector_final = movie_rating.get('RDirectorFinal')
            rother_final = movie_rating.get('ROtherFinal')
            rating_final = movie_rating.get('RatingFinal')

            movie_id = movie_rating.get('MovieId')
            user_count = movie_rating.get('Usercount')
            attitude_count = movie_rating.get('AttitudeCount')

            try:
                rank = value.get('value').get('hotValue').get('Ranking')
            except Exception as e:
                rank = 0

            # 返回所提取的内容
            return (movie_id, movie_title, rating_final,
                    rother_final, rpicture_final, rdirector_final,
                    rstory_final, user_count, attitude_count,
                    u'无',
                    u'无',
                    rank, 0, is_release)

        except Exception as e:
            print(e, page_url, value)
            return None
