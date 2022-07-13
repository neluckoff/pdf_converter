from tkinter import *
from tkinter import filedialog as fd
from misc.pdf_work import choose_funct

OptionList = [
        "Get information about a PDF file",
        "Convert PDF to DOCX",
        "Delete page from PDF",
        "Select one page from PDF",
        "Merge two PDF files",
        "Encrypt PDF file",
        "Decrypt PDF file"
    ]


def start():
    app = Tk()

    app.title("PDF Converter")
    app.geometry('740x350')

    x = (app.winfo_screenwidth() - app.winfo_reqwidth()) / 3
    y = (app.winfo_screenheight() - app.winfo_reqheight()) / 3
    app.wm_geometry("+%d+%d" % (x, y))

    tkvar = StringVar(app)
    tkvar.set(OptionList[0])
    var = StringVar(app)

    w = Label(app, text="File Path:", font=('bold', 14), pady=20, padx=20)
    w.grid(row=0, column=0)
    e = Entry(app, textvariable=var)
    e.grid(row=0, column=1, columnspan=2)
    b = Button(app, text="Browse", command=lambda: var.set(fd.askopenfilename()))
    b.grid(row=0, column=3, columnspan=2)

    OptionMenu(app, tkvar, *OptionList).place(x=45, y=70)
    text = Text(app)
    text.place(x=310, y=10, height=310, width=420)

    submit_button = Button(app, text='Submit', command=lambda: choose_funct(tkvar.get(), var.get(), text), width=20,
                           height=3)
    submit_button.place(x=75, y=120)

    app.mainloop()