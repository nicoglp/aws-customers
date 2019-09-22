import json

from app import api_lambda
from test.claims.providers import ProviderTestCase
from app import provider


class LambdaProviderTestCase(ProviderTestCase):

    def create_provider(self, name="John Lin", address=None, npi="1568412345", type=provider.ProviderType.REFERRING_PROVIDER.value, phone=None):
        provider_json = self._create_provider_json(name, address, npi, type, phone)
        event = dict(body=provider_json, httpMethod='POST')
        response = api_lambda.post(event, None, provider.service)
        return response

    def delete_provider(self, id):
        event = dict(httpMethod='DELETE', pathParameters={'id': id})
        deleted_response = api_lambda.delete(event, None, provider.service)
        return deleted_response

    def test_post(self):
        response = self.create_provider()
        self.assertIsNotNone(response['body'])
        self.assertEqual(response['statusCode'], 201)

        # Delete id
        provider_dict = json.loads(response['body'])
        deleted_response = self.delete_provider(provider_dict['id'])
        self.assertIsNotNone(deleted_response['body'])
        self.assertEqual(deleted_response['statusCode'], 200)

    def test_get(self):
        create_response = self.create_provider()

        # Get id
        provider_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': provider_dict['id']})
        retrieved_user = api_lambda.get(event, None, provider.service)

        self.assertIsNotNone(retrieved_user)

        # Delete id
        deleted_response = self.delete_provider(provider_dict['id'])
        self.assertIsNotNone(deleted_response['body'])
        self.assertEqual(deleted_response['statusCode'], 200)

    def test_list(self):
        create_response = self.create_provider()

        # List
        event = dict(httpMethod='GET')
        page_string = api_lambda.list(event, None, provider.service)
        self.assertIsNotNone(page_string)

        # Delete id
        provider_dict = json.loads(create_response['body'])
        deleted_response = self.delete_provider(provider_dict['id'])
        self.assertIsNotNone(deleted_response['body'])
        self.assertEqual(deleted_response['statusCode'], 200)

provider_test_case = LambdaProviderTestCase()