from tkinter import *


class TextWrapper:
    """Class for console output to the application text window"""
    text_field: Text

    def __init__(self, text_field: Text):
        self.text_field = text_field

    def write(self, text: str):
        self.text_field.insert(END, text)

    def flush(self):
        self.text_field.update()

