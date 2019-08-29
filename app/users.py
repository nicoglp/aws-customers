from marshmallow import fields, post_load

from . import config
from .base import dao_dynamodb as dao
from .base import model
from .base import schema
from .base import service


class User(model.Model):

    def __init__(self, first_name=None, last_name=None, email=None, date_of_birth=None, address=None, **kwargs):
        super(User, self).__init__(**kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.address = address


class UserSchema(schema.ModelSchema):
    firstName = fields.Str(attribute="first_name")
    lastName = fields.Str(attribute="last_name")
    email = fields.Email(attribute="email")
    dob = fields.Date(attribute="date_of_birth")
    address = fields.Str(attribute="address")

    @post_load
    def make_object(self, data, **kargs):
        return User(**data)


schema = UserSchema()

dao = dao.DynamoDAO(config.USER_TABLENAME, schema, 'email')

service = service.EntityService(dao=dao, schema=schema)
