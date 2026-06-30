from langchain_core.prompts import PromptTemplate


RESUME_ANALYSIS_TEMPLATE = """
You are an expert technical recruiter and career coach with 15 years of experience
hiring software engineer and AI/ML engineers at top tech companies.

Analyse the following resume against the job description provided.
Be specific, honest, and actionable. Do not be vague.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis in EXACTLY this format - do not deviate:

MATCH SCORE: [a number from 0 to 100]

STRENGTHS (what makes this candidate strong for this role):
- [specific strength 1]
- [specific strength 2]
- [specific strength 3]

SKILL GAPS (skills in the JD that are missing or weak in the resume):
- [gap 1 with explanation]
- [gap 2 with explanation]
- [gap 3 with explanation]

RESUME IMPROVEMENTS (specific changes to make this resume stronger):
- [improvement 1]
- [improvement 2]
- [improvement 3]

KEYWORDS TO ADD (important keywords from the JD missing in the resume):
[comma-separated list of keywords]

VERDICT:
[2-3 sentence honest assessment of the candidate's fit for this role
and the single most important thing they should do to improve their chances]
"""

RESUME_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template=RESUME_ANALYSIS_TEMPLATE,
)


QUICK_TIPS_TEMPLATE = """
You are a resume expert. Given this resume text, provide 5 quick,
specific, actionable tips to improve it — regardless of any job description.
Focus on formatting, clarity, impact, and ATS optimisation.

RESUME:
{resume_text}

Respond with exactly 5 numbered tips. Be specific and direct.
"""

QUICK_TIPS_PROMPT = PromptTemplate(
    input_variables=["resume_text"],
    template=QUICK_TIPS_TEMPLATE,
)

# Test
print(
    RESUME_ANALYSIS_PROMPT.format(
        resume_text="John Doe...",
        job_description="Looking for a Python developer."
    )
)
