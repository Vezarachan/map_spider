import requests
import json
from typing import List, Dict
import os
import logging
from geojson import FeatureCollection, Feature, Point, dumps

logging.basicConfig(filename=os.path.abspath(os.curdir) + '/logger.log', level=logging.INFO)
logging.StreamHandler.level = logging.INFO
