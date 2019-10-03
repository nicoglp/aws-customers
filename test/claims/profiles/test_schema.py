import json

from marshmallow import ValidationError

from app.profile.profile import schema, Profile
from test.claims.profiles import ProfileTestCase


class ProfileSchemaTestCase(ProfileTestCase):

    def setUp(self):
        super(ProfileSchemaTestCase, self).setUp()

    def test_dump(self):

        profile = self._create_profile()
        try:
            profile_dict = schema.dump(profile)
            self.assertIsInstance(profile_dict, dict)
            self.assertIsNotNone(profile_dict['id'])
        except ValidationError as e:
            self.fail(e.messages)

    def test_load(self):

        profile_data = json.loads(self._create_profile_json())
        try:
            profile = schema.load(profile_data)
            self.assertIsInstance(profile, Profile)
            self.assertIsNotNone(profile.id)
        except ValidationError as e:
            self.fail(e.messages)
