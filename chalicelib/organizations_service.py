from chalicelib.organizations.organization import Organization
from chalicelib.organizations.organization_repository import OrganizationDynamoDBRepository

ORGANIZATIONS = OrganizationDynamoDBRepository.create()


def find_organizations():
    return ORGANIZATIONS.get_all()


def find_organization(reference):
    return ORGANIZATIONS.find(reference)


def register_organization(request):
    organization = Organization.create_new(request)
    ORGANIZATIONS.put(organization)

    return organization
