import json

import requests
from behave import *

response_codes = {}
request_bodies = {}
api_url = "http://localhost:8000/api/contracts/1/contract_states/"
api_url_contracts = "http://localhost:8000/api/musicians/3/contracts/"
login_url = "http://localhost:8000/api/login/"
email = "albieri1304@gmail.com"
password = "albieri98"
response_content = {}
request_headers = {}
use_step_matcher("re")


@given("A musician who receives a contract proposal from an event organizer")
def step_impl(context):
    user = {
        'email': email,
        'password': password
    }
    response = json.loads(requests.post(url=login_url, data=user).content.decode("UTF-8"))['access']
    request_headers['Authorization'] = f"Bearer {response}"
    print('I sent my data to endpoint :' + api_url)


@when('Press the option "accept contract"')
def step_impl(context):
    request_bodies['VALID'] = {}
    response = requests.patch(url=api_url + '2/', data=request_bodies['VALID'], headers=request_headers)
    status_code = response.status_code
    response_content['VALID'] = response.content
    response_codes['VALID'] = status_code


@then('a message is displayed with the question "Are you sure you accept this contract" it is confirmed again')
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200


@step("the list of accepted contracts is shown to the musician")
def step_impl(context):
    request_bodies['VALID'] = {}
    response = requests.get(url=api_url_contracts, data=request_bodies['VALID'], headers=request_headers)
    status_code = response.status_code
    response_content['VALID'] = response.content
    response_codes['VALID'] = status_code

    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200


@when('Press the option "reject contract"')
def step_impl(context):
    request_bodies['VALID'] = {}
    response = requests.patch(url=api_url + '3/', data=request_bodies['VALID'], headers=request_headers)
    status_code = response.status_code
    response_content['VALID'] = response.content
    response_codes['VALID'] = status_code


@then('a message is displayed with the question "Are you sure to reject this contract", it is confirmed again')
def step_impl(context):
    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200


@step("the list of rejected contracts is shown to the musician")
def step_impl(context):
    request_bodies['VALID'] = {}
    response = requests.get(url=api_url_contracts, data=request_bodies['VALID'], headers=request_headers)
    status_code = response.status_code
    response_content['VALID'] = response.content
    response_codes['VALID'] = status_code

    response_string = str(response_codes['VALID'])
    response = response_content['VALID']
    print(f'Post response content : {response}')
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 200
