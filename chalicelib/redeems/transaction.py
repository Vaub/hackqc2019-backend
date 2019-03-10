import datetime
import uuid

import dateutil


class Transaction:

    @staticmethod
    def create_new(json):
        return Transaction(
            **json,
            reference=str(uuid.uuid4()),
            redeemed_at=datetime.datetime.now()
        )

    @staticmethod
    def from_json(json):
        data = {
            **json,
            "redeemed_at": dateutil.parser.parse(json['redeemed_at'])
        }

        return Transaction(**data)

    def __init__(self, reference, from_recipient, to_organization, amount, service, redeemed_at):
        self.reference = reference
        self.redeemed_at = redeemed_at
        self.service = service
        self.amount = amount
        self.to_organization = to_organization
        self.from_recipient = from_recipient

    def is_valid(self):
        return self.amount > 0

    def as_json(self):
        return {
            **self.__dict__,
            "redeemed_at": self.redeemed_at.isoformat()
        }
