from chalicelib import organizations_service, donations_service
from chalicelib.donations.donation import calculate_donated, calculate_donators
from chalicelib.geolocations.neighborhood_finder import NeighborhoodFinder

NEIGHBORHOODS = NeighborhoodFinder.create()
BY_CITY = {
    'quebec': NEIGHBORHOODS.quebec_city,
    'montreal': NEIGHBORHOODS.montreal,
}


def find_neighborhoods_stats(city, city_neighborhood=None):
    print(f'loading neighborhoods for {city}')
    neighborhoods = BY_CITY[city]()

    print(f'loading organizations')
    organizations = organizations_service.find_organizations()
    print(f'loading donations')
    donations = donations_service.find_donations()

    print('parsing results')
    results = [
        (neighborhood, neighborhood.take_organizations(organizations), neighborhood.take_donations(donations))
        for neighborhood in neighborhoods if not city_neighborhood or neighborhood.is_named(city_neighborhood)
    ]

    print('aggregating results')
    results = [
        {
            "neighborhood": neighborhood,
            "organizations": organizations,
            "donated": calculate_donated(donations),
            "donators": calculate_donators(donations)
        }
        for neighborhood, organizations, donations in results
    ]

    if city_neighborhood:
        return results[0] if len(results) else None

    return results
