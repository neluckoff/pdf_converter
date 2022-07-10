import os
from pdf2docx import Converter
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger
from art import tprint


def main():
    """Application menu"""
    print("Welcome to the menu!")
    print("[0] Call menu\n"
          "[1] Get information about a PDF file\n"
          "[2] Convert PDF to DOCX\n"
          "[3] Delete page from PDF\n"
          "[4] Select one page from PDF\n"
          "[5] Merge two PDF files\n"
          "[6] Encrypt PDF file\n"
          "[7] Decrypt PDF file")

    while True:
        choosing = int(input("\nChoose what you want to do: "))
        if choosing == 1:
            pdf_info()
        elif choosing == 2:
            pdf_to_docx()
        elif choosing == 3:
            pdf_delete_page()
        elif choosing == 4:
            pdf_select_page()
        elif choosing == 5:
            merge_pdf()
        elif choosing == 0:
            main()
        elif choosing == 6:
            encrypt_pdf()
        elif choosing == 7:
            decrypt_pdf()


def pdf_info():
    """Find out all the information about the PDF file"""
    path = input("[!] Path: ")
    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        file_name = os.path.splitext(os.path.basename(path))[0]
        with open(path, 'rb') as file:
            pdf = PdfReader(file)
            pages = pdf.getNumPages()
            pdf_i = pdf.getDocumentInfo()

        print(f'File: {file_name}')
        print(f'Author: {pdf_i.author}')
        print(f'Creator: {pdf_i.creator}')
        print(f'Title: {pdf_i.title}')
        print(f'Pages: {pages}')
    else:
        print("[INFO] File not found!")
        pdf_info()


def pdf_select_page():
    """Extract a page from a PDF file into a separate file"""
    path = input("[!] Path: ")
    file_name = os.path.splitext(os.path.basename(path))[0]
    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        pdf = PdfReader(path)
        pages = pdf.getNumPages()
        page = int(input(f"[!] Choose page (max {pages-1}): "))

        if 0 < page < pages:
            pdf_writer = PdfWriter()
            pdf_writer.addPage(pdf.getPage(page-1))

            output_filename = f'{file_name}_page_{page}.pdf'
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
            print(f'[+] Created: {output_filename}')
        else:
            print(f"[INFO] There are only {pages-1} pages in the file")
    else:
        print("[INFO] File not found!")
        pdf_select_page()


def merge_pdf():
    """Join two PDF files together"""
    path1 = input("[!] The file you want to paste into: ")
    path2 = input("[!] File to be inserted: ")
    if Path(path1).is_file() and (Path(path1).suffix == ".pdf" or Path(path1).suffix == ".PDF"):
        if Path(path2).is_file() and (Path(path2).suffix == ".pdf" or Path(path2).suffix == ".PDF"):
            file_name = os.path.splitext(os.path.basename(path1))[0]

            merge_file = PdfFileMerger()
            merge_file.append(path1, 'rb')
            merge_file.append(path2, 'rb')
            merge_file.write(f"{file_name}_merged.pdf")

            print(f'[+] Created: {file_name}_merged.pdf')
        else:
            print("[INFO] Second file not found!")
            merge_pdf()
    else:
        print("[INFO] First file not found!")
        merge_pdf()


def pdf_delete_page():
    """Delete page from PDF file"""
    path = input("[!] Path: ")
    file_name = os.path.splitext(os.path.basename(path))[0]
    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        pdf = PdfReader(path)
        pages = pdf.getNumPages()
        page_del = int(input(f"[!] Select page to delete (max {pages-1}): "))
        pdf_writer = PdfWriter()

        if 0 < page_del < pages:
            for page in range(pdf.getNumPages()):
                if page != page_del-1:
                    pdf_writer.addPage(pdf.getPage(page))

            output_filename = f'{file_name}_del_page_{page_del}.pdf'
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
            print(f'[+] Created: {output_filename}')
        else:
            print(f"[INFO] There are only {pages-1} pages in the file")
    else:
        print("[INFO] File not found!")
        merge_pdf()


def pdf_to_docx():
    """Convert PDF file to DOCX file"""
    pdf_file = input("[!] Path to PDF: ")
    if Path(pdf_file).is_file() and (Path(pdf_file).suffix == ".pdf" or Path(pdf_file).suffix == ".PDF"):
        docx_file = input("[!] Enter a name for the Word file: ") + '.docx'
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        print(f"[+] Created: {docx_file}")
    else:
        print("[INFO] File not found!")
        pdf_to_docx()


def encrypt_pdf():
    """Set password for PDF file"""
    path = input("[+] Path: ")
    file_writer = PdfWriter()
    file_name = os.path.splitext(os.path.basename(path))[0]
    result_file_name = f'{file_name}_encrypted.pdf'

    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        pas = input("[+] Password: ")
        file_reader = PdfReader(path)
        for page in range(file_reader.numPages):
            file_writer.addPage(file_reader.getPage(page))

        file_writer.encrypt(pas)
        with open(result_file_name, 'wb') as file:
            file_writer.write(file)

        print(f"[+] Created: {result_file_name}")
    else:
        print("[INFO] File not found!")
        encrypt_pdf()


def decrypt_pdf():
    """Remove password from PDF file"""
    path = input("[+] Path: ")
    file_writer = PdfWriter()
    file_name = os.path.splitext(os.path.basename(path))[0]
    result_file_name = f'{file_name}_decrypted.pdf'

    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        pas = input("[+] Password: ")
        file_reader = PdfReader(path)
        if file_reader.is_encrypted:
            file_reader.decrypt(pas)

        for page in range(file_reader.numPages):
            file_writer.addPage(file_reader.getPage(page))

        with open(result_file_name, 'wb') as file:
            file_writer.write(file)

        print(f"[+] Created: {result_file_name}")
    else:
        print("[INFO] File not found!")
        encrypt_pdf()


if __name__ == "__main__":
    tprint("PDF Converter")
    main()
