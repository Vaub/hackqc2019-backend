import boto3
from chalice import Chalice, NotFoundError

from chalicelib import (
    citizens_service,
    citizens_in_needs_service,
    donations_service,
    organizations_service,
    recipients_service,
)

app = Chalice(app_name='hackqc2019')


@app.route('/', cors=True)
def index():
    return {'version': '0.0.1'}


# RECIPIENTS

@app.route('/recipients/{reference}', cors=True)
def find_recipient(reference):
    recipient = recipients_service.find_recipient(reference)
    if not recipient:
        raise NotFoundError()

    uri_params = app.current_request.uri_params
    if 'lon' in uri_params and 'lat' in uri_params:
        print(f'location given ({uri_params.lon},{uri_params.lat})')

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
    me = "12345"
    return organizations_service.find_organization(me)


@app.route('/organizations/{reference}', cors=True)
def get_organization(reference):
    organization = organizations_service.find_organization(reference)

    if not organization:
        raise NotFoundError()

    return organization

# CITIZEN


@app.route('/citizens/me')
def me():
    me_citizen = 'C_12345'
    return citizens_service.find(me_citizen)


@app.route('/donations', cors=True)
def get_my_donations():
    return {
        "donations": []
    }


@app.route('/citizens/me/donations', methods=['POST'], cors=True)
def send_donation():
    donation_request = app.current_request.json_body
    donation = donations_service.send_donation(donation_request)
    return donation.as_json()


# CITIZEN IN NEEDS

@app.route('/citizens/in-needs/{reference}', cors=True)
def get_citizen_in_needs(reference):
    citizen_in_needs = citizens_in_needs_service.find(reference)
    if not citizen_in_needs:
        raise NotFoundError()

    return citizen_in_needs


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
