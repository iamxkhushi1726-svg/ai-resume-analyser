from langchain_core.prompts import PromptTemplate


RESUME_ANALYSIS_TEMPLATE = """
You are an expert technical recruiter and career coach with 15 years of
experience hiring software engineers and AI/ML engineers at top technology
companies.

Analyse the following resume against the provided job description.

Be specific, honest, and actionable. Do not be vague.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis in EXACTLY this format.

MATCH SCORE: [a number from 0 to 100]

STRENGTHS:
- [specific strength 1]
- [specific strength 2]
- [specific strength 3]

SKILL GAPS:
- [gap 1 with explanation]
- [gap 2 with explanation]
- [gap 3 with explanation]

RESUME IMPROVEMENTS:
- [improvement 1]
- [improvement 2]
- [improvement 3]

KEYWORDS TO ADD:
[comma-separated list of important keywords from the JD]

VERDICT:
[2-3 sentence honest assessment of the candidate's fit for this role
and the single most important thing they should do to improve their chances]
"""


RESUME_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=[
        "resume_text",
        "job_description",
    ],
    template=RESUME_ANALYSIS_TEMPLATE,
)


QUICK_TIPS_TEMPLATE = """
You are an expert resume writer and ATS optimization specialist.

Given the resume text below, provide exactly 5 specific and actionable
tips to improve the resume regardless of any particular job description.

Focus on:
formatting,
clarity,
measurable impact,
technical presentation,
and ATS optimization.

RESUME:
{resume_text}

Respond with exactly 5 numbered tips.

Be specific and direct.
"""


QUICK_TIPS_PROMPT = PromptTemplate(
    input_variables=["resume_text"],
    template=QUICK_TIPS_TEMPLATE,
)

