"""
@author: Leon Elaiza
@license: MIT license
@contact: xiayin_lou@stu.pku.edu.cn
@file: map_streetview_spider.py
@time: 2020/9/10 3:50 下午
@desc: An spider for acquiring streetview images
"""
from typing import List, Dict
import os
import requests
from requests import Response
from urllib.request import urlretrieve
from urllib.parse import urlencode
import logging
import json

BMAP_STREETVIEW_API = 'http://api.map.baidu.com/panorama/v2'


def __check_json(content: str):
    """
    Check the response
    :param content:
    :return bool:
    """
    try:
        json.loads(content)
        return True
    except Exception:
        return False


class BmapStreetViewSpider(object):
    """
    Baidu Map Streetview API SPider
    """
    api_key: str
    width: float
    height: float
    locations: List[str]
    coord_type: str
    heading: int
    pitch: int
    urls: List[str] = []

    def __init__(self,
                 api_key: str,
                 locations: List[str],
                 width: float = 400,
                 height: float = 300,
                 coord_type: str = 'wgs84ll',
                 heading: int = 0,
                 pitch: int = 0,
                 fov: int = 90):
        self.api_key = api_key
        self.locations = locations
        self.width = width
        self.height = height
        self.coord_type = coord_type
        self.heading = heading
        self.pitch = pitch
        self.fov = fov

    def search_streeview_images(self):
        """
        get streetview url
        :return self:
        """
        for location in self.locations:
            params: Dict = {
                'ak': self.api_key,
                'width': self.width,
                'height': self.height,
                'location': location,
                'coordtype': self.coord_type,
                'heading': self.heading,
                'pitch': self.pitch,
                'fov': self.fov
            }

            try:
                response: Response = requests.get(BMAP_STREETVIEW_API, params=params)
                if __check_json(response.text):
                    logging.error('JSON parse failed.')
                    break
            except Exception as e:
                logging.error('Parse Error - ', e)
            self.urls.append('{0}?{1}'.format(BMAP_STREETVIEW_API, urlencode(params)))
        return self

    def download(self, path: str = None):
        """
        Download images
        :param path:
        :return:
        """
        for i in range(len(self.locations)):
            lng, lat = self.locations[i].split(',')
            img_name = 'sv_{0}_{1}.png'.format(lng, lat)
            try:
                if path:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    save_path = path
                else:
                    save_path = '{0}/{1}'.format(os.path.abspath(os.curdir), 'streetview_imgs')
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                filename = '{0}/{1}'.format(save_path, img_name)
                urlretrieve(self.urls[i], filename=filename)
            except IOError as e:
                logging.error('file operation failed! ', e)
            except Exception as e:
                logging.error('exception!! ', e)
