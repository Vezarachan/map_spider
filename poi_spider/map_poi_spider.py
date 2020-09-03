from requests.models import Response
from poi_spider import *
from .utils import AMAP_API, BMAP_APi, NoRecordsError


class BmapPoiSpider(object):
    keyword: str
    bounds: List[str]
    api_key: str
    record_count: int = 0
    pois: List[Dict] = list()

    def __init__(self, keyword: str, bounds: List[str], api_key: str):
        self.keyword = keyword
        self.bounds = bounds
        self.api_key = api_key

    # get records of nth page in given bound
    def __get_all_records(self, bound: str, page_max: int) -> List[dict]:
        records: List[Dict] = list()

        for page_num in range(1, page_max + 1):
            params = {
                'query': self.keyword,
                'bounds': bound,
                'ak': self.api_key,
                'page_size': 20,
                'page_num': page_num,
                'output': 'json',
                'coord_type': 1,
                'scope': 2
            }

            try:
                logging.info('Getting data -- keyword:{0}'.format(self.keyword))
                response: Response = requests.get(BMAP_APi, params=params)
                poi_json = json.loads(response.text)
            except requests.exceptions.ConnectionError as e:
                logging.error('Connection Error -- ', e)
            except requests.exceptions.HTTPError as e:
                logging.error('Http error -- ', e)

            if poi_json.get('total', 0) == 0:
                logging.error('Got 0 record')
                break
            else:
                logging.info('Converting data ......')
                pois = poi_json['results']
                for poi in pois:
                    self.record_count += 1
                    records.append(
                        {'name': poi['name'],
                         'type': poi['detail_info']['type'],
                         'lng': poi['location']['lng'],
                         'lat': poi['location']['lat']}
                    )
        return records

    def get_all_pois(self):
        for bound in self.bounds:
            for poi in self.__get_all_records(bound, 20):
                self.pois.append(poi)
        print('There is ', self.record_count, ' records.')

    def to_csv(self, filename: str = None):
        logging.info('Writing file as csv  ......')
        if filename is None:
            path = os.path.abspath(os.curdir) + '/poi.csv'
        else:
            path = '{0}/{1}.csv'.format(os.path.abspath(os.curdir), filename)
        with open(path, 'a') as f:
            f.writelines(','.join(self.pois[0].keys()) + '\n')
            for poi in self.pois:
                f.writelines(
                    '{0},{1},{2},{3}\n'.format(poi['name'], poi['type'], poi['lng'], poi['lat']))

    def to_geojson(self, filename: str = None):
        logging.info('Writing file as geojson')
        features = list()
        if filename is None:
            path = os.path.abspath(os.curdir) + '/poi.geojson'
        else:
            path = '{0}/{1}.geojson'.format(os.path.abspath(os.curdir), filename)
        for poi in self.pois:
            feature = Feature(geometry=Point((poi['lng'], poi['lat'])), properties={'name': poi['name'], 'type': poi['type']})
            features.append(feature)
        feature_collection = FeatureCollection(features)
        with open(path, 'a') as f:
            f.write(dumps(feature_collection))


class AmapPoiSpider(object):
    keywords: str
    bounds: List[str]
    api_key: str
    record_count: int = 0
    pois: List[Dict] = list()

    def __init__(self, bounds: List[str], api_key: str, keywords: List[str], ):
        self.keywords = '|'.join(keywords)
        self.bounds = bounds
        self.api_key = api_key

    def __get_all_records(self, bound: str, page_max: int) -> List[Dict]:
        records: List[Dict] = list()

        for page_num in range(1, page_max + 1):
            params = {
                'keywords': self.keywords,
                'polygon': bound,
                'offset': 25,
                'page': page_num,
                'key': self.api_key,
                'output': 'json'
            }

            try:
                logging.info('Getting data  -- keyword:{0}'.format(self.keywords))
                response: Response = requests.get(AMAP_API, params=params)
                poi_json = json.loads(response.text)
            except requests.exceptions.ConnectionError as e:
                logging.error('Connection Error -- ', e)
            except requests.exceptions.HTTPError as e:
                logging.error('Http error -- ', e)

            if poi_json['count'] == 0:
                logging.error('get 0 record')
                break
            else:
                logging.info('Converting data ......')
                pois = poi_json['pois']
                for poi in pois:
                    self.record_count += 1
                    lng, lat = poi['location'].split(',')
                    records.append(
                        {'name': poi['name'],
                         'type': poi['type'],
                         'lng': lng,
                         'lat': lat
                         })
        return records

    # get all the pois
    def get_all_pois(self):
        for bound in self.bounds:
            for poi in self.__get_all_records(bound, 20):
                self.pois.append(poi)
        print('There is ', self.record_count, ' records.')

    def to_csv(self, filename: str = None):
        logging.info('Writing file as csv  ......')
        if filename is None:
            path = os.path.abspath(os.curdir) + '/poi.csv'
        else:
            path = '{0}/{1}.csv'.format(os.path.abspath(os.curdir), filename)
        with open(path, 'a') as f:
            f.writelines(','.join(self.pois[0].keys()) + '\n')
            for poi in self.pois:
                f.writelines(
                    '{0},{1},{2},{3}\n'.format(poi['name'], poi['type'], poi['lng'], poi['lat']))

    def to_geojson(self, filename: str = None):
        logging.info('Writing file as geojson')
        features = list()
        if filename is None:
            path = os.path.abspath(os.curdir) + '/poi.geojson'
        else:
            path = '{0}/{1}.geojson'.format(os.path.abspath(os.curdir), filename)
        for poi in self.pois:
            feature = Feature(geometry=Point((poi['lng'], poi['lat'])),
                              properties={'name': poi['name'], 'type': poi['type']})
            features.append(feature)
        feature_collection = FeatureCollection(features)
        with open(path, 'a') as f:
            f.write(dumps(feature_collection))
