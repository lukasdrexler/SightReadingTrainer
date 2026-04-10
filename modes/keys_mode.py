import tkinter as tk
from tkinter import Canvas, Label

from config import NOTES_IN_OCTAVE

class KeysModeFrame(tk.Frame):
    def __init__(self, parent, on_note_click, on_show_random_pdf):
        super().__init__(parent)

        self.on_note_click = on_note_click
        self.on_show_random_pdf = on_show_random_pdf

        self.main_area = tk.Frame(self)
        self.main_area.pack(fill=tk.BOTH, expand=True)

        self.left_side = tk.Frame(self.main_area)
        self.left_side.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_side = tk.Frame(self.main_area)
        self.right_side.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.left_side)
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

        self.canvas = Canvas(self.left_side, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.random_button = tk.Button(
            self.left_side,
            text="Show Random PDF",
            command=self.on_show_random_pdf
            )
        self.random_button.pack()

        self.answer_label = Label(self.left_side, text="", wraplength=600, justify="center")
        self.answer_label.pack(pady=10)

        self.feedback_label = Label(self.left_side, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=5)


        # right side with the checkboxes

        self.checkbox_vars = []
        checkbox_labels = [
            "C",
            "G",
            "D",
            "A",
            "E",
        ]


        for label_text in checkbox_labels:
            var = tk.BooleanVar(value=False)
            checkbox = tk.Checkbutton(self.right_side, text=label_text, variable=var)
            checkbox.pack(anchor="w")
            self.checkbox_vars.append(var)