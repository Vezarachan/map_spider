from abc import ABC, abstractmethod
from typing import List
import logging

AMAP_API = 'https://restapi.amap.com/v3/place/polygon'
BMAP_APi = 'http://api.map.baidu.com/place/v2/search'


class NoRecordsError(Exception):
    def __init__(self, err='Got 0 record'):
        Exception.__init__(self, err)


class RegionDivision(object):
    y_min: float
    x_min: float
    y_max: float
    x_max: float
    precision: float
    api_type: str

    def __init__(self, extent, precision=0.01, api_tyoe='Amap'):
        self.y_min = extent[0]
        self.x_min = extent[1]
        self.y_max = extent[2]
        self.x_max = extent[3]
        self.precision = precision
        self.api_type = api_tyoe

    def generate_bounds(self) -> List[str]:
        # calculate cols of extent
        if (self.x_max - self.x_min) % self.precision == 0:
            cols = (self.x_max - self.x_min) / self.precision
        else:
            cols = (self.x_max - self.x_min) / self.precision + 1
        # calculate rows of extent
        if (self.y_max - self.y_min) % self.precision == 0:
            rows = (self.y_max - self.y_min) / self.precision
        else:
            rows = (self.y_max - self.y_min) / self.precision + 1

        cols = int(cols)
        rows = int(rows)
        bounds = list()

        for i in range(cols):
            for j in range(rows):
                lng_min = self.x_min + i * self.precision
                lat_min = self.y_min + j * self.precision
                lng_max = self.x_min + (i + 1) * self.precision
                lat_max = self.x_min + (j + 1) * self.precision
                if lng_max > self.x_max:
                    lng_max = self.x_max
                if lat_max > self.y_max:
                    lat_max = self.y_max
                if 'Bmap' == self.api_type:
                    bounds.append('{0},{1},{2},{3}'.format(lat_min, lng_min, lat_max, lng_max))
                elif 'Amap' == self.api_type:
                    bounds.append('{0:.5f},{1:.5f}|{2:.5f},{3:.5f}'.format(lng_min, lat_max, lng_max, lat_min))
        return bounds