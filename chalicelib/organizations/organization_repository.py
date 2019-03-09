import json
from decimal import Decimal

import boto3

from chalicelib.organizations.organization import Organization


def _parse_item(item):
    item['reference'] = item['organization']
    item.pop('organization', None)

    return Organization.from_json(item)


class OrganizationDynamoDBRepository:

    @staticmethod
    def create():
        table = boto3.resource('dynamodb').Table('hackqc2019-organizations')
        return OrganizationDynamoDBRepository(table)

    def __init__(self, table):
        self._table = table

    def put(self, organization):
        item = json.loads(json.dumps(organization.as_json()), parse_float=Decimal)

        self._table.put_item(Item={
            "organization": organization.reference,
            **item,
        })

    def find(self, organization):
        item = self._table.get_item(Key={"organization": organization})
        return _parse_item(item['Item']) if 'Item' in item else None

    def get_all(self):
        items = self._table.scan()['Items']
        return [_parse_item(item) for item in items]
