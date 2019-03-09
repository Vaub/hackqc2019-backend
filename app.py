import boto3
from chalice import Chalice, NotFoundError

import chalicelib.recipients_tag_service as recipients_tag_service
from chalicelib import organizations_service, recipients_service, donations_service

app = Chalice(app_name='hackqc2019')


@app.route('/', cors=True)
def index():
    return {'hello': 'world'}


# RECIPIENTS

@app.route('/recipients/{reference}', cors=True)
def find_recipient(reference):
    recipient = recipients_service.find_recipient(reference)
    if not recipient:
        raise NotFoundError()

    return recipient


@app.route('/recipients/{reference}/tag', cors=True)
def generate_recipient_tag(reference):
    return recipients_tag_service.create_tag(reference)


# ORGANIZATIONS

@app.route('/organizations', cors=True)
def find_organizations():
    return organizations_service.find_organizations()


@app.route('/organizations/{reference}', cors=True)
def get_organization(reference):
    organization = organizations_service.get_organization(reference)

    if not organization:
        raise NotFoundError()

    return organization


# DONATIONS

@app.route('/donations', cors=True)
def get_my_donations():
    return []


@app.route('/donations', methods=['POST'], cors=True)
def send_donation():
    donation_request = app.current_request.json_body
    donation = donations_service.send_donation(donation_request)
    return donation.as_json()


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
