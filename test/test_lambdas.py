import json

from app import aws_lambda
from test import UserTestCase


class UserCreateTestCase(UserTestCase):

    def test_create(self):
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')

        response = aws_lambda.handler(event, None)

        self.assertIsNotNone(response['body'])
        self.assertEqual(response['statusCode'], 201)

    def test_get(self):
        # Insert Entity
        user_json = self._crete_user_json()
        event = dict(body=user_json, httpMethod='POST')
        create_response = aws_lambda.handler(event, None)

        # Get id
        user_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': user_dict['email']})

        retrieved_user = aws_lambda.handler(event, None)

        self.assertIsNotNone(retrieved_user)
