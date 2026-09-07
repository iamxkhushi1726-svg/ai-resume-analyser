import streamlit as st
import sys
import os


# Make project root available to Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from src.pdf_parser import (
    extract_text_from_pdf,
    truncate_text,
    get_resume_stats,
)

from src.analyzer import (
    analyse_resume,
    get_quick_tips,
)


# ─────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon="🧠",
    layout="wide",
)


# ─────────────────────────────────────────────────────────────
# PREMIUM DARK FOREST WORKSPACE
# ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Serif+Display'
        '&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400'
        '&family=JetBrains+Mono:wght@400;500&display=swap'
    );

    .stApp {
        background-color: #080b0a;
    }

    .stApp p,
    .stApp li,
    .stApp label {
        font-family: 'Libre Baskerville', serif !important;
        color: #dcdad2 !important;
        font-size: 1.02rem;
        line-height: 1.6;
    }

    .executive-headline {
        font-family: 'DM Serif Display', serif !important;
        font-size: 3.8rem !important;
        font-weight: 400 !important;
        line-height: 1.1 !important;
        color: #ffffff !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.4rem !important;
        letter-spacing: -0.02em;
        display: block;
    }

    .executive-headline span {
        font-family: 'DM Serif Display', serif !important;
        color: #e4dec3 !important;
    }

    .executive-caption {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        color: #58695d !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    h2,
    h3,
    .stSubheader p {
        font-family: 'DM Serif Display', serif !important;
        color: #ffffff !important;
        font-size: 1.7rem !important;
        font-weight: 400 !important;
        margin-bottom: 1rem !important;
    }

    div[data-testid="stSidebar"] {
        background-color: #111413 !important;
        border-right: 1px solid #232c26 !important;
    }

    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] label {
        font-size: 0.95rem !important;
    }

    div[data-baseweb="textarea"],
    div[data-baseweb="file-uploader"] {
        background-color: #151d19 !important;
        border: 1px solid #2d3c34 !important;
        border-radius: 0px !important;
    }

    div[data-baseweb="textarea"] textarea {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.95rem !important;
    }

    .stButton > button {
        background-color: #e4dec3 !important;
        color: #080b0a !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border: none !important;
        border-radius: 0px !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .stButton > button:hover {
        background-color: #ffffff !important;
        color: #080b0a !important;
        box-shadow: 0 4px 20px rgba(228, 222, 195, 0.2);
    }

    .stButton > button p {
        color: #080b0a !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
    }

    div[data-testid="stNotification"] {
        background-color: #151d19 !important;
        border: 1px solid #2d3c34 !important;
        color: #dcdad2 !important;
        border-radius: 0px !important;
    }

    div[data-testid="stNotification"] p {
        color: #dcdad2 !important;
    }

    hr {
        border-color: #232c26 !important;
        margin: 2.5rem 0 !important;
    }

    code,
    pre {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #151d19 !important;
        color: #a3bda8 !important;
    }

    div[data-testid="stProgress"] > div > div > div {
        background-color: #4c6253 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<h1 class="executive-headline">'
    '🧠 <span>AI Resume Analyser</span>'
    '</h1>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="executive-caption">'
    'Powered by LangChain + Groq (Llama 3.3 70B) · '
    'Project 08/100 · Built by Khushi'
    '</p>',
    unsafe_allow_html=True,
)

st.markdown("---")


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

st.sidebar.markdown("### Operational Pipeline")

st.sidebar.markdown(
    """
    This module performs deterministic alignment scanning across
    unstructured text architectures, optimized for AI engineering
    candidates.

    1. **PDF Tokenization:** PyPDF2 handles stream ingestion.
    2. **Context Matching:** Map profiles directly against target requirements.
    3. **Inference Loop:** Llama 3.3 70B processes structural gaps
       and missing technical metrics.
    """
)

st.sidebar.markdown("---")


mode = st.sidebar.radio(
    "Analysis Configuration",
    [
        "Target Mandate Scan (Resume + JD)",
        "Isolated ATS Metrics (Resume Only)",
    ],
)


st.sidebar.markdown("---")


st.sidebar.caption(
    "System Stack: Llama 3.3 70B · "
    "Groq API · Python · Pydantic Validation"
)


# ─────────────────────────────────────────────────────────────
# MAIN INPUT AREA
# ─────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)


with col1:

    st.subheader("Source Resume Profile (PDF)")

    uploaded_file = st.file_uploader(
        "Upload source portfolio",
        type=["pdf"],
        help=(
            "Optimized for text-based, non-rasterized PDF "
            "records under 5MB."
        ),
        label_visibility="collapsed",
    )

    if uploaded_file:

        st.success(
            f"Stream initialized successfully: "
            f"{uploaded_file.name}"
        )


with col2:

    st.subheader("Target Role Mandate Matrix")

    job_description = st.text_area(
        "Paste requirement matrix here",
        height=200,
        placeholder=(
            "Paste full technical expectations, "
            "stack requirements, and corporate "
            "operational criteria..."
        ),
        disabled=(
            mode == "Isolated ATS Metrics (Resume Only)"
        ),
        label_visibility="collapsed",
    )


# ─────────────────────────────────────────────────────────────
# EXECUTION TRIGGER
# ─────────────────────────────────────────────────────────────

st.markdown("---")


analyse_btn = st.button(
    "Execute Alignment Audit",
    type="primary",
    use_container_width=True,
)


if analyse_btn:

    # ─────────────────────────────────────────────────────────
    # INPUT VALIDATION
    # ─────────────────────────────────────────────────────────

    if not uploaded_file:

        st.error(
            "Execution Defect: Staged resume document "
            "input track missing."
        )

        st.stop()


    if (
        mode == "Target Mandate Scan (Resume + JD)"
        and not job_description.strip()
    ):

        st.error(
            "Execution Defect: Context matrix array empty. "
            "Supply target validation guidelines."
        )

        st.stop()


    # ─────────────────────────────────────────────────────────
    # PDF EXTRACTION
    # ─────────────────────────────────────────────────────────

    with st.spinner(
        "Extracting text token vectors..."
    ):

        try:

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        except ValueError as e:

            st.error(str(e))
            st.stop()


    # ─────────────────────────────────────────────────────────
    # RESUME STATISTICS
    # ─────────────────────────────────────────────────────────

    stats = get_resume_stats(
        resume_text
    )


    if stats["is_empty"]:

        st.error(
            "Ingestion Failure: Zero character length "
            "processed. Validate PDF internal layout "
            "structure."
        )

        st.stop()


    # Limit text sent to the LLM
    resume_text = truncate_text(
        resume_text,
        max_chars=4000,
    )


    st.info(
        f"Data Mapped: {stats['word_count']} "
        f"words parsed into temporary token cache."
    )


    # ─────────────────────────────────────────────────────────
    # RESUME-ONLY MODE
    # ─────────────────────────────────────────────────────────

    if mode == "Isolated ATS Metrics (Resume Only)":

        with st.spinner(
            "Processing standalone structural critique..."
        ):

            try:

                tips = get_quick_tips(
                    resume_text
                )

            except Exception as e:

                st.error(
                    f"Groq processing error: {str(e)}"
                )

                st.stop()


        st.markdown("---")

        st.subheader(
            "Isolated Optimization Protocols"
        )

        st.markdown(tips)


    # ─────────────────────────────────────────────────────────
    # RESUME + JOB DESCRIPTION MODE
    # ─────────────────────────────────────────────────────────

    else:

        with st.spinner(
            "Evaluating structural stack overlap "
            "(Groq Ingest)..."
        ):

            try:

                result = analyse_resume(
                    resume_text,
                    job_description,
                )

            except Exception as e:

                st.error(
                    f"Groq analysis failed: {str(e)}"
                )

                st.info(
                    "If this error mentions "
                    "'model_not_found', verify that the "
                    "configured Groq model is available "
                    "for your API key."
                )

                st.stop()


        st.markdown("---")


        # ─────────────────────────────────────────────────────
        # SCORE MATRIX
        # ─────────────────────────────────────────────────────

        score = result["score"]


        st.subheader(
            f"ATS Alignment Index: {score} / 100"
        )


        st.progress(
            score / 100
        )


        col_a, col_b, col_c = st.columns(3)


        # ─────────────────────────────────────────────────────
        # STRENGTHS
        # ─────────────────────────────────────────────────────

        with col_a:

            st.subheader(
                "Validated Strengths"
            )

            if result["strengths"]:

                for strength in result["strengths"]:

                    st.markdown(
                        f"• {strength}"
                    )

            else:

                st.markdown(
                    result["raw"]
                )


        # ─────────────────────────────────────────────────────
        # SKILL GAPS
        # ─────────────────────────────────────────────────────

        with col_b:

            st.subheader(
                "Technical Gap Analysis"
            )

            if result["gaps"]:

                for gap in result["gaps"]:

                    st.markdown(
                        f"• {gap}"
                    )

            else:

                st.info(
                    "No specific skill gaps were detected."
                )


        # ─────────────────────────────────────────────────────
        # IMPROVEMENTS
        # ─────────────────────────────────────────────────────

        with col_c:

            st.subheader(
                "Iterative Remediation Path"
            )

            if result["improvements"]:

                for improvement in result["improvements"]:

                    st.markdown(
                        f"• {improvement}"
                    )

            else:

                st.info(
                    "No specific improvements were returned."
                )


        # ─────────────────────────────────────────────────────
        # KEYWORDS
        # ─────────────────────────────────────────────────────

        if result["keywords"]:

            st.markdown("---")

            st.subheader(
                "Missing Technical Identifiers"
            )

            st.info(
                result["keywords"]
            )


        # ─────────────────────────────────────────────────────
        # VERDICT
        # ─────────────────────────────────────────────────────

        if result["verdict"]:

            st.markdown("---")

            st.subheader(
                "Executive Fit Assessment"
            )

            st.warning(
                result["verdict"]
            )


        # ─────────────────────────────────────────────────────
        # RAW MODEL OUTPUT
        # ─────────────────────────────────────────────────────

        with st.expander(
            "System Diagnostic Logs"
        ):

            st.text(
                result["raw"]
            )


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────

st.markdown("---")

st.markdown(
    '<p class="executive-caption" '
    'style="text-align: center;">'
    'Operational Infrastructure Stack: '
    'Llama 3.3 70B + Groq + LangChain Processing Pipeline'
    '</p>',
    unsafe_allow_html=True,
)
