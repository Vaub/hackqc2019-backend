from chalicelib.redeems.transaction import Transaction
from chalicelib.redeems.transactions_repository import TransactionsDynamoDBRepository

IN_NEEDS = {
    "R_12345": {
        "reference": "R_12345",
        "pin": "12345",
        "balance": 30.4,
    }
}

TRANSACTIONS = TransactionsDynamoDBRepository.create()


def find_in_needs(citizen):
    return IN_NEEDS[citizen] if citizen in IN_NEEDS else None


def redeem(transaction_request):
    transaction = Transaction.create_new(transaction_request)

    if not transaction.is_valid():
        raise Exception('not a valid transaction')
    if not find_in_needs(transaction.from_recipient):
        raise Exception('not a valid citizen in needs')

    TRANSACTIONS.put(transaction)
    return transaction
