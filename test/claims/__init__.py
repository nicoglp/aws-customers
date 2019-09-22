import json
import unittest
import uuid
from datetime import datetime
from app import claim_state
from app import service_line
from app import claims


class ClaimTestCase(unittest.TestCase):

    def setUp(self):
        super(ClaimTestCase, self).setUp()

    def _create_claim_json(self, patient_id, referringProvider_id,  billingProvider_id, renderingProvider_id, insured_id=None):
        datetimenow = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(dict(
            updatedAt=datetimenow,
            id=str(uuid.uuid1()),
            createdAt=datetimenow,
            patientAccountNumber= "123456",
            totalCharge= 200.50,
            amountPaid= 0,
            insuranceName= "blue_shield_ca",
            insuredId= insured_id,
            patientId= patient_id,
            referringProviderId= referringProvider_id,
            billingProviderId= billingProvider_id,
            billingProviderTaxId= "HE567W65489A",
            renderingProviderId= renderingProvider_id,
            insuredPolicyGroup= "Z9364859",
            insurancePlanName= "IFP ON EXCHANGE",
            priorAuthorizationNumber= "63B4295825",
            physicianSupplierSignature= "Signature on File",
            physicianSupplierSignatureDate= "2019-09-29",
            illnessDate= "2019-09-26",
            similarSymptomDate= "2019-08-20",
            unableToWorkFrom= "2019-09-26",
            unableToWorkTo= "2019-10-26",
            hospitalAdmitDate= "2019-09-26",
            hospitalDischargeDate= "2019-10-15",
            additionalClaimInformation= "",
            insuranceType= claims.InsuranceType.OTHER.value,
            patientCondition= claims.PatientCondition.OTHER_ACCIDENT.value,
            patientSignatureDate= "2019-09-29",
            patientSignature= "Signature on File",
            insuredSignature= "Signature on File",
            patientRelation= claims.PatientRelation.CHILD.value,
            otherInsuredName= "Mcintire, Ashley L",
            otherInsuredPolicyGroup= "115",
            otherInsuredCompanyName= "UHC",
            anotherHealthBenefitPlan= "true",
            claimState= dict(state = "Created"),
            serviceLines= [dict(
                updatedAt=datetimenow,
                id=str(uuid.uuid1()),
                createdAt=datetimenow,
                procedureCode= 87653,
                charges= 100.40,
                units= 1,
                modifiers= [],
                diagnosisCodes= ["N949"],
                serviceDateFrom= "2019-09-29",
                serviceDateTo= "2019-09-29",
                placeOfService= "21",
                emergencyIndicator= "false"
                ),
                dict(
                    updatedAt=datetimenow,
                    id=str(uuid.uuid1()),
                    createdAt=datetimenow,
                    procedureCode=87798,
                    charges=20.02,
                    units=5,
                    modifiers=["59"],
                    diagnosisCodes=["Z7251"],
                    serviceDateFrom="2019-09-29",
                    serviceDateTo="2019-09-29",
                    placeOfService="21",
                    emergencyIndicator="false"
                )
            ]
        ))

    def _create_claim(self, patient_id, referringProvider_id,  billingProvider_id, renderingProvider_id, insured_id=None):
        datetimenow = datetime.utcnow()
        date = datetime.now()
        claim = claims.Claim(
            updated_at=datetimenow,
            id=str(uuid.uuid1()),
            created_at=datetimenow,
            patient_account_number="123456",
            total_charge=200.50,
            amount_paid=0,
            insurance_name="blue_shield_ca",
            insured_id=insured_id,
            patient_id=patient_id,
            referring_provider_id=referringProvider_id,
            billing_provider_id=billingProvider_id,
            billing_provider_tax_id="HE567W65489A",
            rendering_provider_id=renderingProvider_id,
            insured_policy_group="Z9364859",
            insurance_plan_name="IFP ON EXCHANGE",
            prior_authorization_number="63B4295825",
            physician_supplier_signature="Signature on File",
            physician_supplier_signature_date=date,
            illness_date=date,
            similar_symptom_date=date,
            unable_to_work_from=date,
            unable_to_work_to=date,
            hospital_admit_date=date,
            hospital_discharge_date=date,
            additional_claim_information="",
            insurance_type= claims.InsuranceType.OTHER.value,
            patient_condition=claims.PatientCondition.OTHER_ACCIDENT.value,
            patient_signature_date=date,
            patient_signature="Signature on File",
            insured_signature="Signature on File",
            patient_relation=claims.PatientRelation.CHILD.value,
            other_insured_name="Mcintire, Ashley L",
            other_insured_policy_group="115",
            other_insured_company_name="UHC",
            another_health_benefit_plan="true",
            claim_state=claim_state.ClaimState(state="Created"),
            service_lines=[service_line.ServiceLine(
                updated_at=datetimenow,
                id=str(uuid.uuid1()),
                created_at=datetimenow,
                procedure_code=87653,
                charges=100.40,
                units=1,
                modifiers=[],
                diagnosis_codes=["N949"],
                service_date_from=date,
                service_date_to=date,
                place_of_service="21",
                emergency_indicator="false"
            ),
                service_line.ServiceLine(
                    updated_at=datetimenow,
                    id=str(uuid.uuid1()),
                    created_at=datetimenow,
                    procedure_code=87798,
                    charges=20.02,
                    units=5,
                    modifiers=[59],
                    diagnosis_codes=["Z7251"],
                    service_date_from=date,
                    service_date_to=date,
                    place_of_service="21",
                    emergency_indicator="false"
                )
            ]
        )

        return claim
