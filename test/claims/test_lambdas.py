from datetime import date
import json
from app.claim import claim_lambda
from test.claims import ClaimTestCase
from app.claim.claims import service
from app.provider.provider import ProviderType
from app.profile.profile import Gender
from test.claims.providers.test_lambdas import provider_test_case
from test.claims.profiles.test_lambdas import profile_test_case


class claimclaimTestCase(ClaimTestCase):

    def _retrieve_response_id(self, response):
        dict = json.loads(response['body'])
        return dict['id']

    def _insert_claim(self):
        billing_response = provider_test_case.create_provider(name="Gentem", address="303 YOUNGLOVE AVE, san francisco 94103, CA",
                                                             npi="1568412345", type=ProviderType.BILLING_PROVIDER.value, phone="424-248-7725")
        billing_provider_id = self._retrieve_response_id(billing_response)

        referring_response = provider_test_case.create_provider(name="John Lin", npi="1568412346", type=ProviderType.REFERRING_PROVIDER.value)
        referring_provider_id = self._retrieve_response_id(referring_response)

        rendering_response = provider_test_case.create_provider(name="Saint Francis Memorial Hospital", address="2900 Hyde St Lower Nob Hill, san francisco 94103, CA", npi="1316061997", type=ProviderType.RENDERING_PROVIDER.value)
        rendering_provider_id = self._retrieve_response_id(rendering_response)

        insured_response = profile_test_case.create_profile(email="jon.doe@gmail.com", last_name="Doe", gender=Gender.MALE.value, first_name="Jon",
                                                    address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567",middle_initial="P", dob=date(1981, 6, 24))
        insured_id = self._retrieve_response_id(insured_response)
        patient_response = profile_test_case.create_profile(email="susan.doe@gmail.com", last_name="Doe", gender=Gender.FEMALE.value, first_name="Susan",
                                                    address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", dob=date(2015, 10, 19))
        patient_id = self._retrieve_response_id(patient_response)

        claim_json = self._create_claim_json(patient_id, referring_provider_id, billing_provider_id, rendering_provider_id, insured_id)
        event = dict(body=claim_json, httpMethod='POST')
        response = claim_lambda.post_claim(event, None)
        return response, patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id

    def _delete_claim(self, claim_id, patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id):
        event = dict(httpMethod='DELETE', pathParameters={'id': claim_id})
        deleted_response = claim_lambda.delete_claim(event, None)
        self.assertIsNotNone(deleted_response['body'])
        self.assertEqual(deleted_response['statusCode'], 200)

        profile_test_case.delete_profile(patient_id)
        profile_test_case.delete_profile(insured_id)
        provider_test_case.delete_provider(billing_provider_id)
        provider_test_case.delete_provider(referring_provider_id)
        provider_test_case.delete_provider(rendering_provider_id)

    def test_post(self):
        response, patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id = self._insert_claim()

        self.assertIsNotNone(response['body'])
        self.assertEqual(response['statusCode'], 201)
        claim_dict = json.loads(response['body'])
        self._delete_claim(claim_dict['id'], patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id)

    def test_get(self):
        create_response, patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id = self._insert_claim()

        # Get id
        claim_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': claim_dict['id']})
        retrieved_claim = claim_lambda.get_claim(event, None)
        self.assertIsNotNone(retrieved_claim)

        self._delete_claim(claim_dict['id'], patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id)

    def test_list(self):
        response, patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id = self._insert_claim()

        # List
        event = dict(httpMethod='GET')
        page_string = claim_lambda.list_claim(event, None)
        self.assertIsNotNone(page_string)

        claim_dict = json.loads(response['body'])
        self._delete_claim(claim_dict['id'], patient_id, billing_provider_id, referring_provider_id, rendering_provider_id, insured_id)