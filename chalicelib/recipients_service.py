from chalicelib.organizations_service import ORGS


def find_recipient(recipient):
    if recipient in ORGS:
        return {
            'reference': recipient,
            'type': 'ORGANIZATION'
        }

    return None
