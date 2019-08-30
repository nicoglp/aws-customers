import json

from app import aws_lambda
from app.base import exception
from test import UserTestCase


class UserCreateTestCase(UserTestCase):

    def test_post(self):
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')

        response = aws_lambda.post(event, None)

        self.assertIsNotNone(response['body'])
        self.assertEqual(response['statusCode'], 201)

    def test_get(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = aws_lambda.post(event, None)

        # Get id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': user_dict['email']})
        retrieved_user = aws_lambda.get(event, None)

        self.assertIsNotNone(retrieved_user)

    def test_delete(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = aws_lambda.post(event, None)

        # Delete id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='DELETE', pathParameters={'id': user_dict['email']})
        deleted_response = aws_lambda.delete(event, None)

        # Get id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': user_dict['email']})
        self.assertRaises(exception.EntityNotFoundError, aws_lambda.get, event, None)

    def test_list(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = aws_lambda.post(event, None)

        # List
        event = dict(httpMethod='GET')
        page_string = aws_lambda.list(event, None)
        self.assertIsNotNone(page_string)

        # Delete id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='DELETE', pathParameters={'id': user_dict['email']})
        deleted_response = aws_lambda.delete(event, None)