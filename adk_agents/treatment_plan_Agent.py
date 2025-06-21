#   adk_agents/treatment_plan_Agent.py
#   TreatmentPlannerAgent recommends personalized cancer treatment 
#   options for a patient based on:Clinical stage and cancer type

import os
from google.cloud import bigquery

# Get the project ID and table name from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
table_patient = os.getenv("GOOGLE_BIGQUERY_TABLE_N")

# Validate environment variables
if not project_id:
    raise EnvironmentError("Environment variable 'GOOGLE_CLOUD_PROJECT' is not set.")
if not table_patient:
    raise EnvironmentError("Environment variable 'GOOGLE_BIGQUERY_TABLE_N' is not set.")

def get_nccn_guidelines_data(patient_id: str) -> dict:
    """
    Retrieves NCCN guideline text for a specific cancer patient based on diagnosis and stage.
    This function queries Google BigQuery to fetch the NCCN guideline recommendation text
    associated with the cancer type and clinical stage of a patient. It first looks up the
    diagnosis and stage by the provided `patient_id` from the relevant dataset, and then
    returns the matched guideline text from the `nccn_guidelines` table
    Note
    ----
    - NCCN guidelines are clinical best practices from https://www.nccn.org/guidelines/category_1
    - Make sure the BigQuery table contains `nccn_guideline_text` and `stage` columns.
    """

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Parameterized SQL query; f-string used to inject table name safely
    query = f"""
        SELECT nccn_guideline_text, stage
        FROM `{table_patient}`
        WHERE patient_id = @patient_id
        LIMIT 1
    """

    # Configure query with a parameter for patient_id
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("patient_id", "STRING", patient_id)
        ]
    )

    # Run the query
    query_job = client.query(query, job_config=job_config)

    # Fetch results
    result = query_job.result()
    rows = list(result)

    # Handle case where no results were found
    if not rows:
        return {"error": f"No data found for patient_id {patient_id}"}

    # Return the first row as a dictionary
    return dict(rows[0])


