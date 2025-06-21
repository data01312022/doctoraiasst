"""
Explainability Agent for Cancer Patient Diagnosis Support using:
- Google Cloud ADK (Agent Developer Kit)
- Med-PaLM 2 (LLM from Google for Medical Domain)
- GCP services: BigQuery, Vertex AI, Cloud Storage
- Output: Human-readable, citation-backed explanations for diagnosis/treatment
"""

import os
from google.adk.agents import Agent
from google.cloud import bigquery
from google.cloud import storage
from vertexai.preview.generative_models import GenerativeModel, Part

# Step 1: Environment Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
EXPLANATION_TABLE = os.getenv("EXPLANATIONS_TABLE")  # e.g. explanations
LLM_MODEL = os.getenv("GEMINI_MED_VERSION")  # Med-PaLM model on Vertex AI (private preview) or "gemini-med" as fallback

# Step 2: Tool - Fetch Clinical/Genomic Data
def fetch_patient_context(patient_id: str) -> dict:
    """Retrieve patient diagnosis, genomic profile, and treatment plan from BigQuery."""
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT *
        FROM `{EXPLANATION_TABLE}`
        WHERE patient_id = @patient_id
        LIMIT 1
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("patient_id", "STRING", patient_id)]
    )
    result = list(client.query(query, job_config=job_config).result())
    if not result:
        return {"error": f"No data found for patient_id {patient_id}"}
    return dict(result[0])


def generate_explanation(patient_context: dict) -> str:
    """
    Uses Vertex AI Gemini model to generate a citation-backed, human-readable explanation 
    for a cancer patient's diagnosis and treatment plan based on NCCN guidelines.
    """

    # Load Gemini model - you can also try: gemini-1.5-pro-001
    model = GenerativeModel(LLM_MODEL)

    # Prompt template
    prompt = f"""
    You are a knowledgeable AI assistant specializing in oncology.
    Explain the diagnosis and treatment plan based on the patient details, 
    including matching clinical stage and cancer type with NCCN guidelines.
    Provide clear, medically sound, human-readable output.
    Context: {patient_context}
    Instructions:
    - Summarize the patient’s cancer diagnosis and recommended treatment plan.
    - Justify the recommendation based on NCCN guidelines.
    - If possible, cite research papers or clinical guidelines inline like [1], [2], etc.
    """

    # Generate response
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.4,
            "max_output_tokens": 1024
        }
    )

    return response.text

