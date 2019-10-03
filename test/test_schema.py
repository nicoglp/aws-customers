import json

from marshmallow import ValidationError

from app.user.users import schema, User
from test import UserTestCase


class UserSchemaTestCase(UserTestCase):

    def setUp(self):
        super(UserSchemaTestCase, self).setUp()

    def test_dump(self):

        user = self._crete_user()
        try:
            user_dict = schema.dump(user)
            self.assertIsInstance(user_dict, dict)
            self.assertIsNotNone(user_dict['id'])
        except ValidationError as e:
            self.fail(e.messages)

    def test_load(self):

        user_data = json.loads(self._crete_user_json())
        try:
            user = schema.load(user_data)
            self.assertIsInstance(user, User)
            self.assertIsNotNone(user.id)
        except ValidationError as e:
            self.fail(e.messages)
