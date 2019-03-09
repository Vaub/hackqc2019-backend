from chalicelib import organizations_service
from chalicelib.recipients.tag_generator import RecipientTagGenerator

RECIPIENT_TAGS = RecipientTagGenerator.create()

def find_recipient(recipient):
    organization = organizations_service.find_organization(recipient)
    if organization:
        return {
            'reference': recipient,
            'type': 'ORGANIZATION'
        }

    return None


def create_tag(recipient):
    if not find_recipient(recipient):
        raise Exception('recipient does not exists')

    return RECIPIENT_TAGS.create_tag(recipient)
