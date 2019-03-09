ORGS = {
    "12345": {
        "reference": '12345',
        "name": 'Best Org©',
        "description": 'Charity for the poors',
        "position": {
            "x": 3.0,
            "y": -4.0
        },
        "services": []
    },
    "45678": {
        "reference": '45678',
        "name": 'Vi ska gå död',
        "description": 'Det är grattis för dig',
        "position": {
            "x": 3.0,
            "y": -4.0
        },
        "services": []
    }
}


def find_organizations():
    return list(ORGS.values())


def get_organization(reference):
    return ORGS[reference] if reference in ORGS else None
