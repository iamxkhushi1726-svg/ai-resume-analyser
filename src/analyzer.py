```python
import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.prompts import RESUME_ANALYSIS_PROMPT, QUICK_TIPS_PROMPT


load_dotenv()


DEFAULT_MODEL = "llama-3.1-8b-instant"


def get_llm(
    model_name: str = DEFAULT_MODEL,
    temperature: float = 0.3,
):
    """Create and return the Groq LLM client."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Add it to Streamlit Cloud Secrets."
        )

    return ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=temperature,
    )


def analyse_resume(
    resume_text: str,
    job_description: str,
) -> dict:
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

    return parse_analysis_output(raw_output)


def get_quick_tips(resume_text: str) -> str:
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


def parse_analysis_output(raw: str) -> dict:
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
        result["score"] = max(
            0,
            min(int(score_match.group(1)), 100),
        )

    def extract_section(
        section_name: str,
        text: str,
    ) -> str:

        pattern = (
            rf"(?:\*{{0,2}}\s*"
            rf"{re.escape(section_name)}"
            rf"\s*\*{{0,2}}\s*:?\s*)"
            rf"(.*?)"
            rf"(?="
            rf"\n\s*\*{{0,2}}\s*"
            rf"(?:MATCH\s*SCORE|STRENGTHS|"
            rf"SKILL\s*GAPS|RESUME\s*IMPROVEMENTS|"
            rf"KEYWORDS\s*TO\s*ADD|VERDICT)"
            rf"\b"
            rf"|\Z)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return ""

        return match.group(1).strip()

    def extract_bullets(block: str) -> list:

        if not block:
            return []

        bullets = re.findall(
            r"(?:^|\n)\s*[-•*]\s+(.+?)(?=\n|$)",
            block,
            re.MULTILINE,
        )

        cleaned = []

        for bullet in bullets:
            bullet = re.sub(
                r"\s+",
                " ",
                bullet,
            ).strip()

            if bullet:
                cleaned.append(bullet)

        return cleaned

    strengths_block = extract_section(
        "STRENGTHS",
        raw,
    )

    result["strengths"] = extract_bullets(
        strengths_block
    )

    gaps_block = extract_section(
        "SKILL GAPS",
        raw,
    )

    result["gaps"] = extract_bullets(
        gaps_block
    )

    improvements_block = extract_section(
        "RESUME IMPROVEMENTS",
        raw,
    )

    result["improvements"] = extract_bullets(
        improvements_block
    )

    keywords_block = extract_section(
        "KEYWORDS TO ADD",
        raw,
    )

    if keywords_block:
        result["keywords"] = re.sub(
            r"\s+",
            " ",
            keywords_block,
        ).strip()

    verdict_block = extract_section(
        "VERDICT",
        raw,
    )

    if verdict_block:
        result["verdict"] = re.sub(
            r"\s+",
            " ",
            verdict_block,
        ).strip()

    return result
```
