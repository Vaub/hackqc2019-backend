from shapely.geometry import Point


class Neighborhood:

    @staticmethod
    def from_geojson_feature(feature, name_key):
        return Neighborhood(feature['properties'], feature['shape'], name_key)

    def __init__(self, properties, shape, name_key):
        self._properties = properties
        self._shape = shape
        self._name_key = name_key

    def take_organizations(self, organizations):
        organizations = filter(lambda o: self.contains(o.position), organizations)
        return list(organizations)

    def take_donations(self, donations):
        donations = filter(lambda d: self.contains(d.position), donations)
        return list(donations)

    def contains(self, position):
        lon, lat = position['lon'], position['lat']
        return self._shape.contains(Point(lon, lat))

    def is_named(self, name):
        return self.name() == name

    def name(self):
        return self._properties[self._name_key]
