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
        tkvar = StringVar(tab1)
        tkvar.set(option_list[0])
        var = StringVar(tab1)

        w = Label(tab1, text="File Path:", font=('bold', 10), pady=20, padx=20)
        w.grid(row=0, column=0)
        e = Entry(tab1, textvariable=var)
        e.grid(row=0, column=1, columnspan=2)
        b = Button(tab1, text="Browse", command=lambda: var.set(fd.askopenfilename()))
        b.grid(row=0, column=3, columnspan=2)

        OptionMenu(tab1, tkvar, *option_list).place(x=20, y=95)

        submit_button = Button(tab1, text='Get Started', command=lambda: choose_funct(tkvar.get(), var.get(),
                                                                                 text, self.directory_save))
        submit_button.place(x=235, y=98)

        Label(tab1, text="Save folder ", font=('bold', 10)).place(x=20, y=55)
        Entry(tab1, textvariable=var3).place(x=100, y=55)
        Button(tab1, text="Browse", command=lambda: self.choose_directory(var3)).place(x=225, y=51)

        # Setting 2nd page
        var2 = StringVar(tab2)

        button = Button(tab2, text="Choose Images", command=lambda: self.get_images())
        button.place(x=20, y=60)

        button2 = Button(tab2, text="Start Converting", command=lambda: image_in_pdf(self.files, var2.get(), text))
        button2.place(x=180, y=60)

        Label(tab2, text="Enter Author Name: ", pady=20, padx=20, font=('bold', 10)).grid(row=0, column=0)
        Entry(tab2, textvariable=var2).grid(row=0, column=1)
        Label(tab2, text="* Just select all images", font=("default", 8)).place(x=20, y=85)

        Label(tab2, text="Save folder ").place(x=20, y=120)
        Entry(tab2, textvariable=var3).place(x=90, y=120)
        Button(tab2, text="Browse", command=lambda: self.choose_directory(var3)).place(x=214, y=116)

        # All App
        text = Text(self.app)
        text.place(x=310, y=30, height=310, width=420)

        tab_control.pack(expand=1, fill='both')

    def start(self):
        self.app.mainloop()
