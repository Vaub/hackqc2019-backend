import json
from decimal import Decimal

import boto3


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
