# Document Privacy Protection System

A Python application that extracts names and phone numbers from documents, saves the extracted information in an Excel file, and creates a new document with phone numbers removed.

The project currently supports **DOCX**, **TXT**, and **PDF** files.

## Features

- Read text from Microsoft Word (`.docx`) files
- Read text from plain text (`.txt`) files
- Read text from PDF (`.pdf`) files
- Extract names and phone numbers using Regular Expressions
- Save extracted names and phone numbers in an Excel (`.xlsx`) file
- Create a new DOCX file with phone numbers removed
- Create a new TXT file with phone numbers removed
- Create a new PDF file with phone numbers removed
- Append extracted records to an existing Excel workbook
- User-interface (Telegram bot on web)

## Requirements

- Python 3.10 or later
- `python-docx` 1.2.0
- `openpyxl` 3.1.5
- `PyMuPDF` 1.28.2
- `python-dotenv` ==  1.2.3
- `python-telegram-bot` == 22.8
- `httpx` == 0.28.1
- `Flask` == 3.1.2

Install the dependencies:

```bash
pip install python-docx openpyxl pymupdf
```

## Usage

1. Open `control.py`.
2. Set the paths for the input document, Excel file, and output document.
3. Run `control.py`.

For example, to process a TXT file:

```python
file_path = r"D:\example.txt"
excel_path = r"D:\result.xlsx"
output_file = r"D:\example_without_phone.txt"
```

Run the program from the project directory:

```bash
python control.py
```

Change the file paths and extensions to match the document you want to process.

### Supported input and output formats

| Input format | Text extraction | Output without phone numbers |
| --- | --- | --- |
| DOCX (`.docx`) | `read_docx()` | DOCX |
| TXT (`.txt`) | `read_txt()` | TXT |
| PDF (`.pdf`) | `read_pdf()` | PDF |

The input extension is used by `control.py` to choose the corresponding functions. The output file extension should match the input format.

## How It Works

1. **Read the document:** The program extracts text from the input DOCX, TXT, or PDF file.
2. **Find contact details:** `prepare_data()` searches the extracted text for names and phone numbers.
3. **Save the data:** `open_excel()` creates an Excel workbook if one does not exist, or appends records to the active sheet of an existing workbook.
4. **Remove phone numbers:** The program creates a separate output file with phone numbers removed. The original input file is not overwritten.

## Example

### Input

```text
John Smith, +1 234 567 8910
Alice Brown, +44 123 456 7890
```

### Excel output

| Name | Phone Number |
| --- | --- |
| John Smith | +1 234 567 8910 |
| Alice Brown | +44 123 456 7890 |

### Output document

```text
John Smith,
Alice Brown,
```

## Future Improvements

- [x] support TXT format
- [x] support PDF format
- [x] Add unit tests
- [x] Detect phone numbers from multiple international formats
- [x] website development
- [x] Telegram bot development

## Team

- [Kourosh Rezaei](https://github.com/Kourosh-Rezaei) — Developer
- [Daniyal Iran Mehr](https://github.com/Daniyaliranmehr) — Advisor & Manager
