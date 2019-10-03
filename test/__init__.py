import json
import unittest
import uuid
from datetime import datetime

from app.user import users


class UserTestCase(unittest.TestCase):

    def setUp(self):
        super(UserTestCase, self).setUp()

    def _crete_user_json(self):
        return json.dumps(dict(
            firstName="Jon",
            lastName="Doe",
            email="jon.doe@gmail.com",
            dob="1980-10-14",
            address="1 glove drive , san francisco 94103, CA",
            id = 'test-id',
            createdAt = '123456',
            updatedAt='123456'
        ))

    def _crete_user(self):
        timestamp = datetime.utcnow().timestamp()
        user = users.User(
            first_name="Jon",
            last_name="Doe",
            email="jon.doe@gmail.com",
            date_of_birth=datetime.fromisoformat('1980-10-14'),
            address="1 glove drive , san francisco 94103, CA",
            id = uuid.uuid1(),
            created_at = timestamp,
            updated_at = timestamp
        )

        return user
