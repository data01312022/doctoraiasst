# Doctor AI Agents  
**Patient-Centric Clinical and Disease Diagnosis with Treatment Optimization**

## Inspiration
Doctor AI Agent was born from the need to support oncologists in making faster, more accurate decisions using multimodal data (EHR, genomics, imaging) while reducing manual effort and improving patient outcomes.

## What It Does
- Ingests patient data (structured & unstructured)
- Diagnoses diseases (e.g., cancer types/stages) using clinical reasoning
- Recommends personalized treatment plans based on NCCN and historical data
- Matches patients with relevant clinical trials using biomarkers
- Offers explainable outputs for doctors and patients

## How We Built It
**Tech Stack:**
- GCP: Vertex AI, BigQuery, Healthcare API, Cloud Storage, Cloud Run, Python
- LLMs: Gemini-2.0-flash-001 and RAG
- Agents: Built using Agent Development Kits (ADK's),Vertex AI,LangChain
- Data: FHIR, DICOM, VCF (genomics), HL7
- UI: ADK's + Cloud Run with Doctor Mode
**Agents:**
- `Patient Data Agent`: Validates and processes patient data
- `Diagnosis Agent`: Generates a probable diagnosis based on the patient’s symptoms, age, gender, and clinical features using LLM 
- `Treatment Planner Agent`: Suggests treatment regimens using NCCN
- `Clinical Trial Matcher Agent`: Searches local/global clinical trial registries from ClinicalTrials.gov to find matching trials for eligible patients.
- `explainable Agent`: Uses the MedPaLM (or similar) model to generate citation-backed, patient-friendly and doctor-readable explanations for the diagnosis and treatment

##  Challenges
| Problem | Resolution |
|--------|------------|
| Handling PII and compliance | GCP Healthcare APIs, HIPAA, GDPR |
| LLM hallucination | RAG with medical knowledge grounding |
| Complex data orchestration | Multi-agent coordination with LangGraph |
| Trust building with doctors | Explainable AI, Doctor UI with citations |
## Accomplishments
- >85% diagnostic support accuracy in test cases
- Real-time clinical trial matcher
- Integrated multi-modal clinical data
- Streamlined UX for doctors with override options

## What We Learned
- Domain-specific LLM tuning is essential
- Explainability & compliance are non-negotiable
- Agent-based systems scale efficiently for healthcare
- RAG makes LLMs more factual and trusted

## What’s Next
- Integrate with genomics platforms- Support personalized therapies based on mutations, gene panels, and biomarkers
- Speech-based input for real-time consultation- Deploy as a voice assistant in outpatient or surgical settings
- Regulatory Readiness and HIPAA/GDPR Compliance
- Provide doctors and patients with traceable rationale for every AI suggestion including scientific citations, NCCN cross-references, trial inclusion/exclusion reasons
- Clinical pilot deployment and regulatory pathways

## Our Goal
- Empower every physician with a safe, explainable, and personalized AI assistant – built for real-world healthcare

