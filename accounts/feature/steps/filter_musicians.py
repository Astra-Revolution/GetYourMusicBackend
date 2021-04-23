import json

import requests

from behave import *

response_codes = {}
request_bodies = {}
api_url = "http://localhost:8000/api/musicians-filter/"
login_url = "http://localhost:8000/api/login/"
email = "albieri1304@gmail.com"
password = "albieri98"
response_content = {}
request_headers = {}
use_step_matcher("re")


@given("An event organizer in the musicians search view")
def step_impl(context):
    user = {
        'email': email,
        'password': password
    }
    response = json.loads(requests.post(url=login_url, data=user).content.decode("UTF-8"))['access']
    request_headers['Authorization'] = f"Bearer {response}"
    print('I sent my data to endpoint :' + api_url)


@when("Enter in the search bar by name, the name of one or many existing musicians")
def step_impl(context):
    request_bodies['VALID'] = {'name': 'Raphael'}
    response = requests.post(url=api_url, data=request_bodies['VALID'], headers=request_headers)
    status_code = response.status_code
    response_content['VALID'] = response.content
    response_codes['VALID'] = status_code


@then("a list of musicians profiles that match the name entered is displayed")
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200


@when("Enter in the search bar by name, the name of a musician that does not exist")
def step_impl(context):
    request_bodies['VALID'] = {'name': 'Rafinha'}
    response = requests.post(url=api_url, data=request_bodies['VALID'], headers=request_headers)
    if len(response.content) > 0:
        status_code = response.status_code
        response_content['VALID'] = response.content
        response_codes['VALID'] = status_code
    else:
        request_bodies['VALID'] = {'name': ''}
        response = requests.post(url=api_url, data=request_bodies['VALID'], headers=request_headers)
        status_code = response.status_code
        response_content['VALID'] = response.content
        response_codes['VALID'] = status_code


@then("a list of suggested musicians' profiles according to the organizer's previous hires is displayed")
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200


@when("Select the search filters you want and there are musicians that match the filters")
def step_impl(context):
    request_bodies['VALID'] = {'genre': 3}
    response = requests.post(url=api_url, data=request_bodies['VALID'], headers=request_headers)
    if len(response.content) > 0:
        status_code = response.status_code
        response_content['VALID'] = response.content
        response_codes['VALID'] = status_code
    else:
        request_bodies['VALID'] = {'genre': ''}
        response = requests.post(url=api_url, data=request_bodies['VALID'], headers=request_headers)
        status_code = response.status_code
        response_content['VALID'] = response.content
        response_codes['VALID'] = status_code


@then("a list of profiles of musicians with characteristics that match the selected filters is displayed")
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200


@then("a list of suggested musician profiles is displayed with characteristics that match the selected filters")
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200
