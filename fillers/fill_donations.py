import random
import time

from chalicelib import donations_service
from chalicelib.geolocations.neighborhood_finder import NeighborhoodFinder

NEIGHBORHOODS = NeighborhoodFinder.create()


def main():
    neighborhoods = NEIGHBORHOODS.quebec_city()

    citizens = ["C_12345", "C_23456", "C_34567", "C_45678", "C_56789"]
    recipients = ["R_12345", "R_23456", "R_34567", "R_45678", "R_56789"]

    for i in range(1000):
        neighborhood = neighborhoods[random.randint(0, len(neighborhoods) - 1)]
        position = neighborhood._shape.representative_point()
        position = {"lon": position.x, "lat": position.y}

        amount = random.randint(1, 8)
        donations_service.send_donation(
            {
                "from": citizens[random.randint(0, 4)],
                "to": recipients[random.randint(0, 4)],
                "amount": amount,
                "position": position,
            }
        )

if __name__ == '__main__':
    main()
