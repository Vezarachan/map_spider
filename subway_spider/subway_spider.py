"""
@author: Leon Elaiza
@license: MIT license
@contact: xiayin_lou@stu.pku.edu.cn
@file: subway_spider.py
@time: 2021/3/3 10:52 上午
@desc: 
"""
import os
from json import dumps

import requests
from geojson import Feature, Point, FeatureCollection
from requests.models import Response

AMAP_SUBWAY_API = 'http://map.amap.com/service/subway'
CITY_CODE = {
    'beijing': '1100',
    'shanghai': '3100',
    'xiamen': '3502',
    'guangzhou': '4401',
    'shenzhen': '4403',
    'wuhan': '4201',
    'tianjing': '1200',
    'nanjing': '3201',
    'xianggang': '8100',
    'chongqing': '5000',
    'hangzhou': '3301',
    'chengdu': '5101',
    'suzhou': '3205',
    'shenyang': '2101',
    'dalian': '2102',
    'changchun': '2201',
    'foshan': '4406',
    'kunming': '5301',
    'xian': '6101',
    'zhengzhou': '4101',
    'changsha': '4301',
    'ningbo': '3302',
    'wuxi': '3202',
    'qingdao': '3702',
    'nanchang': '3601',
    'fuzhou': '3501',
    'dongguan': '4419',
    'nanning': '4501',
    'hefei': '3401',
    'guiyang': '5201',
    'haerbin': '2301',
    'shijiazhuang': '1301',
    'wulumuqi': '6501',
    'wenzhou': '3303',
    'jinan': '3701',
    'lanzhou': '6201',
    'changzhou': '3204',
    'xuzhou': '3203',
    'taiyuan': '1401',
    'huhehaote': '1501'
}


class SubwaySpider:
    def __init__(self, city_name: str):
        self._city_name = city_name
        self._city_subway_url = '{0}_drw_{1}.json'.format(CITY_CODE[city_name], city_name)
        self._station_info = []

    def get_all_station_name(self):
        params = {
            'srhdata': self._city_subway_url
        }
        response: Response = requests.get(AMAP_SUBWAY_API, params=params)
        station_json = response.json()
        subway_lines = station_json['l']
        for line in subway_lines:
            stations = line['st']
            line_code = line['ln']
            for station in stations:
                station_name = station['n']
                coordinates = station['sl']
                lon, lat = coordinates.split(',')
                self._station_info.append({
                    'name': station_name,
                    'line': line_code,
                    'lon': lon,
                    'lat': lat
                })
        return self

    def to_csv(self, filename: str = None):
        if filename is None:
            path = os.path.abspath(os.curdir) + '/{0}_subway_stations.csv'.format(self._city_name)
        else:
            path = '{0}/{1}.csv'.format(os.path.abspath(os.curdir), filename)
        with open(path, 'a') as f:
            f.writelines(','.join(self._station_info[0].keys()) + '\n')
            for station in self._station_info:
                # f.writelines(
                #     '{0},{1},{2},{3}\n'.format(poi['name'], poi['type'], poi['lng'], poi['lat']))
                f.writelines(
                    '{0}, {1}, {2}, {3}\n'.format(station['name'], station['line'], station['lon'], station['lat']))
        return self

    def to_geojson(self, filename: str = None):
        features = []
        if filename is None:
            path = os.path.abspath(os.curdir) + '/{0}_subway_stations.geojson'.format(self._city_name)
        else:
            path = '{0}/{1}.csv'.format(os.path.abspath(os.curdir), filename)
            for station in self._station_info:
                feature = Feature(geometry=Point((station['lon'], station['lat'])),
                                  properties={'name': station['name'], 'line': station['line']})
                features.append(feature)
            feature_collection = FeatureCollection(features)
            with open(path, 'a') as f:
                f.write(dumps(feature_collection))
        return self
