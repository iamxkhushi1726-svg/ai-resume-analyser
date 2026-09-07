import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.prompts import RESUME_ANALYSIS_PROMPT, QUICK_TIPS_PROMPT


load_dotenv()


# Use a currently supported Groq model.
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def get_llm(
    model_name=DEFAULT_MODEL,
    temperature=0.3,
):
    """Create and return the Groq LLM client."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add GROQ_API_KEY to Streamlit Cloud Secrets."
        )

    return ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=temperature,
    )


def analyse_resume(resume_text, job_description):
    """Analyse a resume against a job description."""

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty.")

    llm = get_llm()

    chain = RESUME_ANALYSIS_PROMPT | llm

    response = chain.invoke(
        {
            "resume_text": resume_text,
            "job_description": job_description,
        }
    )

    raw_output = response.content

    if not raw_output:
        raise ValueError("Groq returned an empty response.")

    return parse_analysis_output(raw_output)


def get_quick_tips(resume_text):
    """Generate quick resume improvement tips."""

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    llm = get_llm()

    chain = QUICK_TIPS_PROMPT | llm

    response = chain.invoke(
        {
            "resume_text": resume_text,
        }
    )

    return response.content.strip()


def parse_analysis_output(raw):
    """Convert LLM output into a structured dictionary."""

    result = {
        "raw": raw,
        "score": 0,
        "strengths": [],
        "gaps": [],
        "improvements": [],
        "keywords": "",
        "verdict": "",
    }

    if not raw:
        return result

    score_match = re.search(
        r"MATCH\s*SCORE\s*:\s*(\d+)",
        raw,
        re.IGNORECASE,
    )

    if score_match:
        score = int(score_match.group(1))
        result["score"] = max(0, min(score, 100))

    def extract_section(section_name, text):
        pattern = (
            r"\*{0,2}\s*"
            + re.escape(section_name)
            + r"\s*\*{0,2}\s*:?\s*"
            r"(.*?)"
            r"(?=\n\s*\*{0,2}\s*"
            r"(?:MATCH SCORE|STRENGTHS|SKILL GAPS|"
            r"RESUME IMPROVEMENTS|KEYWORDS TO ADD|VERDICT)"
            r"\b|\Z)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return ""

        return match.group(1).strip()

    def extract_bullets(block):
        if not block:
            return []

        matches = re.findall(
            r"(?:^|\n)\s*[-•*]\s+(.+)",
            block,
            re.MULTILINE,
        )

        return [
            re.sub(r"\s+", " ", item).strip()
            for item in matches
            if item.strip()
        ]

    strengths = extract_section(
        "STRENGTHS",
        raw,
    )

    gaps = extract_section(
        "SKILL GAPS",
        raw,
    )

    improvements = extract_section(
        "RESUME IMPROVEMENTS",
        raw,
    )

    keywords = extract_section(
        "KEYWORDS TO ADD",
        raw,
    )

    verdict = extract_section(
        "VERDICT",
        raw,
    )

    result["strengths"] = extract_bullets(
        strengths
    )

    result["gaps"] = extract_bullets(
        gaps
    )

    result["improvements"] = extract_bullets(
        improvements
    )

    if keywords:
        result["keywords"] = re.sub(
            r"\s+",
            " ",
            keywords,
        ).strip()

    if verdict:
        result["verdict"] = re.sub(
            r"\s+",
            " ",
            verdict,
        ).strip()

    return result

