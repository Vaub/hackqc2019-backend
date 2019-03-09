from chalicelib import organizations_service, donations_service
from chalicelib.donations.donation import calculate_donated, calculate_donators
from chalicelib.geolocations.neighborhood_finder import NeighborhoodFinder

NEIGHBORHOODS = NeighborhoodFinder.create()





def find_neighborhoods_stats():
    neighborhoods = NEIGHBORHOODS.quebec_city()

    organizations = organizations_service.find_organizations()
    donations = donations_service.find_donations()

    return [
        {
            "neighborhood": neighborhood,
            "organizations": neighborhood.take_organizations(organizations),
            "donated": calculate_donated(neighborhood.take_donations(donations)),
            "donators": calculate_donators(neighborhood.take_donations(donations))
        }
        for neighborhood in neighborhoods
    ]


def find_neighborhood_stats(neighborhood):
    statistics = find_neighborhoods_stats()
    statistics = filter(lambda s: s['neighborhood'].is_named(neighborhood), statistics)
    statistics = list(statistics)

    if not len(statistics):
        return None

    return statistics[0]


def _find_neighborhood_for(position):
    neighborhood = filter(lambda n: n.contains(position), NEIGHBORHOODS.quebec_city())
    neighborhood = list(neighborhood)

    if (len(neighborhood)) == 0:
        return None

    return neighborhood[0]


