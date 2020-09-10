# Map Spider

> Map Spider is a tool to search and acquire pois and streetview data from the apis of Amap and Bmap.

## POI Spider
### Usage
```python
from poi_spider.map_poi_spider import BmapPoiSpider, AmapPoiSpider
from poi_spider.utils import RegionDivision

if __name__ == '__main__':
    # The rectangle area you wan to search
    extent = [39.900, 116.385, 39.995, 116.435]
    # Divide the given area into fine parts in order to avoid reach query limits
    # You can set precision to other values, remember, the higher the precision is, the more data you get
    # and the more time the program consumes
    amap_bounds = RegionDivision(extent, precision=0.02, api_type='Amap').generate_bounds()
    # Search by keywords, area and your apikey
    amap_poi_spider = AmapPoiSpider(amap_bounds, '9c538d0d20ffed4cc35f78bc6c41d9fd', keywords=['快餐', '医院'])
    # Convert the acquired records in the form of poi
    amap_poi_spider.get_all_pois()
    # Output the pois acuqired (csv or geojson)
    amap_poi_spider.to_csv()
    # You can also give the filename you are in favour of
    amap_poi_spider.to_geojson(filename='bmap_poi')
    print('Done!')
```
### Output structure
> .csv file

| name | type | lng | lat |
| ---- | ---- | ---- | ---- |
| 麦当劳(交通口餐厅) | cater | 116.415862 | 39.947472 |
| ... | ... | ... | ... |

> .geojson file

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [116.423801, 39.971425]},
      "properties": {"name": "护国寺小吃(和平西街店)", "type": "cater"}
    },
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [116.445986, 39.966328]},
      "properties": {"name": "南城香(国展店)", "type": "cater"}
    }
  ]
}
```
---
## StreetView Spider
### Usage
```python
from streetview_spider.map_streetview_spider import BmapStreetViewSpider
from typing import List

locations: List[str] = []

with open('path/to/places.csv', 'r') as f:
    for line in f.readlines():
        locations.append(line)

bmap_streetview_spider = BmapStreetViewSpider(api_key='hM9GzOGeQVHvXi6lM0iLjfd2uEidhfYm', locations=locations)
bmap_streetview_spider.search_streeview_images().download(path='path/to/street_view_imgs')
```
### Output
![](https://github.com/Vezarachan/map_spider/blob/master/examples/streetview_imgs/sv_116.35_40.04778.png)
![](https://github.com/Vezarachan/map_spider/blob/master/examples/streetview_imgs/sv_116.3_%2040.04778.png)


## TODO
- [x] POI Spider (Amap & Bmap)
- [x] StreetView Spider 
- [ ] GUI (based on Web or PyQT)

## Current Projects
- **[quadtree-py](https://github.com/Vezarachan/quadtree-py)** - A quadtree implementation in pure Python
- **[cocopulas](https://github.com/Vezarachan/cocopulas)** - A Python lib for copulas (elliptical, archimedean copulas)
- **map_spider** - A spider searching for POI and streetview from Amap and Bmap

## Next Projects
- **KD-Tree** - The k-dimensional tree implementation in Python
- **V2ML** - Way to Machine Learning (Courses from Hung-yi Lee in NTU)
- **GeoBayesian** - Combination of Spatial Analysis and Bayesian Data Analysis
- **MicroGIS** - A lightweight, full-function, modern GIS based on C++
