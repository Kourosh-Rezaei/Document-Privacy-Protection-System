from docx import Document
import re


def read_docx(file_path: str) -> str:
    """
    Extract the content of the DOCX file
    """
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)

        return '\n'.join(full_text)

    except Exception as e:
        return f"error: {e}"


def prepare_data(text: str) -> str:
    """
    Find all phone numbers and names and at them to a list of dictionaries
    """
    data = []

    pattern = r'([A-Za-z\s]+)\s+(\+\d{1,3}\s?\d{3}\s?\d{3}\s?\d{4})'

    matches = re.findall(pattern, text)

    for name, phone in matches:
        data.append({
            "name": name.strip(),
            "Phone Number": phone.strip()
        })

    return data
