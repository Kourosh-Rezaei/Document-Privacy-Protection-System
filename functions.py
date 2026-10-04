import os
import re

import pymupdf
from docx import Document
from openpyxl import Workbook, load_workbook


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

    except Exception as e:  # noqa: BLE001
        return f"error: {e}"
    

def read_txt(file_path: str) -> str:
    """
    Extract the content of the TXT file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def read_pdf(file_path: str) -> str:
    """
    Extract the content of the PDF file.
    """
    try:
        document = pymupdf.open(file_path)

        full_text = []

        for page in document:
            full_text.append(page.get_text())

        document.close()

        return "\n".join(full_text)

    except Exception as e:  # noqa: BLE001
        return f"error: {e}"
    
    
def prepare_data(text: str) -> list[dict[str, str]]:
    """
    Find all phone numbers and names and add them to a list of dictionaries.
    """

    data = []

    pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:(\+\d{1,3})\s*)?(\d{3}[\s-]?\d{3}[\s-]?\d{4}|\d{10})\b'

    matches = re.findall(pattern, text)

    for name, country_code, phone in matches:

        if country_code:
            phone = country_code + " " + phone

        data.append({
            "name": name.strip(),
            "Phone Number": phone.strip()})

    return data


def open_excel(excel_path: str, data: list):
    """
    Open an Excel file and write data to it.
    """

    if os.path.exists(excel_path):
        workbook = load_workbook(excel_path)
        sheet = workbook.active
    else:
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Name", "Phone Number"])

    for item in data:
        sheet.append([item["name"], item["Phone Number"]])

    workbook.save(excel_path)


def remove_phone_numbers_docx(input_file: str, output_file: str):
    """
    Remove all phone numbers from a DOCX file.
    """
    pattern = r'(?<!\w)(?:\+|00)?(?:\d{1,3}[\s-]?)?(?:\d{2,4}[\s-]?){2,4}\d(?!\w)'
    doc = Document(input_file)

    def replace_phone(match):
        phone = match.group()
        digits = re.sub(r"\D", "", phone)

        if 10 <= len(digits) <= 15:
            return ""
        return phone

    for para in doc.paragraphs:
        para.text = re.sub(pattern, replace_phone, para.text)

    doc.save(output_file)


def remove_phone_numbers_txt(input_file: str, output_file: str):
    """
    Remove all phone numbers from a TXT file.
    """

    pattern = r'(?<!\w)(?:\+|00)?(?:\d{1,3}[\s-]?)?(?:\d{2,4}[\s-]?){2,4}\d(?!\w)'

    try:
        
        text = read_txt(input_file)

        def replace_phone(match):
            phone = match.group()

            digits = re.sub(r"\D", "", phone)

            if 10 <= len(digits) <= 15:
                return ""

            return phone

        text = re.sub(pattern, replace_phone, text)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)

    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def remove_phone_numbers_pdf(input_file: str, output_file: str):
    """
    Remove all phone numbers from a PDF file.
    """

    pattern = r'(?<!\w)(?:\+\d{1,3}\s*)?(?:\d{3}[\s-]?\d{3}[\s-]?\d{4}|\d{10})(?!\w)'

    try:
        text = read_pdf(input_file)

        text = re.sub(pattern, "", text)

        text = re.sub(r' +([.,])', r'\1', text)

        text = re.sub(r'\n\s*([.,])', r'\1', text)

        text = re.sub(r'([.,])([A-Za-z])', r'\1 \2', text)

        text = re.sub(r' {2,}', ' ', text)

        create_pdf(text, output_file)

    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def create_pdf(text: str, output_file: str):
    """
    Create a new PDF file from text.
    """

    document = pymupdf.open()

    page = document.new_page()

    page.insert_textbox(
        pymupdf.Rect(50, 50, 550, 800),
        text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0))

    document.save(output_file)
    document.close()
