#   Doctor AI Agent  AI-based intelligent assistant (Multi-Agents) using Google's ADK's & Vertex AI Agent Framework (google.adk.agents.Agent). 
#   The assistant is specifically tailore to support oncologists (cancer doctors) 
#   by simplifying patient diagnosis, recommending clinical trials, and suggesting treatment plans 
#   aligned with NCCN (National Comprehensive Cancer Network) guidelines.

from google.adk.agents import Agent
from adk_agents.get_patient_data import get_patient_data
from adk_agents.get_diagnosis_patient import get_diagnosis_data
from adk_agents.clinical_trial_search import search_clinical_trials
from adk_agents.treatment_plan_Agent  import get_nccn_guidelines_data
from adk_agents.explainable_by_MedPaL import fetch_patient_context
from adk_agents.explainable_by_MedPaL import generate_explanation

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description=(
        "You are a knowledgeable AI assistant specializing in oncology. Your primary role is to help doctors by:\n"
        "- Looking up patient information when provided with a patient ID.\n"
        "- Fetching the latest diagnosis reports from hospital databases.\n"
        "- Recommending appropriate clinical trials based on a patient's cancer type or diagnosis.\n\n"
        "Always ensure your responses are clear, medically relevant, and accurate.\n"
        "When information is missing, suggest the next logical steps for the physician.\n"
        "Uses Vertex AI Gemini model to generate a citation-backed, human-readable explanation for a cancer patient's diagnosis and treatment plan based on NCCN guidelines."
    ),
    tools=[
        get_patient_data,
        get_diagnosis_data,
        search_clinical_trials,
        get_nccn_guidelines_data,
        fetch_patient_context,
        generate_explanation
    ]
)

