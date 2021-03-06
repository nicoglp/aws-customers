import json

from app.profile import profile_lambda
from test.claims.profiles import ProfileTestCase
from app.profile import profile



class LambdaProfileTestCase(ProfileTestCase):

    def create_profile(self, email="pia.farinella@gmail.com", last_name= "Doe", gender=profile.Gender.MALE.value, first_name="Jon",
                             address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", middle_initial="P", dob=None):
        profile_json = self._create_profile_json(email, last_name, gender, first_name, address, member_id, phone, middle_initial, dob)
        event = dict(body=profile_json, httpMethod='POST')
        response = profile_lambda.post_profile(event, None)
        return response

    def delete_profile(self, id):
        event = dict(httpMethod='DELETE', pathParameters={'id': id})
        deleted_response = profile_lambda.delete_profile(event, None)
        return deleted_response

    def test_post(self):
        response = self.create_profile()
        self.assertIsNotNone(response['body'])
        self.assertEqual(response['statusCode'], 201)

        profile_dict = json.loads(response['body'])
        deleted_response= self.delete_profile(profile_dict['id'])
        self.assertIsNotNone(deleted_response['body'])
        self.assertEqual(deleted_response['statusCode'], 200)

    def test_get(self):
        create_response = self.create_profile()

        # Get id
        profile_dict = json.loads(create_response['body'])
        event = dict(httpMethod='GET', pathParameters={'id': profile_dict['id']})
        retrieved_user = profile_lambda.get_profile(event, None)
        self.assertIsNotNone(retrieved_user)

        # Delete id
        deleted_response = self.delete_profile(profile_dict['id'])
        self.assertIsNotNone(deleted_response['body'])
        self.assertEqual(deleted_response['statusCode'], 200)

    def test_list(self):
        create_response = self.create_profile()

        # List
        event = dict(httpMethod='GET')
        page_string = profile_lambda.list_profile(event, None)
        self.assertIsNotNone(page_string)

        # Delete id
        profile_dict = json.loads(create_response['body'])
        deleted_response = self.delete_profile(profile_dict['id'])
        self.assertIsNotNone(deleted_response['body'])
        self.assertEqual(deleted_response['statusCode'], 200)

profile_test_case = LambdaProfileTestCase()