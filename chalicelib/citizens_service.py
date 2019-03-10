CITIZENS = {
    "C_12345": {
        "reference": "C_12345",
        "name": "Bob Citizen",
    },
}


def find(citizen):
    return CITIZENS[citizen] if citizen in CITIZENS else None
