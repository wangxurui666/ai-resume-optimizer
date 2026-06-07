"""
Resume parser: extract text from PDF and DOCX files.
"""
from pypdf import PdfReader
from docx import Document
import io


def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF resume."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts)


def parse_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX resume."""
    doc = Document(io.BytesIO(file_bytes))
    text_parts = []
    for para in doc.paragraphs:
        if para.text.strip():
            text_parts.append(para.text)
    return "\n".join(text_parts)


def parse_resume(file_bytes: bytes, filename: str) -> tuple[str, str]:
    """
    Parse a resume file and return (text, file_type).
    Supports PDF and DOCX.
    """
    if filename.lower().endswith(".pdf"):
        return parse_pdf(file_bytes), "pdf"
    elif filename.lower().endswith(".docx"):
        return parse_docx(file_bytes), "docx"
    else:
        raise ValueError(f"Unsupported file type: {filename}. Please upload PDF or DOCX.")
