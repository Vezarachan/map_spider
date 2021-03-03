"""
@author: Leon Elaiza
@license: MIT license
@contact: xiayin_lou@stu.pku.edu.cn
@file: xiamen_poi.py
@time: 2020/9/28 3:04 下午
@desc: 
"""
from poi_spider.map_poi_spider import BmapPoiSpider, AmapPoiSpider
from poi_spider.utils import RegionDivision

if __name__ == '__main__':
    extent = [24.420, 118.056, 24.562, 118.212]
    # bmap_bounds = RegionDivision(extent, precision=0.01, api_tyoe='Bmap').generate_bounds()
    # for bound in bmap_bounds:
    #     print(bound)
    # bmap_poi_spider = BmapPoiSpider('地铁站', bmap_bounds, 'hM9GzOGeQVHvXi6lM0iLjfd2uEidhfYm')
    # bmap_poi_spider.get_all_pois()
    # bmap_poi_spider.to_csv(filename='xiamen_parking_log')
    # bmap_poi_spider.to_geojson(filename='xiamen_parking_log')
    amap_bounds = RegionDivision(extent, precision=0.02, api_tyoe='Amap').generate_bounds()
    for bound in amap_bounds:
        print(bound)
    amap_poi_spider = AmapPoiSpider(amap_bounds, '9c538d0d20ffed4cc35f78bc6c41d9fd', keywords=['地铁'])
    amap_poi_spider.get_all_pois()
    amap_poi_spider.to_csv(filename='xiamen_subway')
    amap_poi_spider.to_geojson(filename='xiamen_subway')
    print('Done!')

