"""
@author: Leon Elaiza
@license: MIT license
@contact: xiayin_lou@stu.pku.edu.cn
@file: demo2.py
@time: 2020/9/10 5:55 下午
@desc: 
"""
from streetview_spider.map_streetview_spider import BmapStreetViewSpider

BAMP_API_KEY = 'hM9GzOGeQVHvXi6lM0iLjfd2uEidhfYm'

locations = ['116.35,40.04778',
             '116.3, 40.04778']


bmap_streetview_spider = BmapStreetViewSpider(api_key='hM9GzOGeQVHvXi6lM0iLjfd2uEidhfYm', locations=locations)
bmap_streetview_spider.search_streeview_images().download()

