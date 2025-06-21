#   adk_agents/get_patient_data.py
from google.cloud import bigquery
import os

def get_patient_data(patient_id: str) -> dict:
    """
    Fetch cancer patient details from BigQuery using the provided patient_id.

    This function connects to the BigQuery dataset `patient_records`,
    executes a parameterized SQL query to retrieve patient data matching the given patient_id, 
    and returns the result as a dictionary.

    Parameters:
    ----------
    patient_id : str
        The unique identifier for the cancer patient whose record is to be fetched.
    """
    # Get the project ID and table name from environment variables
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    table_patient = os.getenv("GOOGLE_BIGQUERY_TABLE_P")

    # Validate environment variables
    if not project_id:
        raise ValueError("Environment variable GOOGLE_CLOUD_PROJECT is not set.")
    if not table_patient:
        raise ValueError("Environment variable GOOGLE_BIGQUERY_TABLE_P is not set.")

    # Initialize the BigQuery client with the project ID
    client = bigquery.Client(project=project_id)

    # Construct the SQL query with the actual table name injected
    query = f"""
        SELECT *
        FROM `{table_patient}`
        WHERE patient_id = @patient_id
        LIMIT 1
    """

    # Configure the query with parameters to prevent SQL injection and support dynamic input
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("patient_id", "STRING", patient_id)
        ]
    )

    # Execute the query with the given configuration
    query_job = client.query(query, job_config=job_config)

    # Wait for the query job to complete and retrieve the result
    result = query_job.result()

    # Convert the result to a list to check if any rows were returned
    rows = list(result)
    
    # If no data found for the given patient_id, return a custom error message
    if not rows:
        return {"error": f"No data found for patient_id {patient_id}"}

    # Convert the first (and only) row to a dictionary and return it
    return dict(rows[0])

