import PyPDF2
import io
import pdfplumber

# Configure logging
import logging
logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        logger.info("Extracting text from PDF using pdfplumber.")
        text = ""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    logger.warning(f"No extractable text on page {i}")
        if not text.strip():
            raise ValueError("No extractable text found in the PDF.")
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {str(e)}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
