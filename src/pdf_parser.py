import PyPDF2
import io
import re


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text from an uploaded PDF file.
    Works with streamlit's UploadedFile object directly.
    Returns cleaned plain text string.
    """
    try:
        uploaded_file.seek(0)
        pdf_bytes = io.BytesIO(uploaded_file.read())
        uploaded_file.seek(0)

        reader = PyPDF2.PdfReader(pdf_bytes)

        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        if not text_parts:
            raise ValueError(
                "No extractable text found. The PDF may be scanned or image-based."
            )


        full_text = clean_text("\n".join(text_parts))
        return full_text
    
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {e}") from e
    

def clean_text(text: str) -> str:
    """
    Clean extracted PDF text:
    - Remove excessive whitespace and newlines
    - Remove non-printable characters
    - Preserve meaningful line breaks
    """

    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text

def truncate_text(text: str, max_chars: int = 4000) -> str:
    """
    Truncate text to fit within LLM context limits.
    Keeps the most important first portion of the resume.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[Resume truncated to fit context limit]"

def get_resume_stats(text: str) -> dict:
    """Return basic stats about the extracted resume text."""
    return {
        "char_count": len(text),
        "word_count": len(text.split()),
        "line_count": len([line for line in text.splitlines() if line.strip()]),
        "is_empty": len(text.strip()) == 0,
    }