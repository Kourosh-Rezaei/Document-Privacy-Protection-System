from docx import Document


def read_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            print(para)
            full_text.append(para.text)

        return '\n'.join(full_text)

    except Exception as e:
        return f"error: {e}"
