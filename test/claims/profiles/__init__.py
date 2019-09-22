import json
import unittest
import uuid
from datetime import datetime, date

from app import profile


class ProfileTestCase(unittest.TestCase):

    def setUp(self):
        super(ProfileTestCase, self).setUp()

    def _create_profile_json(self, email="jon.doe@gmail.com", last_name= "Doe", gender=profile.Gender.MALE.value, first_name="Jon",
                             address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", middle_initial="P", dob=None):
        datetimenow = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if not dob:
            dob = date(1981, 6, 24)
        dob = dob.strftime("%Y-%m-%d")
        return json.dumps(dict(
            updatedAt= datetimenow,
            id= str(uuid.uuid1()),
            createdAt= datetimenow,
            lastName=last_name,
            gender=gender,
            firstName=first_name,
            address=address,
            memberId=member_id,
            dob=dob,
            phone=phone,
            email=email,
            middleInitial=middle_initial
        ))

    def _create_profile(self, email="pia.farinella@gmail.com", last_name= "Doe", gender=profile.Gender.MALE.value, first_name="Jon",
                             address="1 glove drive , san francisco 94103, CA", member_id="ABC100286987", phone="415 1234567", middle_initial="P", dob=None):
        datetimenow = datetime.utcnow()
        if not dob:
            dob = date(1981, 6, 24)
        profile_entity = profile.Profile(
            id=uuid.uuid1(),
            procedure_code=123,
            updated_at=datetimenow,
            created_at=datetimenow,
            last_name=last_name,
            gender= gender,
            first_name= first_name,
            address= address,
            member_id= member_id,
            dob= dob,
            phone= phone,
            email= email,
            middle_initial= middle_initial
        )
        return profile_entity

profile_test_case = ProfileTestCase()