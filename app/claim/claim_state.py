import enum
from marshmallow import fields, post_load
from marshmallow.validate import OneOf
from sqlalchemy import types, ForeignKey, Column
from app.base.model import DBModel
from app.base import dao_postgres as dao
from app.base import schema
from app.base import service
from app import session


class State(enum.Enum):

    CREATED = 'Created'
    SUBMITTED = 'Submitted'
    DENIED = 'Denied'
    APPEALED = 'Appealed'
    PAYED = 'Payed'
    REQUESTED_MORE_INFORMATION = 'Requested more information'

    @staticmethod
    def list():
        return list(map(lambda state: state.value, State))


class ClaimState(DBModel):
    __tablename__ = 'claim_state'
    __table_args__ = {"schema": 'gentem'}

    state = Column(types.String(255))
    claim_id = Column(types.String(36), ForeignKey('gentem.claim.id'))


class ClaimStateSchema(schema.DBSchema):
    state = fields.Str(attribute='state', required=True, allow_none=False, validate=OneOf(State.list()))
    claimId = fields.Str(attribute='claim_id', required=False, allow_none=True)
    @post_load
    def make_object(self, data, **kargs):
        return ClaimState(**data)


schema = ClaimStateSchema()

dao = dao.PostgresDAO(schema, ClaimState, session)

service = service.EntityService(dao=dao, schema=schema)