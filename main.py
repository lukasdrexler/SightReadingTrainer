import tkinter as tk
from tkinter import Canvas, Label
import random
import fitz  # PyMuPDF
from PIL import Image, ImageTk

all_notes = ['F3', 'F#3',
         'Gb3', 'G3', 'G#3', 'Ab3', 'A3', 'A#3', 'Bb3', 'B3','C4', 'C#4', 'Db4', 'D4', 'D#4', 'Eb4', 'E4', 'F4', 'F#4',
         'Gb4', 'G4', 'G#4', 'Ab4', 'A4', 'A#4', 'Bb4', 'B4', 'C5', 'C#5', 'Db5', 'D5', 'D#5', 'Eb5', 'E5', 'F5', 'F#5',
         'Gb5', 'G5', 'G#5', 'Ab5', 'A5', 'A#5', 'Bb5', 'B5', 'C6']


# each note for which we want a button
notes_in_octave = [
    ("C",),
    ("C#", "Db"),
    ("D",),
    ("D#", "Eb"),
    ("E",),
    ("F",),
    ("F#", "Gb"),
    ("G",),
    ("G#", "Ab"),
    ("A",),
    ("A#", "Bb"),
    ("B",),
]


# Function to render a PDF page to a Tkinter canvas with a scale factor to fill the canvas
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



# Function to update canvas size and render PDF on window resize
def on_resize(event):
    if current_pdf is None:
        return
    render_pdf(canvas, current_pdf)



# Function to show the answer after a set amount of time
def show_answer():
    if current_answer is not None:
        answer_label.config(text=current_answer)

def check_answer(user_answer):
    global answered

    if current_answer is None or answered:
        return

    answered = True

    if user_answer == current_answer:
        feedback_label.config(text="Correct ✅")
    else:
        feedback_label.config(
            text=f"Incorrect ❌ (Correct: {current_answer})"
        )

def on_note_button_clicked(note_name):
    check_answer(note_name)


# Function to show a random PDF page
def show_random_pdf():
    global current_pdf, current_answer, answered

    answered = False
    pdf_path = random.choice(pdf_files)
    current_pdf = fitz.open(pdf_path)

    current_answer = pdf_path.split('/')[1].split('.')[0][:-1]
    # Initial render of PDF
    render_pdf(canvas, current_pdf)

    # Reset answer label text
    feedback_label.config(text="")

# Main application setup
app = tk.Tk()
app.title("Sight Reading Trainer")

button_frame = tk.Frame(app)
button_frame.pack(pady=5)

for note_group in notes_in_octave:
    group_frame = tk.Frame(button_frame)
    group_frame.pack(side=tk.LEFT, padx=2)

    for note in note_group:
        b = tk.Button(
            group_frame,
            text=note,
            width=4,
            command=lambda n=note: on_note_button_clicked(n)
        )
        b.pack()

# Canvas setup with resizing behavior
canvas = Canvas(app, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Bind window resize event to on_resize function
app.bind("<Configure>", on_resize)

# Button to show a random PDF
button = tk.Button(app, text="Show Random PDF", command=show_random_pdf)
button.pack()

# Label to display the answer
answer_label = Label(app, text="", wraplength=600, justify="center")
answer_label.pack(pady=10)

feedback_label = Label(app, text="", font=("Arial", 14))
feedback_label.pack(pady=5)


# List of pre-rendered PDF files (change paths to your PDF files)
pdf_files = ['pdfs/' + notestr + '.pdf' for notestr in all_notes]

# Variables to track currently displayed PDF and page
current_pdf = None

app.mainloop()