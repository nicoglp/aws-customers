create schema gentem;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create table gentem.profile (
id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
created_at timestamptz not null,
updated_at timestamptz null,
first_name varchar(255) NOT NULL,
last_name varchar(255) NOT NULL,
middle_initial varchar(255) NULL,
address varchar(255) NOT NULL,
phone varchar(255) NULL,
dob timestamp NOT NULL,
gender varchar(255) NOT NULL,
member_id varchar(255) NOT NULL,
email varchar(255) NOT NULL,
UNIQUE (email)
);

create table gentem.provider (
id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
created_at timestamptz not null,
updated_at timestamptz null,
name varchar(255) NOT NULL,
address varchar(255) NULL,
phone varchar(255) NULL,
npi varchar(255) NOT NULL,
type varchar(255) NOT NULL,
UNIQUE (npi)
);


create table gentem.claim (
id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
created_at timestamptz not null,
updated_at timestamptz null,
insurance_name varchar(255) NOT null,
patient_account_number varchar(255) NOT NULL,
total_charge float NOT NULL,
amount_paid float NULL,
insured_id uuid NULL,
patient_id uuid NOT NULL,
referring_provider_id uuid NOT NULL,
billing_provider_id uuid NOT NULL,
billing_provider_tax_id varchar(255) NOT NULL,
rendering_provider_id uuid NOT NULL,
insured_policy_group varchar(255) NULL,
insurance_plan_name varchar(255) NULL,
prior_authorization_number varchar(255) NULL,
physician_supplier_signature varchar(255) NULL,
physician_supplier_signature_date timestamp not null,
illness_date timestamp null,
similar_symptom_date timestamp null,
unable_to_work_from timestamp null,
unable_to_work_to timestamp null,
hospital_admit_date timestamp null,
hospital_discharge_date timestamp null,
additional_claim_information varchar(1024) NULL,
insurance_type varchar(255) NULL,
patient_condition varchar(255) NULL,
patient_signature varchar(255) NOT NULL,
insured_signature varchar(255) NOT NULL,
patient_signature_date timestamp NOT NULL,
patient_relation varchar(255) NOT NULL,
other_insured_name varchar(255) NULL,
other_insured_policy_group varchar(255) NULL,
other_insured_company_name varchar(255) NULL,
another_health_benefit_plan boolean null default false,
UNIQUE (patient_account_number),
FOREIGN KEY (insured_id) REFERENCES gentem.profile(id),
FOREIGN KEY (patient_id) REFERENCES gentem.profile(id),
FOREIGN KEY (referring_provider_id) REFERENCES gentem.provider(id),
FOREIGN KEY (billing_provider_id) REFERENCES gentem.provider(id),
FOREIGN KEY (rendering_provider_id) REFERENCES gentem.provider(id)
);


create table gentem.service_line (
id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
created_at timestamptz not null,
updated_at timestamptz null,
procedure_code integer NOT NULL,
charges float NOT NULL,
units integer NOT NULL,
modifiers varchar[] NULL,
diagnosis_codes varchar[] NOT NULL,
claim_id uuid NOT NULL,
service_date_from timestamp NOT NULL,
service_date_to timestamp null,
place_of_service varchar(255) NOT NULL,
emergency_indicator boolean default false,
id_qualifier varchar(255) NULL,
rendering_provider_id varchar(255) NULL,
EPSDT_family_plan varchar(255) NULL,
FOREIGN KEY (claim_id) REFERENCES gentem.claim(id)
);

create table gentem.claim_state (
id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
created_at timestamptz not null,
claim_id uuid NOT NULL,
state varchar(255) NOT NULL,
FOREIGN KEY (claim_id) REFERENCES gentem.claim(id)
);