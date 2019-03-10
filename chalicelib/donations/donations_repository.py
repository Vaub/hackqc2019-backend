import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

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
        item = json.loads(json.dumps(donation.as_json()), parse_float=Decimal)

        self._table.put_item(Item={
            "donation": donation.reference,
            **item,
        })

    def get_all(self):
        items = self._table.scan()
        items = items['Items']

        return [_parse_item(item) for item in items]

    def find_by(self, citizen=None, recipient=None):
        if not citizen and not recipient:
            return None

        query = None
        if citizen:
            query = self._table.query(
                IndexName='from_citizen-donation-index',
                KeyConditionExpression=Key('from_citizen').eq(citizen)
            )
        if recipient:
            query = self._table.query(
                IndexName='to_recipient-donation-index',
                KeyConditionExpression=Key('to_recipient').eq(recipient)
            )

        items = query['Items']
        return [_parse_item(item) for item in items]
