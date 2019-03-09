CITIZENS = {
    "C_12345": {
        "reference": "C_12345",
        "name": "Bob Citizen",
        "age": 34,
    },
}


def find(citizen):
    return CITIZENS[citizen] if citizen in CITIZENS else None
