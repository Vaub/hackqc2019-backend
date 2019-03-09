from chalicelib.donations.donation import Donation
from chalicelib.donations.donations_repository import DonationsDynamoDBRepository

DONATIONS = DonationsDynamoDBRepository.create()


def send_donation(donation_request):
    donation = Donation.create_new_from(donation_request)
    if not donation.is_valid():
        raise Exception('donation is not valid')

    DONATIONS.put(donation)
    return donation


def find_from_citizen(citizen):
    return DONATIONS.find_by(citizen=citizen)
