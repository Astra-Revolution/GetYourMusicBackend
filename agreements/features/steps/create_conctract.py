import json

import requests
from behave import *
from requests.auth import HTTPBasicAuth

response_codes = {}
request_bodies = {}
api_url = "http://localhost:8000/api/organizers/2/musicians/1/contracts/"
login_url = "http://localhost:8000/api/login/"
email = "magotor1304@gmail.com"
password = "pacheco98"
response_content = {}
request_headers = {}
use_step_matcher("re")


@given("an organizer in the register contract form")
def step_impl(context):
    user = {
        'email': email,
        'password': password
    }
    response = json.loads(requests.post(url=login_url, data=user).content.decode("UTF-8"))['access']
    request_headers['Authorization'] = f"Bearer {response}"
    print('I sent my data to endpoint :' + api_url)


@when('send the form with valid data pushing the button "Create Contract"')
def step_impl(context):
    request_bodies['VALID'] = {'name': 'contract',
                               'address': "Mi casa",
                               'reference': 'near',
                               'description': 'Holi',
                               'amount': 500,
                               'start_date': '20-09-2021',
                               'end_date': '21-09-2021',
                               'district_id': 1}
    response = requests.post(url=api_url, data=request_bodies['VALID'], headers=request_headers)
    # print(f'post response : {response.text}')
    status_code = response.status_code
    response_content['VALID'] = response.content
    response_codes['VALID'] = status_code


@then("create and show it in the list of contracts")
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 201


@when('send the form with invalid data pushing the button "Create Contract"')
def step_impl(context):
    request_bodies['INVALID'] = {'name': 'contract',
                                 'reference': 'near',
                                 'description': 'Holi',
                                 'amount': 500,
                                 'start_date': '20-09-2021',
                                 'end_date': '21-09-2021',
                                 'district_id': 1}
    response = requests.post(url=api_url, data=request_bodies['INVALID'], headers=request_headers)
    # print(f'post response : {response.text}')
    status_code = response.status_code
    response_content['INVALID'] = response.content
    response_codes['INVALID'] = status_code


@then("show the same form indicating the wrong fields")
def step_impl(context):
    response_string = str(response_codes['INVALID'])
    response = response_content['INVALID']
    # print(f'Post response content : {response}')
    # print(f'Post response code : {response_string}')
    assert response_codes['INVALID'] == 400


@step("ask to fix them")
def step_impl(context):
    response = response_content['INVALID']
    print(f'Fix the field : {response}')
