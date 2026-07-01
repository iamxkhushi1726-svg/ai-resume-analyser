# 🧠 AI Resume Analyser

> Project 08/100 — Building a strong GitHub portfolio from scratch.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://iamxkhushi1726-svg-ai-resume-analyser-app-ffqp2d.streamlit.app/)

An AI-powered resume analysis engine built with LangChain and Llama 3 via Groq. By cross-referencing unstructured PDF resumes against target job descriptions, the application instantly calculates a tailored match score, identifies critical skill gaps, isolates missing keywords, and delivers actionable formatting and content recommendations for optimal ATS alignment.

## Live Demo

👉 [Open App](https://iamxkhushi1726-svg-ai-resume-analyser-app-ffqp2d.streamlit.app/)

## System Architecture & Data Pipeline

The application establishes a synchronous, highly constrained pipeline that safely handles file stream parsing, dynamic schema validation, and low-latency token ingestion:

```text
                 +---------------------------+
                 |     PDF Resume (.pdf)     |
                 +-------------+-------------+
                               |
                               v
                  PyPDF2 Text Extraction
                               |
                               v
                 Cleaning & Token Truncation
                               |
                               +------------------+
                                                  |
                                                  v
                 +---------------------------+    +---------------------------+
                 |    Job Description (JD)   | -> |     LangChain Prompt      |
                 +---------------------------+    +-------------+-------------+
                                                                |
                                                                v
                                                 Groq (Llama-3-8b-8192)
                                                                |
                                                                v
                                                  Pydantic Output Parser
                                                                |
                                                                v
                                           ATS Score • Skill Gaps • Keywords
                                           • Strengths • Suggestions
```


1. **Stream Ingestion & Token Normalization:** Raw structural streams are extracted from user-supplied PDFs via `PyPDF2`. Extraneous structural whitespace and formatting markers are sanitized, and total text inputs are bounded to a maximum allocation window of 4,000 characters to optimize processing throughput.
2. **Contextual Alignment Mapping:** Context vectors from the candidate text and the baseline role matrix are integrated into a standardized multi-variable instruction template engineered to control response variability.
3. **Deterministic Output Serialization:** The underlying core inference model (`Llama 3`) runs on the **Groq API** layer to keep runtime computation latency under 2 seconds. The output is processed by a strict `Pydantic` schema constraint model, preventing string generation failures or parsing errors.

---

## Core Features & Technical Capabilities

* **Dual-Mode Analytical Arrays:**
  * **Contextual Mandate Mode:** Compares candidate profiles directly with comprehensive, multi-layered job specifications.
  * **Autonomous Review Mode:** Evaluates systemic structural parameters, terminology standards, and layout optimizations purely on the resume token stream when no target role data is provided.
* **Granular Gap Isolate Engine:** Runs comparative matrix audits to target exact discrepancies across programming languages, engineering methodologies, and key technological frameworks.
* **Algorithmic Fit Index:** Provides a mathematical compliance index from 0 to 100 alongside structured reasoning steps instead of relying on unpredictable free-form text blocks.

---

## Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq-000000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Llama_3-4B0082?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PyPDF2-217346?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge" />
  <img src="https://img.shields.io/badge/python--dotenv-306998?style=for-the-badge" />
</p>


---

## Deployment & Local Replication

### System Prerequisites
Ensure your operating terminal has Python 3.10+ configured alongside an isolated virtual environment manager.

```bash
# Clone the repository source tree
git clone [https://github.com/iamxkhushi1726-svg/ai-resume-analyser.git](https://github.com/iamxkhushi1726-svg/ai-resume-analyser.git)
cd ai-resume-analyser

# Build and activate isolated virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows execution: .venv\Scripts\activate

# Install compiled package requirements
pip install -r requirements.txt

# Configure system run-time environment secrets
echo "GROQ_API_KEY=your_actual_groq_api_key_here" > .env

# Initialize application container runtime
streamlit run app.py
```

> **Deployment Note:** Generate a free API key from the **Groq Console** and add it to your `.env` file before running the application.

> Get your free API key: https://console.groq.com


## 📂 Project Structure

```text
ai-resume-analyser/
├── src/
│   ├── pdf_parser.py    # PDF text extraction and preprocessing
│   ├── prompts.py       # LangChain prompt templates
│   └── analyzer.py      # LLM analysis pipeline and Pydantic output parsing
├── app.py               # Streamlit application
├── .env.example         # Environment variable template
├── requirements.txt     # Project dependencies
├── .gitignore
└── README.md
```

## What I Learned

- How to build a production LLM application with LangChain
- How to use Groq API for free, fast LLM inference
- How to write structured prompt templates that produce parseable output
- How to extract and clean text from PDF files with PyPDF2
- How to securely manage API keys with dotenv in Streamlit Cloud

## Part of 100 Projects Challenge

Project 08 of my 100-project challenge to secure AI/ML internships.

⭐ If you like this project, consider giving it a star.

Follow my progress: [GitHub Profile](https://github.com/iamxkhushi1726-svg)