from requests.models import Response
from poi_spider import *
from .utils import AMAP_API, BMAP_APi
import logging


class BmapPoiSpider(object):
    keyword: str
    bounds: List[str]
    api_key: str
    record_count: int  = 0

    def __init__(self, keyword: str, bounds: List[str], api_key: str):
        self.keyword = keyword
        self.bounds = bounds
        self.api_key = api_key

    # get records of nth page in given bound
    def __get_all_records(self, bound: str, page_num: int) -> bool:
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
            print('Getting data ......')
            response: Response = requests.get(BMAP_APi, params=params)
            records = json.loads(response.text)
        except Exception as e:
            logging.error('fail to acquire records ', e)

        if records.get('total', 0) == 0:
            logging.error('get no record')
            return False
        else:
            print('Writing file ......')
            # convert into form of poi
            with open(os.path.abspath(os.curdir) + '/' + self.keyword + 'poi.csv', 'a') as f:
                for record in records['results']:
                    self.record_count += 1
                    f.writelines('{0},{1},{2},{3}\n'.format(record['name'], record['detail_info']['type'], record['location']['lat'], record['location']['lng']))

        return True

    # get all the pois
    def get_all_pois(self):
        for bound in self.bounds:
            count = 1
            while count <= 20 and self.__get_all_records(bound, count):
                self.__get_all_records(bound, count)
                count += 1
        print('There is ', self.record_count, ' records.')


class AmapPoiSpider(object):
    keywords: str
    bounds: List[str]
    api_key: str
    record_count: int = 0

    def __init__(self, bounds: List[str], api_key: str, keywords: List[str], ):
        self.keywords = '|'.join(keywords)
        self.bounds = bounds
        self.api_key = api_key

    def __get_all_records(self, bound: str, page_num: int):
        params = {
            'keywords': self.keywords,
            'polygon': bound,
            'offset': 25,
            'page': page_num,
            'key': self.api_key,
            'output': 'json'
        }

        try:
            print('Getting data ......')
            response: Response = requests.get(AMAP_API, params=params)
            records = json.loads(response.text)
        except Exception as e:
            logging.error('fail to acquire records ', e)

        if records['count'] == 0:
            logging.error('get 0 record')
            return False
        else:
            print('Writing file ......')
            # convert into form of poi
            with open(os.path.abspath(os.curdir) + '/' + self.keywords + 'poi.csv', 'a') as f:
                for record in records['pois']:
                    self.record_count += 1
                    lng, lat = record['location'].split(',')
                    f.writelines('{0},{1},{2},{3}\n'.format(record['name'], record['type'], lng, lat))

        return True

    # get all the pois
    def get_all_pois(self):
        for bound in self.bounds:
            count = 1
            while count <= 25 and self.__get_all_records(bound, count):
                self.__get_all_records(bound, count)
                count += 1
        print('There is ', self.record_count, ' records.')






