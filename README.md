# Map Spider

> Search and acquire pois and streetview data from the apis of Amap and Bmap.

## Usage
```python
from poi_spider.map_poi_spider import BmapPoiSpider, AmapPoiSpider
from poi_spider.utils import RegionDivision

if __name__ == '__main__':
    # The rectangle area you wan to search
    extent = [39.900, 116.385, 39.995, 116.435]
    # Divide the given area into fine parts in order to avoid reach query limits
    # You can set precision to other values, remember, the higher the precision is, the more data you get
    # and the more time the program consumes
    amap_bounds = RegionDivision(extent, precision=0.02, api_tyoe='Amap').generate_bounds()
    # Search by keywords, area and your apikey
    amap_poi_spider = AmapPoiSpider(amap_bounds, '9c538d0d20ffed4cc35f78bc6c41d9fd', keywords=['快餐', '医院'])
    # Get all the pois and save it as 'csv' file
    amap_poi_spider.get_all_pois()
    print('Done!')
```
