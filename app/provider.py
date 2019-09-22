from datetime import datetime
import enum
from marshmallow import fields, post_load
from marshmallow.validate import OneOf
from sqlalchemy import types, Column
from .base.model import DBModel
from .base import dao_postgres as dao
from .base import schema
from .base import service
from . import session


class ProviderType(enum.Enum):

    BILLING_PROVIDER = 'billing_provider'
    RENDERING_PROVIDER = 'rendering_provider'
    REFERRING_PROVIDER = 'referring_provider'

    @staticmethod
    def list():
        return list(map(lambda provider_type: provider_type.value, ProviderType))


class Provider(DBModel):
    __tablename__ = 'provider'
    __table_args__ = {"schema": 'gentem'}

    updated_at = Column(types.DateTime, default=datetime.utcnow())
    name = Column(types.String(255))
    address = Column(types.String(255))
    phone = Column(types.String(255))
    npi = Column(types.Date)
    type = Column(types.String(255))


class ProviderSchema(schema.DBSchema):
    name = fields.Str(required=True, allow_none=False)
    address = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    npi = fields.Str(required=True, allow_none=False)
    type = fields.Str(validate=OneOf(ProviderType.list()), required=True, allow_none=False)

    @post_load
    def make_object(self, data, **kargs):
        return Provider(**data)


schema = ProviderSchema()

dao = dao.PostgresDAO(schema, Provider, session)

service = service.EntityService(dao=dao, schema=schema)
