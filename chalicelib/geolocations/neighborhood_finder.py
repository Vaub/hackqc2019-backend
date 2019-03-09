import io

import boto3
import geojson
from shapely.geometry import shape

from chalicelib.geolocations.neighborhood import Neighborhood


def _download_geojson(geojson_object):
    with io.BytesIO() as data:
        geojson_object.download_fileobj(data)

        data.seek(0)
        json = geojson.loads(data.read())

        return [
            {
                "properties": feature.properties,
                "shape": shape(feature.geometry)
            } for feature in json.features
        ]


class NeighborhoodFinder:

    @staticmethod
    def create():
        bucket = boto3.resource('s3').Bucket('hackqc2019')
        return NeighborhoodFinder(bucket)

    def __init__(self, bucket):
        self._bucket = bucket
        self._quebec_city = bucket.Object('neighborhoods/ca-qc-quebec-neighborhoods.geojson')

    def quebec_city(self):
        quebec_city = _download_geojson(self._quebec_city)
        return [Neighborhood.from_geojson_feature(feature) for feature in quebec_city]
