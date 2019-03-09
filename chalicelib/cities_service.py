import os

import geojson
import geojson.utils as utils

import chalicelib.geolocations as geolocations


def get_geolocation():
    _load_quebec_neighborhoods()


def _load_quebec_neighborhoods():
    return _load_geojson(file_name='ca-qc-quebec-neighborhoods.geojson')


def _load_geojson(file_name):
    dir_path = os.path.dirname(geolocations.__file__)

    geojson_file = os.path.join(dir_path, file_name)
    with open(geojson_file, 'r') as quebec_neighborhoods:
        return geojson.loads(quebec_neighborhoods.read())
