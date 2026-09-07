```python
import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.prompts import RESUME_ANALYSIS_PROMPT, QUICK_TIPS_PROMPT


# Load environment variables
load_dotenv()


# ---------------- LLM CONFIGURATION ----------------

DEFAULT_MODEL = "llama-3.1-8b-instant"


def get_llm(
    model_name: str = DEFAULT_MODEL,
    temperature: float = 0.3,
):
    """
    Create and return the Groq LLM client.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Add GROQ_API_KEY to your .env file locally "
            "or Streamlit Cloud Secrets when deployed."
        )

    return ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=temperature,
    )


# ---------------- GROQ CONNECTION TEST ----------------

def test_groq_connection() -> str:
    """
    Test whether the Groq API connection is working.
    """

    try:
        llm = get_llm(temperature=0)

        response = llm.invoke(
            "Reply with exactly: GROQ CONNECTION OK"
        )

        return response.content.strip()

    except Exception as e:
        raise RuntimeError(
            f"Groq connection failed: {type(e).__name__}: {str(e)}"
        ) from e


# ---------------- MAIN ANALYSIS ----------------

def analyse_resume(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Analyse a resume against a job description using Groq.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty.")

    try:
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
            raise ValueError(
                "Groq returned an empty response."
            )

        return parse_analysis_output(raw_output)

    except Exception as e:
        raise RuntimeError(
            f"Resume analysis failed: {type(e).__name__}: {str(e)}"
        ) from e


# ---------------- QUICK TIPS ----------------

def get_quick_tips(resume_text: str) -> str:
    """
    Generate quick resume improvement tips.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    try:
        llm = get_llm()

        chain = QUICK_TIPS_PROMPT | llm

        response = chain.invoke(
            {
                "resume_text": resume_text,
            }
        )

        return response.content.strip()

    except Exception as e:
        raise RuntimeError(
            f"Quick tips generation failed: "
            f"{type(e).__name__}: {str(e)}"
        ) from e


# ---------------- PARSER ----------------

def parse_analysis_output(raw: str) -> dict:
    """
    Convert the LLM's text response into a structured dictionary.
    """

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

    # ---------------- SCORE ----------------

    score_match = re.search(
        r"MATCH\s*SCORE\s*:\s*(\d+)",
        raw,
        re.IGNORECASE,
    )

    if score_match:
        try:
            score = int(score_match.group(1))
            result["score"] = max(0, min(score, 100))
        except ValueError:
            result["score"] = 0

    # ---------------- SECTION EXTRACTOR ----------------

    def extract_section(
        section_name: str,
        text: str,
    ) -> str:
        """
        Extract text between one section heading and the next.
        """

        pattern = (
            rf"(?:\*{{0,2}}\s*{re.escape(section_name)}"
            rf"\s*\*{{0,2}}\s*:?\s*)"
            rf"(.*?)"
            rf"(?="
            rf"\n\s*\*{{0,2}}\s*"
            rf"(?:MATCH\s*SCORE|STRENGTHS|SKILL\s*GAPS|"
            rf"RESUME\s*IMPROVEMENTS|KEYWORDS\s*TO\s*ADD|VERDICT)"
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

    # ---------------- BULLET EXTRACTOR ----------------

    def extract_bullets(block: str) -> list:
        """
        Extract bullet-point items from a section.
        """

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

    # ---------------- STRENGTHS ----------------

    strengths_block = extract_section(
        "STRENGTHS",
        raw,
    )

    result["strengths"] = extract_bullets(
        strengths_block
    )

    # ---------------- SKILL GAPS ----------------

    gaps_block = extract_section(
        "SKILL GAPS",
        raw,
    )

    result["gaps"] = extract_bullets(
        gaps_block
    )

    # ---------------- RESUME IMPROVEMENTS ----------------

    improvements_block = extract_section(
        "RESUME IMPROVEMENTS",
        raw,
    )

    result["improvements"] = extract_bullets(
        improvements_block
    )

    # ---------------- KEYWORDS ----------------

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

    # ---------------- VERDICT ----------------

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


# ---------------- LOCAL TEST ----------------

if __name__ == "__main__":

    print("\n==============================")
    print(" GROQ CONNECTION TEST")
    print("==============================\n")

    try:
        test_result = test_groq_connection()
        print(test_result)

    except Exception as e:
        print("\nERROR:")
        print(e)
        raise SystemExit(1)

    print("\n==============================")
    print(" RESUME ANALYSIS TEST")
    print("==============================\n")

    resume = """
    John Doe
    Python Developer

    Skills:
    Python, SQL, Pandas, NumPy, Machine Learning

    Experience:
    Built Python data processing pipelines.
    Developed machine learning models.
    Created REST APIs using Python.
    """

    job_description = """
    Looking for a Python developer with experience in
    Python, SQL, machine learning, APIs, and data science.
    """

    try:
        result = analyse_resume(
            resume,
            job_description,
        )

        print("MATCH SCORE:")
        print(result["score"])

        print("\nSTRENGTHS:")
        for item in result["strengths"]:
            print("-", item)

        print("\nSKILL GAPS:")
        for item in result["gaps"]:
            print("-", item)

        print("\nRESUME IMPROVEMENTS:")
        for item in result["improvements"]:
            print("-", item)

        print("\nKEYWORDS:")
        print(result["keywords"])

        print("\nVERDICT:")
        print(result["verdict"])

        print("\nRAW OUTPUT:")
        print(result["raw"])

    except Exception as e:
        print("\nANALYSIS ERROR:")
        print(e)
```
