import json

import requests
from behave import *

response_codes = {}
request_bodies = {}
api_url = "http://localhost:8000/api/contracts/"
login_url = "http://localhost:8000/api/login/"
email = "magotor1304@gmail.com"
password = "pacheco98"
response_content = {}
request_headers = {}
use_step_matcher("re")


@given("an musician watching his list of contracts")
def step_impl(context):
    user = {
        'email': email,
        'password': password
    }
    response = json.loads(requests.post(url=login_url, data=user).content.decode("UTF-8"))['access']
    request_headers['Authorization'] = f"Bearer {response}"
    print('I sent my data to endpoint :' + api_url)


@when("select a available contract")
def step_impl(context):
    response = requests.get(url=f"{api_url}1/", headers=request_headers)
    status_code = response.status_code
    response_content['VALID'] = response.content
    response_codes['VALID'] = status_code


@then("shows the contract's details")
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200


@when("select a unavailable contract")
def step_impl(context):
    response = requests.get(url=f"{api_url}100/", headers=request_headers)
    status_code = response.status_code
    response_content['INVALID'] = response.content
    response_codes['INVALID'] = status_code


@then('shows the message "Error 404: Contract not founded"')
def step_impl(context):
    response_string = str(response_codes['INVALID'])
    response = response_content['INVALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['INVALID'] == 404
