from behave import given, when, then
import requests
response_codes = {}
request_bodies = {}
api_url = "http://localhost:8000/api/register/"


@given(u'I have entered my data to register')
def step_impl(context):
    print('I sent my data to endpoint :' + api_url)


@when("I press register and set a complete request body")
def step_impl(context):
    request_bodies['VALID'] = {"email": "albieri1304@gmail.com", "password": "albieri98"}
    response = requests.post(url=api_url, data=request_bodies['VALID'])
    print(f'post response : {response.text}')
    status_code = response.status_code
    response_codes['VALID'] = status_code


@then("the result should be HTTP response code 201")
def step_impl(context):
    response_string = str(response_codes['VALID'])
    print(f'Post response code : {response_string}')
    assert response_codes['VALID'] == 201


@given("I have entered my incomplete data to register")
def step_impl(context):
    print('I sent my data to endpoint :' + api_url)


@when("I press register and set a incomplete request Body")
def step_impl(context):
    request_bodies['INVALID'] = {"email": "", "password": "noli98"}
    response = requests.post(url=api_url, data=request_bodies['INVALID'])
    print(f'post response : {response.text}')
    status_code = response.status_code
    response_codes['INVALID'] = status_code


@then("the result should be HTTP response code 400")
def step_impl(context):
    response_string = str(response_codes['INVALID'])
    print(f'Post response code : {response_string}')
    assert response_codes['INVALID'] == 400
