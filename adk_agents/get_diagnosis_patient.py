#   adk_agents/get_diagnosis_patient.py
#   Analyze a patient’s clinical profile and return:
#   Cancer type, Clinical stage, Diagnosis confidence level
#   Reasoning/explanation


from google.cloud import bigquery
import os

def get_diagnosis_data(patient_id: str) -> dict:
    """
    Fetch the cancer patient diagnosis details from BigQuery using a given patient ID.

    Args:
        patient_id (str): The unique patient identifier.

    Returns:
        dict: Diagnosis details or an error message if no data is found.
    """
    # Get the project ID and table name from environment variables
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    table_patient = os.getenv("GOOGLE_BIGQUERY_TABLE_D")
   
   # Validate environment variables
    if not project_id:
        raise ValueError("Environment variable GOOGLE_CLOUD_PROJECT is not set.")
    if not table_patient:
        raise ValueError("Environment variable GOOGLE_BIGQUERY_TABLE_P is not set.")

    client = bigquery.Client(project=project_id)

    # Construct the SQL query with the actual table name injected
    query = f"""
        SELECT *
        FROM `{table_patient}`
        WHERE patient_id = @patient_id
        LIMIT 1
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("patient_id", "STRING", patient_id)
        ]
    )

    query_job = client.query(query, job_config=job_config)
    result = query_job.result()

    rows = list(result)
    if not rows:
        return {"error": f"No data found for patient_id {patient_id}"}

    return dict(rows[0])

