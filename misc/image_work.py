from PIL import Image
from pathlib import Path
from tkinter import messagebox as mb
from misc.text_wrapper import TextWrapper


def image_in_pdf(image_list, author, text, save_path):
    """Convert all images in pdf file"""
    if image_list is not None:
        if save_path is not None:
            image_arr = []
            for path in image_list:
                if Path(path).suffix == ".png" or Path(path).suffix == ".jpg" or Path(path).suffix == ".jpeg":
                    im1 = (Image.open(path)).convert('RGB')
                    image_arr.append(im1)
                else:
                    mb.showwarning(f"WARNING!", f"The file is not a photo!\n\n{path}")

            image_arr[0].save(f'{save_path}/Images.pdf', save_all=True,
                              append_images=image_arr[1:], creator="github.com/neluckoff/pdf_converter",
                              title="Images in PDF file", author=str(author))
            print('[+] Created: Images.pdf', file=TextWrapper(text))
        else:
            mb.showerror("ERROR", "Specify the path to save the file!")
    else:
        mb.showwarning(f"WARNING!", f"You have not selected any images")
