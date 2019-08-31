from marshmallow import ValidationError

from app.users import dao, schema, User
from test import UserTestCase


class UserDAOTestCase(UserTestCase):

    def setUp(self):
        super(UserDAOTestCase, self).setUp()

    def test_crud(self):

        user = self._crete_user()
        try:
            persisted_user = dao.save(user)

            self.assertIsInstance(persisted_user, User)
            self.assertIsNotNone(persisted_user.id)
            self.assertIsNotNone(persisted_user.created_at)
            self.assertIsNotNone(persisted_user.updated_at)

            new_user = dao.retrieve(persisted_user.email)
            self.assertIsNotNone(new_user)

            new_user.first_name = "New First Name"
            new_user.last_name = "New Last Name"
            updated_user = dao.update(new_user)
            self.assertNotEqual(updated_user.first_name, persisted_user.first_name)

            deleted = dao.delete(user.email)
            self.assertTrue(deleted)

        except ValidationError:
            self.fail()

    def test_find_all(self):
        user = self._crete_user()
        try:
            dao.save(user)

            page = dao.find_all()
            self.assertIsNotNone(page)
            self.assertTrue(len(page.items) > 0)

            dao.delete(user.email)

        except ValidationError:
            self.fail()

    def test_update_dynamo_structure(self):

        user = User(first_name='Nicolas', last_name='Garcia', email='nicoglp@gmail.com')
        user_schema = schema
        document_dict = user_schema.dump(user)

        params = dict(
            ExpressionAttributeNames={},
            ExpressionAttributeValues={},
            UpdateExpression="SET "
        )
        for attr, value in document_dict.items():
            if attr not in ('email'):
                name_key = "#{}".format(attr)
                value_key = ":{}".format(attr)
                params['ExpressionAttributeNames'][name_key] = attr
                params['ExpressionAttributeValues'][value_key] = value
                params['UpdateExpression'] += "{} = {} ".format(name_key, value_key)

        # print(json.dumps(params, indent=2))
