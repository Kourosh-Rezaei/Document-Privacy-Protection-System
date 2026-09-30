from functions import (
    read_docx,
    read_txt,
    read_pdf,
    prepare_data,
    open_excel,
    remove_phone_numbers_docx,
    remove_phone_numbers_txt,
    remove_phone_numbers_pdf)


def main():
    file_path = r"D:\example.pdf"
    excel_path = r"D:\result.xlsx"
    output_file = r"D:\example_without_phone.pdf"

    if file_path.endswith(".txt"):  
        content = read_txt(file_path)

    elif file_path.endswith(".docx"):
        content = read_docx(file_path) 

    elif file_path.endswith(".pdf"):
        content = read_pdf(file_path)       

    print(10 * "-", "CONTENT", 10 * "-")
    print(content)

    data = prepare_data(content)

    print(10 * "-", "DATA", 10 * "-")
    print(data)

    open_excel(excel_path, data)

    if file_path.endswith(".txt"):
        remove_phone_numbers_txt(file_path, output_file)

    elif file_path.endswith(".docx"):
        remove_phone_numbers_docx(file_path, output_file)

    elif file_path.endswith(".pdf"):

        remove_phone_numbers_pdf(file_path,output_file) 
    
    print("\nThe program is finished.")

if __name__ == "__main__":
    main()
