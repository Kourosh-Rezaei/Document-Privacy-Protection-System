from docx import Document
import re
import os
from openpyxl import load_workbook, Workbook
import pymupdf



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
    

def read_txt(file_path: str) -> str:
    """
    Extract the content of the TXT file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        return f"error: {e}"


def read_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    try:
        document = pymupdf.open(file_path)

        full_text = []

        for page in document:
            full_text.append(page.get_text())

        document.close()

        return "\n".join(full_text)

    except Exception as e:
        return f"error: {e}"
    
    
def prepare_data(text: str) -> list[dict[str, str]]:
    """
    Find all phone numbers and names and at them to a list of dictionaries
    """
    data = []
    pattern = r'([A-Za-z]+(?:\s+[A-Za-z]+)*)\s+((?<!\w)(?:\+|00)?(?:\d{1,3}[\s-]?)?(?:\d{2,4}[\s-]?){2,4}\d(?!\w))'
    matches = re.findall(pattern, text)

    for name, phone in matches:
        data.append({
            "name": name.strip(),
            "Phone Number": phone.strip()
        })

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

    except Exception as e:
        return f"error: {e}"


def remove_phone_numbers_pdf(input_file: str, output_file: str):
    """
    Remove phone numbers from a PDF file
    and save the result as a new PDF file.
    """

    pattern = r'(?<!\w)(?:\+\d{1,3}[\s-]?)?(?:\d{3}[\s-]?\d{3}[\s-]?\d{4}|\d{10})(?!\w)'

    try:

        document = pymupdf.open(input_file)

        for page in document:

            words = page.get_text("words")

            words.sort(
                key=lambda word: (
                    word[5],
                    word[6],
                    word[7]
                )
            )

            redactions = []

            for i in range(len(words)):

                selected_words = []

                for j in range(i, min(i + 5, len(words))):

                    selected_words.append(words[j])

                    text = " ".join(
                        word[4]
                        for word in selected_words
                    )

                    matches = re.finditer(
                        pattern,
                        text
                    )

                    for match in matches:

                        phone = match.group()

                        digits = re.sub(
                            r"\D",
                            "",
                            phone
                        )

                        if 10 <= len(digits) <= 15:

                            match_start = match.start()
                            match_end = match.end()

                            current_position = 0

                            for word in selected_words:

                                word_text = word[4]

                                word_start = current_position
                                word_end = current_position + len(word_text)

                                if (
                                    word_end > match_start
                                    and word_start < match_end
                                ):

                                    rectangle = pymupdf.Rect(
                                        word[0],
                                        word[1],
                                        word[2],
                                        word[3]
                                    )

                                    redactions.append(
                                        rectangle
                                    )

                                current_position = word_end + 1

                    if list(
                        re.finditer(
                            pattern,
                            text
                        )
                    ):
                        break

            for rectangle in redactions:

                page.add_redact_annot(
                    rectangle,
                    fill=(1, 1, 1)
                )

            page.apply_redactions()

        document.save(output_file)

        document.close()

    except Exception as e:

        return f"error: {e}"