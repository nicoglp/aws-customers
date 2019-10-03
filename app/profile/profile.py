from datetime import datetime
import enum
from marshmallow import fields, post_load
from marshmallow.validate import OneOf
from sqlalchemy import types, Column
from app.base.model import DBModel
from app.base import dao_postgres as dao
from app.base import schema
from app.base import service
from app import session


class Gender(enum.Enum):

    FEMALE = 'Female'
    MALE = 'Male'

    @staticmethod
    def list():
        return list(map(lambda gender: gender.value, Gender))

class Profile(DBModel):
    __tablename__ = 'profile'
    __table_args__ = {"schema": 'gentem'}

    updated_at = Column(types.DateTime, default=datetime.utcnow())
    first_name = Column(types.String(255))
    last_name = Column(types.String(255))
    middle_initial = Column(types.String(255))
    address = Column(types.String(255))
    phone = Column(types.String(255))
    dob = Column(types.Date)
    gender = Column(types.String(255))
    member_id = Column(types.String(255))
    email = Column(types.String(255))


class ProfileSchema(schema.DBSchema):
    firstName = fields.Str(attribute='first_name', required=True, allow_none=False)
    lastName = fields.Str(attribute='last_name', required=True, allow_none=False)
    middleInitial = fields.Str(attribute='middle_initial')
    address = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=True, allow_none=False)
    dob = fields.Date(required=True, allow_none=False)
    gender = fields.Str(required=True, allow_none=False, validate=OneOf(Gender.list()))
    memberId = fields.Str(attribute='member_id', required=True, allow_none=False)
    email = fields.Str(required=True, allow_none=False)


    @post_load
    def make_object(self, data, **kargs):
        return Profile(**data)


schema = ProfileSchema()
profile_dao = dao.PostgresDAO(schema, Profile, session)
service = service.EntityService(dao=profile_dao, schema=schema)