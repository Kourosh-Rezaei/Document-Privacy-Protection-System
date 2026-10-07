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

## Requirements

- Python 3.10 or later
- `python-docx` 1.2.0
- `openpyxl` 3.1.5
- `PyMuPDF` 1.28.2

Install the dependencies:

```bash
pip install python-docx openpyxl pymupdf
```

## Project Structure

```text
Document-Privacy-Protection-System/
├── control.py
├── functions.py
├── README.md
└── requirements.txt
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

## Main Functions

The functions are defined in `functions.py`.

| Function | Purpose |
| --- | --- |
| `read_docx(file_path)` | Extracts text from a DOCX file |
| `read_txt(file_path)` | Reads a TXT file using UTF-8 encoding |
| `read_pdf(file_path)` | Extracts text from a PDF file |
| `prepare_data(text)` | Finds matching names and phone numbers and returns a list of dictionaries |
| `open_excel(excel_path, data)` | Creates or updates an Excel workbook with extracted records |
| `remove_phone_numbers_docx(input_file, output_file)` | Removes matching phone numbers from a DOCX file |
| `remove_phone_numbers_txt(input_file, output_file)` | Removes matching phone numbers from a TXT file |
| `remove_phone_numbers_pdf(input_file, output_file)` | Removes matching phone numbers from extracted PDF text and writes a new PDF |
| `create_pdf(text, output_file)` | Creates a PDF file from text |

## Unit Tests

Unit tests can be written with `pytest`. If the test file is named `test_functions.py`, install pytest:

```bash
pip install pytest
```

Run the tests from the project directory:

```bash
pytest
```

Tests should cover successful processing and relevant edge cases for each function, including missing or invalid input files, text with no matching phone numbers, and checking that names remain after phone numbers are removed.

## Notes and Limitations

- The name and phone-number extraction in `prepare_data()` uses a Regular Expression. It does not identify every possible name or international phone-number format.
- The current PDF removal function extracts the PDF text, removes matching phone-number patterns, and creates a new PDF from that text. It does **not** edit the original PDF in place, and the new PDF may not preserve the original layout, fonts, images, or other formatting.
- The phone-number patterns used for PDF processing and DOCX/TXT processing are not identical, so supported number formats may differ by file type.
- The program writes a separate output file; it does not overwrite the input document when different paths are provided.
- When using an existing Excel workbook, records are appended to its active sheet.

## Future Improvements

- [x] support TXT format
- [x] support PDF format
- [ ] Remove specific phone numbers
- [ ] Remove other contact addresses
- [ ] Process multiple documents at a time
- [ ] Add unit tests
- [ ] Add Docker support
- [ ] Detect phone numbers from multiple international formats
- [ ] Encrypt exported Excel files
- [ ] Validate and normalize phone numbers automatically
- [ ] Delete communication channels associated with a specific person
- [ ] Django integration
- [ ] Telegram bot development

## Team

- [Kourosh Rezaei](https://github.com/Kourosh-Rezaei) — Developer
- [Daniyal Iran Mehr](https://github.com/Daniyaliranmehr) — Advisor & Manager
