import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompts import RESUME_ANALYSIS_PROMPT, QUICK_TIPS_PROMPT

load_dotenv()


# ---------------- LLM ----------------
def get_llm(model_name: str = "llama-3.1-8b-instant", temperature: float = 0.3):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=temperature,
    )


# ---------------- MAIN ANALYSIS ----------------
def analyse_resume(resume_text: str, job_description: str) -> dict:
    llm = get_llm()
    chain = RESUME_ANALYSIS_PROMPT | llm

    raw_output = chain.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
    }).content

    return parse_analysis_output(raw_output)


# ---------------- QUICK TIPS ----------------
def get_quick_tips(resume_text: str) -> str:
    llm = get_llm()
    chain = QUICK_TIPS_PROMPT | llm

    return chain.invoke({
        "resume_text": resume_text
    }).content


# ---------------- PARSER ----------------
def parse_analysis_output(raw: str) -> dict:
    result = {
        "raw": raw,
        "score": 0,
        "strengths": [],
        "gaps": [],
        "improvements": [],
        "keywords": "",
        "verdict": "",
    }

    # Score
    score_match = re.search(r"MATCH SCORE:\s*(\d+)", raw)
    if score_match:
        result["score"] = int(score_match.group(1))

    # Sections extractor
    def extract_bullets(section_name: str, text: str):
        pattern = rf"\*?\*?{section_name}.*?:\*?\*?\s*(.*?)(?=\n\*?\*?[A-Z]|\Z)"
        match = re.search(pattern, text, re.DOTALL)

        if not match:
            return []

        block = match.group(1)

        return [b.strip() for b in re.findall(r"-\s*(.+)", block)]

    result["strengths"] = extract_bullets("STRENGTHS", raw)
    result["gaps"] = extract_bullets("SKILL GAPS", raw)
    result["improvements"] = extract_bullets("RESUME IMPROVEMENTS", raw)

    # Keywords
    keywords_match = re.search(r"\*?\*?KEYWORDS TO ADD.*?:\*?\*?\s*(.*?)(?=\n\*?\*?[A-Z]|\Z)", raw, re.DOTALL)
    if keywords_match:
        result["keywords"] = keywords_match.group(1).strip()

    # Verdict
    verdict_match = re.search(r"\*?\*?VERDICT.*?:\*?\*?\s*(.*)", raw, re.DOTALL)
    if verdict_match:
        result["verdict"] = verdict_match.group(1).strip()

    return result


# ---------------- TEST ----------------
if __name__ == "__main__":
    resume = "John Doe..."
    jd = "Looking for a Python developer."

    result = analyse_resume(resume, jd)

    print("\n=== RESUME ANALYSIS RESULT ===\n")
    print(result)