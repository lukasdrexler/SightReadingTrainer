import tkinter as tk
from tkinter import Canvas, Label

from config import NOTES_IN_OCTAVE

class StandardModeFrame(tk.Frame):
    def __init__(self, parent, on_note_click, on_show_random_pdf):
        super().__init__(parent)

        self.on_note_click = on_note_click
        self.on_show_random_pdf = on_show_random_pdf

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        for note_group in NOTES_IN_OCTAVE:
            group_frame = tk.Frame(self.button_frame)
            group_frame.pack(side=tk.LEFT, padx=2)

            for note in note_group:
                button = tk.Button(
                    group_frame,
                    text=note,
                    width=4,
                    command=lambda n=note: self.on_note_click(n)
                )
                button.pack()

        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.random_button = tk.Button(
            self,
            text="Show Random PDF",
            command=self.on_show_random_pdf
        )
        self.random_button.pack()

        self.answer_label = Label(self, text="", wraplength=600, justify="center")
        self.answer_label.pack(pady=10)

        self.feedback_label = Label(self, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=5)