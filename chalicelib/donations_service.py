from chalicelib import recipients_service
from chalicelib.donations.donation import Donation
from chalicelib.donations.donations_repository import DonationsDynamoDBRepository

DONATIONS = DonationsDynamoDBRepository.create()


def send_donation(donation_request):
    donation = Donation.create_new_from(donation_request)
    if not donation.is_valid():
        raise Exception('donation is not valid')

    recipient = recipients_service.find_recipient(donation.to_recipient)
    if not recipient:
        raise Exception('not a recipient')

    DONATIONS.put(donation)
    return {
        "donation": donation,
        "recipient": recipient
    }


def find_from_citizen(citizen):
    return DONATIONS.find_by(citizen=citizen)


def find_for_recipient(recipient):
    return DONATIONS.find_by(recipient=recipient)


def find_donations():
    return DONATIONS.get_all()


