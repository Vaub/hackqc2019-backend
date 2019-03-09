import boto3

from chalicelib.donations.donation import Donation


def _parse_item(item):
    item['reference'] = item['donation']
    item.pop('donation', None)

    return Donation.from_json(item)


class DonationsDynamoDBRepository:

    @staticmethod
    def create():
        table = boto3.resource('dynamodb').Table('hackqc2019-donations')
        return DonationsDynamoDBRepository(table)

    def __init__(self, table):
        self._table = table

    def put(self, donation):
        self._table.put_item(Item={
            "donation": donation.reference,
            **donation.as_json(),
        })

    def find_by(self, citizen=None, recipient=None):
        if not citizen and not recipient:
            return None

        item = None
        if citizen:
            item = self._table.get_item(Key={"from_citizen": citizen})
        if recipient:
            item = self._table.get_item(Key={"to_recipient", recipient})

        return _parse_item(item['Item']) if 'Item' in item else None
