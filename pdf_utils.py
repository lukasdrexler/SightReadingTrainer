import os
import sys

import fitz
from PIL import Image, ImageTk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def render_pdf(canvas, pdf_document):
    if pdf_document is None:
        return

    canvas.delete("all")

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    page = pdf_document[0]

    pdf_width = page.rect.width
    pdf_height = page.rect.height

    scale_x = canvas_width / pdf_width
    scale_y = canvas_height / pdf_height
    scale = min(scale_x, scale_y)

    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = ImageTk.PhotoImage(image=img)

    canvas.image = img
    canvas.create_image(0, 0, anchor="nw", image=img)


def extract_note_name(pdf_path):
    filename = os.path.basename(pdf_path)
    return os.path.splitext(filename)[0][:-1]


def build_pdf_file_list(all_notes):
    return [resource_path(os.path.join("pdfs", f"{notestr}.pdf")) for notestr in all_notes]