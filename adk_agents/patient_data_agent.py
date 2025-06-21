#   adk_agents/patient_data_agent.py
#   This module defines a PatientDataAgent class that:
#   Accepts structured patient data (from a Pydantic model).
#   Uploads patient imaging data to Google Cloud Storage (GCS).
#   Validates and standardizes the patient record.
#   Inserts the record into Google BigQuery.

from google.cloud import storage, bigquery
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from pydantic import BaseModel
import os

project_id=os.getenv("GOOGLE_CLOUD_PROJECT")
bq_dataset_var= os.getenv("BIGQUERY_DATASET")
gcs_bucket_var= os.getenv("GCS_BUCKET")

bigquery.Client(project=project_id)

class PatientRecord(BaseModel):
    patient_id: str
    patient_name: str
    age: int
    gender: str
    location: str
    country: str
    diagnosis: str
    genetic_variants: dict
    imaging_path: str  # GCS URI for DICOM

class PatientDataAgent:
    def __init__(self, gcs_bucket, bq_dataset, creds_path):
        self.gcs_bucket = gcs_bucket
        self.bq_dataset = bq_dataset
        creds_path = os.getenv("CREDS_PATH")# "keys -.json
        self.credentials = service_account.Credentials.from_service_account_file(creds_path)
        self.storage_client = storage.Client(credentials=self.credentials)
        self.bq_client = bigquery.Client(credentials=self.credentials)

    def ingest_data(self, record: PatientRecord):
        print(f"Ingesting patient data for {record.patient_id}")
        # Upload image if not already in GCS
        if not record.imaging_path.startswith("gs://"):
            blob = self.storage_client.bucket(self.gcs_bucket).blob(f"images/{record.patient_id}.dcm")
            print(blob)
            blob.upload_from_filename(record.imaging_path)
            record.imaging_path = f"gs://{self.gcs_bucket}/images/{record.patient_id}.dcm"

        return record

    def validate_and_standardize(self, record: PatientRecord):
        print(f"Validating record for {record.patient_id}")
        assert record.age > 0
        assert record.gender in ["male", "female", "other"]
        return record

    def save_to_bigquery(self, record: PatientRecord):
        print("Saving to BigQuery...")
        table_id = f"{self.bq_dataset}.patient_records"
        rows = [{
            "patient_id": record.patient_id,
            "patient_name":record.patient_name,
            "age": record.age,
            "gender": record.gender,
            "location": record.location,
            "country": record.country,
            "diagnosis": record.diagnosis,
            "genetic_variants": str(record.genetic_variants),
            "imaging_path": record.imaging_path,
        }]
        errors = self.bq_client.insert_rows_json(table_id, rows)
        if errors:
            raise RuntimeError(errors)

# Example usage
if __name__ == "__main__":
    agent = PatientDataAgent(
        bq_dataset= os.getenv("BIGQUERY_DATASET"),
        gcs_bucket= os.getenv("GCS_BUCKET"),
        creds_path = os.getenv("CREDS_PATH")
    )
    example = PatientRecord(
        patient_id="P006",
        patient_name="Dobby Jonthan",
        age=65,
        gender="female",
        location="Texas",
        country="USA",
        diagnosis="lung cancer",
        genetic_variants={"KRAS": "positive"},
        imaging_path="gs://patient_cancer_data/lung_cancer_KRAS.jpeg"
    )
    std_record = agent.validate_and_standardize(agent.ingest_data(example))
    agent.save_to_bigquery(std_record)

