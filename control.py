from functions import read_docx, prepare_data, open_excel, remove_phone_numbers


def main():
    file_path = r"D:\example.docx"
    excel_path = r"D:\result.xlsx"
    output_file = r"D:\example_without_phone.docx"

    content = read_docx(file_path)

    print("--- The content of DOCX file ---")

    print(content)

    print("-------------------------------")

    data = prepare_data(content)

    print(data)

    open_excel(excel_path, data)
    
    remove_phone_numbers(file_path, output_file)

    print("Phone numbers removed successfully.")

if __name__ == "__main__":
    main()
