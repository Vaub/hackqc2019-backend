from chalicelib import organizations_service, citizens_in_needs_service
from chalicelib.recipients.tag_generator import RecipientTagGenerator

RECIPIENT_TAGS = RecipientTagGenerator.create()


def find_recipient(recipient):
    organization = organizations_service.find_organization(recipient)
    if organization:
        return {
            'reference': recipient,
            'entity': organization.as_json(),
            'type': 'ORGANIZATION',
        }

    citizen_in_needs = citizens_in_needs_service.find_in_needs(recipient)
    if citizen_in_needs:
        return {
            'reference': recipient,
            'entity': citizen_in_needs,
            'type': 'CITIZEN_IN_NEEDS',
        }

    return None


def create_tag(recipient):
    if not find_recipient(recipient):
        raise Exception('recipient does not exists')

    return RECIPIENT_TAGS.create_tag(recipient)
