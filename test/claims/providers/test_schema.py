import json

from marshmallow import ValidationError

from app.provider import schema, Provider
from test.claims.providers import ProviderTestCase


class ServiceLineSchemaTestCase(ProviderTestCase):

    def setUp(self):
        super(ServiceLineSchemaTestCase, self).setUp()

    def test_dump(self):

        provider = self._create_provider("npi1")
        try:
            provider_dict = schema.dump(provider)
            self.assertIsInstance(provider_dict, dict)
            self.assertIsNotNone(provider_dict['id'])
        except ValidationError as e:
            self.fail(e.messages)

    def test_load(self):

        provider_data = json.loads(self._create_provider_json())
        try:
            provider = schema.load(provider_data)
            self.assertIsInstance(provider, Provider)
            self.assertIsNotNone(provider.id)
        except ValidationError as e:
            self.fail(e.messages)
