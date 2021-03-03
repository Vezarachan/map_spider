"""
@author: Leon Elaiza
@license: MIT license
@contact: xiayin_lou@stu.pku.edu.cn
@file: subway_spider_test.py
@time: 2021/3/3 2:53 下午
@desc: 
"""
from subway_spider.subway_spider import SubwaySpider

spider = SubwaySpider(city_name='xiamen')

spider.get_all_station_name().to_csv().to_geojson()