from poi_spider.map_poi_spider import BmapPoiSpider, AmapPoiSpider
from poi_spider.utils import RegionDivision

if __name__ == '__main__':
    extent = [39.900, 116.385, 39.995, 116.435]
    # bmap_bounds = RegionDivision(extent, precision=0.02, api_tyoe='Bmap').generate_bounds()
    # for bound in bmap_bounds:
    #     print(bound)
    # bmap_poi_spider = BmapPoiSpider('快餐', bmap_bounds, 'hM9GzOGeQVHvXi6lM0iLjfd2uEidhfYm')
    # bmap_poi_spider.get_all_pois()
    amap_bounds = RegionDivision(extent, precision=0.02, api_tyoe='Amap').generate_bounds()
    for bound in amap_bounds:
        print(bound)
    amap_poi_spider = AmapPoiSpider(amap_bounds, '9c538d0d20ffed4cc35f78bc6c41d9fd', keywords=['快餐', '医院'])
    amap_poi_spider.get_all_pois()
    print('Done!')
