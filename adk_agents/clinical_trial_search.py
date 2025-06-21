#   adk_agents/clinical_trial_search.py
#   This module enables intelligent matching of patients to relevant clinical trials by:
#   Using the patient’s cancer type, stage, biomarkers, and location
#   Searching structured sources like clinicaltrials.gov, internal registries, or a BigQuery dataset


from serpapi import GoogleSearch
import os

# Get the project ID and table name from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
SERP_KEY = os.getenv("SERP_API_KEY")

SERP_API_KEY = SERP_KEY # store securely in .env

def search_clinical_trials(cancer_type: str) -> list:
    """ Search for clinical trials related to a specific cancer type using Google search via SerpAPI.This function constructs a search query targeting ClinicalTrials.gov and fetches the top 5 organic search results from Google using SerpAPI."""

    query = f"{cancer_type} cancer site:clinicaltrials.gov"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Parse top 5 results
    trial_links = []
    for result in results.get("organic_results", [])[:5]:
        title = result.get("title")
        link = result.get("link")
        trial_links.append(f"{title} - {link}")

    return trial_links or ["No trials found."]
