IN_NEEDS = {
    "R_12345": {
        "reference": "R_12345",
        "pin": "12345",
        "balance": 30.4,
    }
}


def find(citizen):
    return IN_NEEDS[citizen] if citizen in IN_NEEDS else None
