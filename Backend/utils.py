import PyPDF2
import io

# Configure logging
import logging
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        logger.info("Extracting text from PDF.")
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        logger.info("Text extraction from PDF completed.")
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {str(e)}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
