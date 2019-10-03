import datetime
import enum
from marshmallow import fields, post_load
from marshmallow.validate import OneOf
from sqlalchemy import types, ForeignKey, Column
from sqlalchemy.orm import relationship
from app.base.model import DBModel
from app.base import dao_postgres as dao
from app.base import schema
from app.base import service
from .claim_state import ClaimState, ClaimStateSchema
from app.service_line.service_line import ServiceLine, ServiceLineSchema
from app.profile.profile import ProfileSchema
from app.provider.provider import ProviderSchema
from app import session


class PatientCondition(enum.Enum):

    EMPLOYMENT = 'Employment'
    AUTO_ACCIDENT = 'Auto Accident'
    OTHER_ACCIDENT = 'Other Accident'

    @staticmethod
    def list():
        return list(map(lambda patient_condition: patient_condition.value, PatientCondition))


class InsuranceType(enum.Enum):

    MEDICARE = 'MEDICARE'
    MEDICAID = 'MEDICAID'
    TRICARE = 'TRICARE'
    CHAMPVA = 'CHAMPVA'
    GROUP_HEALTH_PLAN = 'GROUP_HEALTH_PLAN'
    FECA_BLK_LUNG = 'FECA_BLK_LUNG'
    OTHER = 'OTHER'

    @staticmethod
    def list():
        return list(map(lambda insurance_type: insurance_type.value, InsuranceType))


class PatientRelation(enum.Enum):

    SELF = 'SELF'
    SPOUSE = 'SPOUSE'
    CHILD = 'CHILD'
    OTHER = 'OTHER'

    @staticmethod
    def list():
        return list(map(lambda patient_condition: patient_condition.value, PatientRelation))

class Claim(DBModel):
    __tablename__ = 'claim'
    __table_args__ = {"schema": 'gentem'}

    updated_at = Column(types.DateTime, default=datetime.datetime.utcnow())
    insurance_name = Column(types.String(255))
    patient_account_number = Column(types.String(255))
    total_charge = Column(types.Float)
    amount_paid = Column(types.Float)
    insured_id = Column(types.String(36), ForeignKey('gentem.profile.id'))
    patient_id = Column(types.String(36), ForeignKey('gentem.profile.id'))
    referring_provider_id = Column(types.String(36), ForeignKey('gentem.provider.id'))
    billing_provider_id = Column(types.String(36), ForeignKey('gentem.provider.id'))
    billing_provider_tax_id = Column(types.String(255))
    rendering_provider_id = Column(types.String(36), ForeignKey('gentem.provider.id'))
    insured_policy_group = Column(types.String(255))
    insurance_plan_name = Column(types.String(255))
    prior_authorization_number = Column(types.String(255))
    physician_supplier_signature = Column(types.String(255))
    physician_supplier_signature_date = Column(types.Date)
    illness_date = Column(types.Date)
    similar_symptom_date = Column(types.Date)
    unable_to_work_from = Column(types.Date)
    unable_to_work_to = Column(types.Date)
    hospital_admit_date = Column(types.Date)
    hospital_discharge_date = Column(types.Date)
    additional_claim_information = Column(types.String(255))
    insurance_type = Column(types.String(255))
    patient_condition = Column(types.String(255))
    patient_signature = Column(types.String(255))
    insured_signature = Column(types.String(255))
    patient_signature_date = Column(types.Date, default=datetime.datetime.utcnow())
    patient_relation = Column(types.String(255))
    other_insured_name = Column(types.String(255))
    other_insured_policy_group = Column(types.String(255))
    other_insured_company_name = Column(types.String(255))

    insured = relationship('Profile', foreign_keys=[insured_id], cascade="expunge", uselist=False, lazy='joined')
    patient = relationship('Profile', foreign_keys=[patient_id], cascade="expunge", uselist=False, lazy='joined')
    referring_provider = relationship('Provider', foreign_keys=[referring_provider_id], uselist=False, lazy='joined', cascade="expunge")
    billing_provider = relationship('Provider', foreign_keys=[billing_provider_id], uselist=False, lazy='joined', cascade="expunge")
    rendering_provider = relationship('Provider', foreign_keys=[rendering_provider_id], uselist=False, lazy='joined', cascade="expunge")
    service_lines = relationship(ServiceLine, uselist=True, lazy='subquery', primaryjoin="Claim.id == foreign(ServiceLine.claim_id)", cascade="all,delete")
    claim_state = relationship(ClaimState, uselist=False, lazy='subquery', order_by="desc(ClaimState.created_at)",
                                 primaryjoin="Claim.id == foreign(ClaimState.claim_id)", cascade="all,delete")


class ClaimSchema(schema.DBSchema):
    insuranceName = fields.Str(attribute="insurance_name", required=True, allow_none=False)
    patientAccountNumber = fields.Str(attribute="patient_account_number", required=True, allow_none=False)
    totalCharge = fields.Float(attribute="total_charge", required=True, allow_none=False)
    amountPaid = fields.Float(attribute="amount_paid", required=False, allow_none=True)
    insuredId = fields.Str(attribute='insured_id', required=False, allow_none=True)
    patientId = fields.Str(attribute='patient_id', required=True, allow_none=False)
    referringProviderId = fields.Str(attribute='referring_provider_id', required=True, allow_none=False)
    billingProviderId = fields.Str(attribute='billing_provider_id', required=True, allow_none=False)
    billingProviderTaxId = fields.Str(attribute='billing_provider_tax_id', required=True, allow_none=False)
    renderingProviderId = fields.Str(attribute='rendering_provider_id', required=True, allow_none=False)
    insuredPolicyGroup = fields.Str(attribute='insured_policy_group', required=False, allow_none=True)
    insurancePlanName = fields.Str(attribute='insurance_plan_name', required=False, allow_none=True)
    priorAuthorizationNumber = fields.Str(attribute='prior_authorization_number', required=False, allow_none=True)
    physicianSupplierSignature = fields.Str(attribute='physician_supplier_signature', required=True, allow_none=False)
    physicianSupplierSignatureDate = fields.Str(attribute='physician_supplier_signature_date', required=True, allow_none=False)
    illnessDate = fields.Date(attribute="illness_date", required=False, allow_none=True)
    similarSymptomDate = fields.Date(attribute="similar_symptom_date", required=False, allow_none=True)
    unableToWorkFrom = fields.Date(attribute="unable_to_work_from", required=False, allow_none=True)
    unableToWorkTo = fields.Date(attribute="unable_to_work_to", required=False, allow_none=True)
    hospitalAdmitDate = fields.Date(attribute="hospital_admit_date", required=False, allow_none=True)
    hospitalDischargeDate = fields.Date(attribute="hospital_discharge_date", required=False, allow_none=True)
    additionalClaimInformation = fields.Str(attribute='additional_claim_information', required=False, allow_none=True)
    insuranceType = fields.Str(attribute='insurance_type', required=False, allow_none=True, validate=OneOf(InsuranceType.list()))
    patientSignature = fields.Str(attribute='patient_signature', required=False, allow_none=True, default='SOF')
    insuredSignature = fields.Str(attribute='insured_signature', required=False, allow_none=True, default='SOF')
    patientCondition = fields.Str(attribute='patient_condition', required=False, allow_none=True, validate=OneOf(PatientCondition.list()))
    patientSignatureDate = fields.Date(attribute='patient_signature_date', required=False, allow_none=True)
    patientRelation = fields.Str(attribute='patient_relation', required=True, allow_none=False, validate=OneOf(PatientRelation.list()))
    otherInsuredName = fields.Str(attribute='other_insured_name', required=False, allow_none=True)
    otherInsuredPolicyGroup = fields.Str(attribute='other_insured_policy_group', required=False, allow_none=True)
    otherInsuredCompanyName = fields.Str(attribute='other_insured_company_name', required=False, allow_none=True)
    anotherHealthBenefitPlan = fields.Boolean(attribute='another_health_benefit_plan', required=False, allow_none=True)
    insured = fields.Nested(ProfileSchema)
    patient = fields.Nested(ProfileSchema)
    referringProvider = fields.Nested(ProviderSchema, attribute='referring_provider')
    billingProvider = fields.Nested(ProviderSchema, attribute='billing_provider')
    renderingProvider = fields.Nested(ProviderSchema, attribute='rendering_provider')
    serviceLines = fields.Nested(ServiceLineSchema, many=True, attribute='service_lines')
    claimState = fields.Nested(ClaimStateSchema, attribute='claim_state', required=False, allow_none=True)

    @post_load
    def make_object(self, data, **kargs):
        return Claim(**data)


schema = ClaimSchema()

dao = dao.PostgresDAO(schema, Claim, session)

service = service.EntityService(dao=dao, schema=schema)
