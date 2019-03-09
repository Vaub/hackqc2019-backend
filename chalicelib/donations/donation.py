import datetime
import uuid


class Donation:

    @staticmethod
    def create_new_from(json):
        return Donation(
            reference=str(uuid.uuid4()),
            from_citizen=json['from'],
            to_recipient=json['to'],
            amount=json['amount'],
            donated_at=datetime.datetime.now(),
        )

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
            "reference": self.reference,
            "from": self.from_citizen,
            "to": self.to_recipient,
            "amount": self.amount,
            "donated_at": self.donated_at.isoformat()
        }
