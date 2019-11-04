from datetime import date
import json
from marshmallow import ValidationError
from app.claim.claims import schema, Claim
from test.claims import ClaimTestCase
from app.provider.provider import ProviderType
from app.profile.profile import Gender
from test.claims.providers import provider_test_case
from test.claims.profiles import profile_test_case


class ClaimSchemaTestCase(ClaimTestCase):

    def setUp(self):
        super(ClaimSchemaTestCase, self).setUp()

    def test_dump(self):
        billing_provider = provider_test_case._create_provider(name="Gentem", address="303 YOUNGLOVE AVE, san francisco 94103, CA",
                                                             npi="1568412345", type=ProviderType.BILLING_PROVIDER.value, phone="424-248-7725")
        referring_provider = provider_test_case._create_provider(name="John Lin", npi="1568412346", type=ProviderType.REFERRING_PROVIDER.value)
        rendering_provider = provider_test_case._create_provider(name="Saint Francis Memorial Hospital", address="2900 Hyde St Lower Nob Hill, san francisco 94103, CA",
                                                             npi="1316061997", type=ProviderType.RENDERING_PROVIDER.value)

        insured = profile_test_case._create_profile(email="jon.doe@gmail.com", last_name= "Doe", gender=Gender.MALE.value, first_name="Jon",
                                                    address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", middle_initial="P", dob=date(1981, 6, 24))
        patient = profile_test_case._create_profile(email="susan.doe@gmail.com", last_name="Doe", gender=Gender.FEMALE.value, first_name="Susan",
                                                    address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", dob=date(2015, 10, 19))

        claim = self._create_claim(patient.id, rendering_provider.id, referring_provider.id, billing_provider.id, insured.id)
        try:
            claim_dict = schema.dump(claim)
            self.assertIsInstance(claim_dict, dict)
            self.assertIsNotNone(claim_dict['id'])
        except ValidationError as e:
            self.fail(e.messages)

    def test_load(self):
        billing_prov = provider_test_case._create_provider_json(name="Gentem", address="303 YOUNGLOVE AVE, san francisco 94103, CA",
                                                             npi="1568412345", type=ProviderType.BILLING_PROVIDER.value, phone="424-248-7725")
        ref_prov = provider_test_case._create_provider_json(name="John Lin", npi="1568412346", type=ProviderType.REFERRING_PROVIDER.value)
        ren_prov = provider_test_case._create_provider_json(name="Saint Francis Memorial Hospital", address="2900 Hyde St Lower Nob Hill, san francisco 94103, CA",
                                                             npi="1316061997", type=ProviderType.RENDERING_PROVIDER.value)
        insured = profile_test_case._create_profile_json(email="jon.doe@gmail.com", last_name= "Doe", gender=Gender.MALE.value, first_name="Jon",
                                                    address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", middle_initial="P", dob=date(1981, 6, 24))
        patient = profile_test_case._create_profile_json(email="susan.doe@gmail.com", last_name="Doe", gender=Gender.FEMALE.value, first_name="Susan",
                                                    address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", dob=date(2015, 10, 19))
        claim_data = json.loads(self._create_claim_json(json.loads(patient)['id'], json.loads(billing_prov)['id'], json.loads(ref_prov)['id'], json.loads(ren_prov)['id'], json.loads(insured)['id']))
        try:
            claim = schema.load(claim_data)
            self.assertIsInstance(claim, Claim)
            self.assertIsNotNone(claim.id)
        except ValidationError as e:
            self.fail(e.messages)
