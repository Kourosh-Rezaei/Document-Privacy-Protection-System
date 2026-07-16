# Document Privacy Protection System

A Python program for processing Microsoft Word documents by extracting names and phone numbers into an Excel file while generating a new version of the document with phone numbers removed.



## Features

- Read text from Microsoft Word (`.docx`) files
- Extract names and phone numbers using Regular Expressions
- Create or update an Excel workbook with extracted data
- Remove phone numbers from the original document
- Generate a new DOCX file without phone numbers

## Requirements

- Python 3.x
- python-docx
- openpyxl

Install the required packages:

```bash
pip install python-docx openpyxl
```

## Usage

1. Open `control.py`.
2. Set the paths for the input document, output Excel file, and output document.

```python
file_path = r"D:\example.docx"
excel_path = r"D:\result.xlsx"
output_file = r"D:\example_without_phone.docx"
```

3. Run the project.

```bash
python control.py
```

## Example

### Input

```
John Smith, +1 234 567 8910

Alice Brown, +44 123 456 7890
```

### Excel Output

| Name | Phone Number |
|------|--------------|
| John Smith | +1 234 567 8910 |
| Alice Brown | +44 123 456 7890 |

### Output Document

```
John Smith,

Alice Brown,
```

## Future Improvements

- [ ] support other formats
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

[Kourosh Rezaei (Developer)](https://github.com/Kourosh-Rezaei)

[Daniyal Iran Mehr (Advisor & Manager)](https://github.com/Daniyaliranmehr)