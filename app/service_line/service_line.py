from datetime import datetime
from marshmallow import fields, post_load
from sqlalchemy import types, ForeignKey, Column
from app.base.model import DBModel
from app.base import dao_postgres as dao
from app.base import schema
from app.base import service
from app import session


class ServiceLine(DBModel):
    __tablename__ = 'service_line'
    __table_args__ = {"schema": 'gentem'}

    updated_at = Column(types.DateTime, default=datetime.utcnow())
    procedure_code = Column(types.Integer)
    charges = Column(types.Float)
    units = Column(types.Integer)
    modifiers = Column(types.ARRAY(types.String(255)))
    diagnosis_codes = Column(types.ARRAY(types.String(255)))
    claim_id = Column(types.String(36), ForeignKey('gentem.claim.id'))
    service_date_from = Column(types.Date)
    service_date_to = Column(types.Date)
    place_of_service = Column(types.String(255))
    emergency_indicator = Column(types.Boolean)
    id_qualifier = Column(types.String(255))
    rendering_provider_id = Column(types.String(255))
    epsdt_family_plan = Column(types.String(255))


class ServiceLineSchema(schema.DBSchema):
    procedureCode = fields.Int(attribute='procedure_code', required=True, allow_none=False)
    charges = fields.Float(required=True, allow_none=False)
    units = fields.Int(required=True, allow_none=False)
    modifiers = fields.List(fields.Str(), required=False, allow_none=True)
    diagnosisCodes = fields.List(fields.Str(), attribute='diagnosis_codes', required=True, allow_none=False)
    claimId = fields.Str(attribute='claim_id', required=False, allow_none=True)
    serviceDateFrom = fields.Date(attribute='service_date_from', required=True, allow_none=False)
    serviceDateTo = fields.Date(attribute='service_date_to', required=False, allow_none=True)
    placeOfService = fields.Str(attribute='place_of_service', required=True, allow_none=False)
    emergencyIndicator = fields.Boolean(attribute='emergency_indicator', required=False, allow_none=True)
    idQualifier = fields.Str(attribute='id_qualifier', required=False, allow_none=True)
    renderingProviderId = fields.Str(attribute='rendering_provider_id', required=False, allow_none=True)
    EPSDTFamilyPlan = fields.Str(attribute='epsdt_family_plan', required=False, allow_none=True)

    @post_load
    def make_object(self, data, **kargs):
        return ServiceLine(**data)


schema = ServiceLineSchema()

dao = dao.PostgresDAO(schema, ServiceLine, session)

service = service.EntityService(dao=dao, schema=schema)
