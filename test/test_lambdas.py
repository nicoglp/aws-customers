import json

from app import api_lambda
from app.base import exception
from test import UserTestCase
from app.users import service


class UserCreateTestCase(UserTestCase):

    def test_post(self):
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')

        response = api_lambda.post(event, None, service)

        self.assertIsNotNone(response['body'])
        self.assertEqual(response['statusCode'], 201)

    def test_get(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = api_lambda.post(event, None, service)

        # Get id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': user_dict['email']})
        retrieved_user = api_lambda.get(event, None, service)

        self.assertIsNotNone(retrieved_user)

    def test_delete(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = api_lambda.post(event, None, service)

        # Delete id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='DELETE', pathParameters={'id': user_dict['email']})
        deleted_response = api_lambda.delete(event, None, service)

        # Get id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': user_dict['email']})
        self.assertRaises(exception.EntityNotFoundError, api_lambda.get, event, None, service)

    def test_list(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = api_lambda.post(event, None, service)

        # List
        event = dict(httpMethod='GET')
        page_string = api_lambda.list(event, None, service)
        self.assertIsNotNone(page_string)

        # Delete id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='DELETE', pathParameters={'id': user_dict['email']})
        deleted_response = api_lambda.delete(event, None, service)