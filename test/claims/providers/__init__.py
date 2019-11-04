import json
import unittest
import uuid
from datetime import datetime

from app.provider import provider


class ProviderTestCase(unittest.TestCase):

    def setUp(self):
        super(ProviderTestCase, self).setUp()

    def _create_provider_json(self, name="John Lin", address=None, npi="1568412345", type=provider.ProviderType.REFERRING_PROVIDER.value, phone=None):
        datetimenow = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(dict(
            updatedAt= datetimenow,
            id= str(uuid.uuid1()),
            createdAt= datetimenow,
            name= name,
            address= address,
            npi= npi,
            type= type,
            phone= phone
        ))

    def _create_provider(self, name="John Lin", address=None, npi="1568412345", type=provider.ProviderType.REFERRING_PROVIDER.value, phone=None):
        datetimenow = datetime.utcnow()
        provider_entity = provider.Provider(
            id=uuid.uuid1(),
            procedure_code=123,
            updated_at=datetimenow,
            created_at=datetimenow,
            name=name,
            address=address,
            npi=npi,
            type=type,
            phone=phone
        )

        return provider_entity

provider_test_case = ProviderTestCase()