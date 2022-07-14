from tkinter import *
from tkinter import filedialog as fd
from misc.pdf_work import choose_funct
import tkinter.ttk as ttk
from misc.image_work import image_in_pdf

option_list = [
    "Get information about a PDF file",
    "Convert PDF to DOCX",
    "Delete page from PDF",
    "Select one page from PDF",
    "Merge two PDF files",
    "Encrypt PDF file",
    "Decrypt PDF file"
]


class GUI:
    def get_images(self):
        self.files = fd.askopenfilenames(parent=self.app, title='Choose a file')

    def choose_directory(self, var):
        self.directory_save = fd.askdirectory()
        var.set(self.directory_save)

    def __init__(self):
        self.directory_save = None
        self.files = None
        self.app = Tk()

        self.app.title("PDF Converter")
        self.app.geometry('740x350')

        x = (self.app.winfo_screenwidth() - self.app.winfo_reqwidth()) / 3
        y = (self.app.winfo_screenheight() - self.app.winfo_reqheight()) / 3
        self.app.wm_geometry("+%d+%d" % (x, y))

        # Create tabs
        tab_control = ttk.Notebook(self.app)
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab1, text="PDF")
        tab_control.add(tab2, text="IMAGE")

        var3 = StringVar(self.app)

        # Settings 1st page
        Label(tab1, text="PDF Converter", font=('bold', 14)).place(x=20, y=5)
        tkvar = StringVar(tab1)
        tkvar.set(option_list[0])
        var = StringVar(tab1)

        Label(tab1, text="File Path", font=('bold', 10)).place(x=20, y=40)
        Entry(tab1, textvariable=var).place(y=40, x=100)
        Button(tab1, text="Browse", command=lambda: var.set(fd.askopenfilename())).place(y=36, x=220)

        OptionMenu(tab1, tkvar, *option_list).place(x=40, y=115)

        submit_button = Button(tab1, text='Get Started', command=lambda: choose_funct(tkvar.get(), var.get(),
                                                                                      text, self.directory_save))
        submit_button.place(x=200, y=158)

        Label(tab1, text="Save folder ", font=('bold', 10)).place(x=20, y=75)
        Entry(tab1, textvariable=var3).place(x=100, y=75)
        Button(tab1, text="Browse", command=lambda: self.choose_directory(var3)).place(x=220, y=71)

        # Setting 2nd page
        Label(tab2, text="Image Converter", font=('bold', 14)).place(x=20, y=5)
        var2 = StringVar(tab2)

        button = Button(tab2, text="Choose Images", command=lambda: self.get_images())
        button.place(x=20, y=120)

        button2 = Button(tab2, text="Start Converting", command=lambda: image_in_pdf(self.files, var2.get(),
                                                                                     text, var3.get()))
        button2.place(x=180, y=120)

        Label(tab2, text="Enter Author Name: ", font=('bold', 10)).place(x=20, y=40)
        Entry(tab2, textvariable=var2).place(y=40, x=150)
        Label(tab2, text="* Just select all images", font=("default", 8)).place(x=20, y=145)

        Label(tab2, text="Save folder ", font=('bold', 10)).place(x=20, y=80)
        Entry(tab2, textvariable=var3).place(x=100, y=80)
        Button(tab2, text="Browse", command=lambda: self.choose_directory(var3)).place(x=224, y=76)

        # All App
        text = Text(self.app)
        text.place(x=310, y=30, height=310, width=420)
        Label(self.app, text="https://github.com/neluckoff/pdf_converter").place(x=5, y=320)

        tab_control.pack(expand=1, fill='both')

    def start(self):
        self.app.mainloop()
