import io
from pypdf import PdfReader
from docx import Document


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return _extract_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        return _extract_docx(file_bytes)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")


def _extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def _extract_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join(para.text for para in doc.paragraphs)
    return text.strip()