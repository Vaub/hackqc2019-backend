import datetime
import uuid
from functools import reduce

import dateutil


def calculate_donated(donations):
    return reduce(lambda acc, donation: acc + donation.amount, donations, 0)


def calculate_donators(donations):
    donators = set([donation.from_citizen for donation in donations])
    return len(donators)


class Donation:

    @staticmethod
    def create_new_from(json):
        return Donation(
            reference=str(uuid.uuid4()),
            from_citizen=json['from'],
            to_recipient=json['to'],
            amount=json['amount'],
            position=json['position'],
            donated_at=datetime.datetime.now(),
        )

    @staticmethod
    def from_json(json):
        json['donated_at'] = dateutil.parser.parse(json['donated_at'])
        return Donation(**json)

    def __init__(self, reference, from_citizen, to_recipient, amount, position, donated_at):
        self.reference = reference
        self.from_citizen = from_citizen
        self.to_recipient = to_recipient
        self.amount = amount
        self.position = position
        self.donated_at = donated_at

    def is_valid(self):
        return self.amount > 0

    def as_json(self):
        return {
            **self.__dict__,
            "donated_at": self.donated_at.isoformat()
        }
