from chalicelib.organizations.organization import Organization
from chalicelib.organizations.organization_repository import OrganizationDynamoDBRepository
from chalicelib.redeems.transactions_repository import TransactionsDynamoDBRepository

ORGANIZATIONS = OrganizationDynamoDBRepository.create()
TRANSACTIONS = TransactionsDynamoDBRepository.create()


def find_organizations():
    return ORGANIZATIONS.get_all()


def find_organization(reference):
    return ORGANIZATIONS.find(reference)


def register_organization(request):
    organization = Organization.create_new(request)
    ORGANIZATIONS.put(organization)

    return organization


def list_transactions(organization):
    return TRANSACTIONS.list_for(organization=organization)
