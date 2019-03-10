import boto3
from chalice import Chalice, NotFoundError

from chalicelib import (
    citizens_service,
    citizens_in_needs_service,
    donations_service,
    organizations_service,
    recipients_service,
    statistics_service)

app = Chalice(app_name='hackqc2019')

ME_CITIZEN = 'C_12345'
ME_ORGANIZATION = '42f6484d-2a42-4e71-bd08-de85be6357ac'
ME_POSITION = {'lat': 46.816480, 'lon': -71.200458}


@app.route('/', cors=True)
def index():
    return {'version': '0.0.1'}


# RECIPIENTS

@app.route('/recipients/{reference}', cors=True)
def find_recipient(reference):
    recipient = recipients_service.find_recipient(reference)
    if not recipient:
        raise NotFoundError()

    return recipient


@app.route('/recipients/{reference}/tag', cors=True)
def generate_recipient_tag(reference):
    return recipients_service.create_tag(reference)


# ORGANIZATIONS

@app.route('/organizations', cors=True)
def find_organizations():
    organizations = organizations_service.find_organizations()

    return {
        "organizations": [organization.as_json() for organization in organizations]
    }


@app.route('/organizations', methods=['POST'], cors=True)
def register_organization():
    request = app.current_request.json_body
    return organizations_service.register_organization(request).as_json()


@app.route('/organizations/me', cors=True)
def my_organization():
    return organizations_service.find_organization(ME_ORGANIZATION)


@app.route('/organizations/me/transactions', cors=True)
def get_organization_transactions():
    transactions = organizations_service.list_transactions(ME_ORGANIZATION)
    return {
        "transactions": [transaction.as_json() for transaction in transactions]
    }


@app.route('/organizations/me/donations', cors=True)
def get_organization_donations():
    donations = donations_service.find_for_recipient(ME_ORGANIZATION)
    return {
        "donations": [donation.as_json() for donation in donations]
    }

@app.route('/organizations/me/redeem', methods=['POST'], cors=True)
def redeem():
    request = app.current_request.json_body

    request['to_organization'] = ME_ORGANIZATION
    return citizens_in_needs_service.redeem(request).as_json()


@app.route('/organizations/{reference}', cors=True)
def get_organization(reference):
    organization = organizations_service.find_organization(reference)

    if not organization:
        raise NotFoundError()

    return organization.as_json()


# CITIZEN


@app.route('/citizens/me', cors=True)
def me():
    return citizens_service.find(ME_CITIZEN)


@app.route('/citizens/me/donations', cors=True)
def get_my_donations():
    donations = donations_service.find_from_citizen(ME_CITIZEN)

    return {
        "donations": [donation.as_json() for donation in donations]
    }


@app.route('/citizens/me/donations', methods=['POST'], cors=True)
def send_donation():
    donation_request = app.current_request.json_body

    donation_request['from'] = ME_CITIZEN
    if 'position' not in donation_request:
        donation_request['position'] = ME_POSITION

    donation = donations_service.send_donation(donation_request)

    return {
        "donation": donation['donation'].as_json(),
        "recipient": {
            "type": donation['recipient']['type'],
            **donation['recipient']['entity'],
        }
    }


# CITIZEN IN NEEDS

@app.route('/citizens/in-needs/{reference}', cors=True)
def get_citizen_in_needs(reference):
    citizen_in_needs = citizens_in_needs_service.find_in_needs(reference)
    if not citizen_in_needs:
        raise NotFoundError()

    return citizen_in_needs


# STATISTICS

@app.route('/statistics', cors=True)
def get_neighborhoods_statistics():
    params = app.current_request.query_params
    if params and 'neighborhood' in params:
        statistics= statistics_service.find_neighborhood_stats(neighborhood=params['neighborhood'])
        return _serialize_neighborhood_statistics(statistics)

    statistics = statistics_service.find_neighborhoods_stats()
    return [_serialize_neighborhood_statistics(s) for s in statistics]


def _serialize_neighborhood_statistics(statistics):
    if not statistics:
        raise NotFoundError()

    return {
        "neighborhood": statistics['neighborhood'].name(),
        "organizations": [o.as_json() for o in statistics['organizations']],
        "donated": statistics['donated'],
        "donators": statistics['donators'],
    }


@app.route('/doc', cors=True)
def swagger():
    apigateway = boto3.client('apigateway')
    context = app.current_request.context

    if 'apiId' not in context:
        return {}

    export = apigateway.get_export(
        restApiId=context['apiId'],
        stageName=context['stage'],
        exportType='oas30',
        parameters={
            "extensions": "apigateway",
        },
        accepts='application/json',
    )

    return export['body'].read().decode('utf-8')

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
