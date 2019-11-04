import json

from app.user import user_lambda
from app.base import exception
from test import UserTestCase
from app.user.users import service


class UserCreateTestCase(UserTestCase):

    def test_post(self):
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')

        response = user_lambda.post_user(event, None)

        self.assertIsNotNone(response['body'])
        self.assertEqual(response['statusCode'], 201)

    def test_get(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = user_lambda.post_user(event, None)

        # Get id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': user_dict['email']})
        retrieved_user = user_lambda.get_user(event, None)

        self.assertIsNotNone(retrieved_user)

    def test_delete(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = user_lambda.post_user(event, None)

        # Delete id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='DELETE', pathParameters={'id': user_dict['email']})
        deleted_response = user_lambda.delete_user(event, None)

        # Get id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': user_dict['email']})
        self.assertRaises(exception.EntityNotFoundError, user_lambda.get_user, event, None)

    def test_list(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = user_lambda.post_user(event, None)

        # List
        event = dict(httpMethod='GET')
        page_string = user_lambda.list_user(event, None)
        self.assertIsNotNone(page_string)

        # Delete id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='DELETE', pathParameters={'id': user_dict['email']})
        deleted_response = user_lambda.delete_user(event, None)