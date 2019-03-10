import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

from chalicelib.redeems.transaction import Transaction


def _parse_item(item):
    item['reference'] = item['transaction']
    item.pop('transaction', None)

    return Transaction.from_json(item)


class TransactionsDynamoDBRepository:

    @staticmethod
    def create():
        table = boto3.resource('dynamodb').Table('hackqc2019-transactions')
        return TransactionsDynamoDBRepository(table)

    def __init__(self, table):
        self._table = table

    def put(self, transaction):
        item = json.loads(json.dumps(transaction.as_json()), parse_float=Decimal)

        self._table.put_item(Item={
            "transaction": transaction.reference,
            **item,
        })

    def list_for(self, organization=None):
        if not organization:
            return []

        query = self._table.query(
            IndexName='to_organization-transaction-index',
            KeyConditionExpression=Key('to_organization').eq(organization)
        )

        items = query['Items']
        return [_parse_item(item) for item in items]
