from chalicelib.donations.donation import Donation


def send_donation(donation_request):
    donation = Donation.create_new_from(donation_request)
    if not donation.is_valid():
        raise Exception('donation is not valid')

    return donation
