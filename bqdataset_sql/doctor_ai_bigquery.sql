CREATE TABLE `<PROJECT_ID>.<BIGQUERY_DATASET_NAME>.patient_records` (
  patient_id STRING,
  patient_name STRING,
  age INT64,
  gender STRING,
  location STRING,
  country STRING,
  diagnosis STRING,
  genetic_variants STRING,
  imaging_path STRING
);
CREATE TABLE `<PROJECT_ID>.<BIGQUERY_DATASET_NAME>.diagnosis_results` (
  patient_id STRING,
  patient_name STRING,
  diagnosis STRING,
  stage STRING,
  confidence FLOAT64,
  rationale STRING
);


CREATE TABLE `<PROJECT_ID>.<BIGQUERY_DATASET_NAME>.nccn_guidelines` (
  patient_id STRING,
  diagnosis STRING,
  stage STRING,
  nccn_guideline_text STRING
);

CREATE TABLE `<PROJECT_ID>.<BIGQUERY_DATASET_NAME>.explanations` (
  patient_id STRING NOT NULL,
  diagnosis STRING NOT NULL,
  stage STRING,
  genetic_variants STRING,
  treatment_plan STRING,
  doctor_notes STRING,
  imaging_path STRING,
  last_updated TIMESTAMP
);



