import os
from pdf2docx import Converter
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from misc.text_wrapper import TextWrapper


def choose_funct(choosing, path, text, save_path):
    """Choosing menu"""
    if choosing == "Get information about a PDF file":
        pdf_info(path, text)
    elif save_path is not None:
        if choosing == "Convert PDF to DOCX":
            pdf_to_docx(path, text, save_path)
        elif choosing == "Delete page from PDF":
            new_app = Tk()
            new_app.title("Delete page from PDF")
            new_app.geometry('220x100')
            x = (new_app.winfo_screenwidth() - new_app.winfo_reqwidth()) / 2
            y = (new_app.winfo_screenheight() - new_app.winfo_reqheight()) / 2
            new_app.wm_geometry("+%d+%d" % (x, y))
            var1 = StringVar(new_app)
            Label(new_app, text="Enter page to delete", font=('bold', 10)).place(x=10, y=5)
            Entry(new_app, textvariable=var1).place(x=12, y=35)
            Button(new_app, text='Delete',
                   command=lambda: pdf_delete_page(path, int(var1.get()),
                                                   new_app, text, save_path)).place(y=31, x=120)
            new_app.mainloop()
        elif choosing == "Select one page from PDF":
            new_app = Tk()
            new_app.title("Select one page from PDF")
            new_app.geometry('220x100')
            x = (new_app.winfo_screenwidth() - new_app.winfo_reqwidth()) / 2
            y = (new_app.winfo_screenheight() - new_app.winfo_reqheight()) / 2
            new_app.wm_geometry("+%d+%d" % (x, y))
            var1 = StringVar(new_app)
            Label(new_app, text="Page to save as a separate PDF", font=('bold', 10)).place(x=10, y=5)
            Entry(new_app, textvariable=var1).place(x=12, y=35)
            Button(new_app, text='Select',
                   command=lambda: pdf_select_page(path, int(var1.get()),
                                                   new_app, text, save_path)).place(y=31, x=120)
            new_app.mainloop()
        elif choosing == "Merge two PDF files":
            new_file = fd.askopenfilename()
            merge_pdf(path, new_file, text, save_path)
        elif choosing == "Encrypt PDF file":
            new_app = Tk()
            new_app.title("Encrypt PDF file")
            new_app.geometry('220x100')
            x = (new_app.winfo_screenwidth() - new_app.winfo_reqwidth()) / 2
            y = (new_app.winfo_screenheight() - new_app.winfo_reqheight()) / 2
            new_app.wm_geometry("+%d+%d" % (x, y))
            var1 = StringVar(new_app)
            Label(new_app, text="Enter password to encrypt PDF file", font=('bold', 10)).place(x=10, y=5)
            Entry(new_app, textvariable=var1).place(x=12, y=35)
            Button(new_app, text='Encrypt',
                   command=lambda: encrypt_pdf(path, var1.get(),
                                               new_app, text, save_path)).place(y=31, x=120)
            new_app.mainloop()
        elif choosing == "Decrypt PDF file":
            new_app = Tk()
            new_app.title("Decrypt PDF file")
            new_app.geometry('220x100')
            x = (new_app.winfo_screenwidth() - new_app.winfo_reqwidth()) / 2
            y = (new_app.winfo_screenheight() - new_app.winfo_reqheight()) / 2
            new_app.wm_geometry("+%d+%d" % (x, y))
            var1 = StringVar(new_app)
            Label(new_app, text="Enter password to decrypt PDF file", font=('bold', 10)).place(x=10, y=5)
            Entry(new_app, textvariable=var1).place(x=12, y=35)
            Button(new_app, text='Decrypt',
                   command=lambda: decrypt_pdf(path, var1.get(),
                                               new_app, text, save_path)).place(y=31, x=120)
            new_app.mainloop()
    else:
        mb.showerror("ERROR", "Specify the path to save the file!")


def pdf_info(path, text):
    """Find out all the information about the PDF file"""
    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        file_name = os.path.splitext(os.path.basename(path))[0]
        try:
            with open(path, 'rb') as file:
                pdf = PdfReader(file)
                pages = pdf.getNumPages()
                pdf_i = pdf.getDocumentInfo()

            print(f'File name: {file_name}', file=TextWrapper(text))
            print(f'Author: {pdf_i.author}', file=TextWrapper(text))
            print(f'Creator: {pdf_i.creator}', file=TextWrapper(text))
            print(f'Title: {pdf_i.title}', file=TextWrapper(text))
            print(f'Pages: {pages}', file=TextWrapper(text))
        except Exception as ex:
            mb.showerror("ERROR", f'{ex}')
    else:
        mb.showinfo("INFO", "File not found!")


def pdf_select_page(path, page, app, text, save_path):
    """Extract a page from a PDF file into a separate file"""
    app.destroy()
    file_name = os.path.splitext(os.path.basename(path))[0]
    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        try:
            pdf = PdfReader(path)
            pages = pdf.getNumPages()

            if 0 < page < pages:
                pdf_writer = PdfWriter()
                pdf_writer.addPage(pdf.getPage(page - 1))

                output_filename = f'{file_name}_page_{page}.pdf'
                with open(f'{save_path}/{output_filename}', 'wb') as out:
                    pdf_writer.write(out)
                print(f'[+] Created: {output_filename}', file=TextWrapper(text))
            else:
                mb.showinfo('INFO', f"[INFO] There are only {pages - 1} pages in the file")
        except Exception as ex:
            mb.showerror("ERROR", f'{ex}')
    else:
        mb.showerror("INFO", "File not found!")


def merge_pdf(path1, path2, text, save_path):
    """Join two PDF files together"""
    if Path(path1).is_file() and (Path(path1).suffix == ".pdf" or Path(path1).suffix == ".PDF"):
        if Path(path2).is_file() and (Path(path2).suffix == ".pdf" or Path(path2).suffix == ".PDF"):
            try:
                file_name = os.path.splitext(os.path.basename(path1))[0]

                merge_file = PdfFileMerger()
                merge_file.append(path1, 'rb')
                merge_file.append(path2, 'rb')
                output_filename = f"{file_name}_merged.pdf"
                with open(f'{save_path}/{output_filename}', 'wb') as out:
                    merge_file.write(out)

                print(f'[+] Created: {file_name}_merged.pdf', file=TextWrapper(text))
            except Exception as ex:
                mb.showerror("ERROR", f'{ex}')
        else:
            mb.showerror("INFO", "Second file not found!")
    else:
        mb.showerror("INFO", "First file not found!")


def pdf_delete_page(path, page_del, app, text, save_path):
    """Delete page from PDF file"""
    app.destroy()
    file_name = os.path.splitext(os.path.basename(path))[0]
    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        try:
            pdf = PdfReader(path)
            pages = pdf.getNumPages()
            pdf_writer = PdfWriter()

            if 0 < page_del < pages:
                for page in range(pdf.getNumPages()):
                    if page != page_del - 1:
                        pdf_writer.addPage(pdf.getPage(page))

                output_filename = f'{file_name}_del_page_{page_del}.pdf'
                with open(f'{save_path}/{output_filename}', 'wb') as out:
                    pdf_writer.write(out)
                print(f'[+] Created: {output_filename}', file=TextWrapper(text))
            else:
                print(f"[INFO] There are only {pages - 1} pages in the file", file=TextWrapper(text))
        except Exception as ex:
            mb.showerror("ERROR", f'{ex}')
    else:
        mb.showerror("INFO", "File not found!")


def pdf_to_docx(path, text, save_path):
    """Convert PDF file to DOCX file"""
    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        try:
            docx_file = os.path.splitext(os.path.basename(path))[0] + '.docx'
            cv = Converter(path)
            cv.convert(f'{save_path}/{docx_file}', start=0, end=None)
            cv.close()
            print(f"[+] Created: {docx_file}", file=TextWrapper(text))
        except Exception as ex:
            mb.showerror("ERROR", f'File has not been decrypted')
    else:
        mb.showerror("INFO", "File not found!")


def encrypt_pdf(path, pas, app, text, save_path):
    """Set password for PDF file"""
    app.destroy()
    file_writer = PdfWriter()
    file_name = os.path.splitext(os.path.basename(path))[0]
    result_file_name = f'{file_name}_encrypted.pdf'

    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        file_reader = PdfReader(path)
        for page in range(file_reader.numPages):
            file_writer.addPage(file_reader.getPage(page))

        file_writer.encrypt(str(pas))
        with open(f'{save_path}/{result_file_name}', 'wb') as file:
            file_writer.write(file)

        print(f"[+] Created: {result_file_name}", file=TextWrapper(text))
    else:
        mb.showerror("INFO", "File not found!")


def decrypt_pdf(path, pas, app, text, save_path):
    """Remove password from PDF file"""
    app.destroy()
    file_writer = PdfWriter()
    file_name = os.path.splitext(os.path.basename(path))[0]
    result_file_name = f'{file_name}_decrypted.pdf'

    if Path(path).is_file() and (Path(path).suffix == ".pdf" or Path(path).suffix == ".PDF"):
        file_reader = PdfReader(path)
        if file_reader.is_encrypted:
            try:
                file_reader.decrypt(str(pas))

                for page in range(file_reader.numPages):
                    file_writer.addPage(file_reader.getPage(page))

                with open(f'{save_path}/{result_file_name}', 'wb') as file:
                    file_writer.write(file)

                print(f"[+] Created: {result_file_name}", file=TextWrapper(text))
            except Exception as ex:
                mb.showerror("ERROR", f"{ex}\nCheck your password and try again")
    else:
        mb.showerror("INFO", "File not found!")
