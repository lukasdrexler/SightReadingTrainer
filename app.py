import tkinter as tk
from tkinter import Canvas, Label

from config import APP_TITLE, ALL_NOTES, NOTES_IN_OCTAVE
from menu import create_menu_bar
from pdf_utils import render_pdf, build_pdf_file_list
from quiz_logic import load_random_question, is_correct_answer


class SightReadingTrainerApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title(APP_TITLE)

        self.pdf_files = build_pdf_file_list(ALL_NOTES)

        self.current_pdf = None
        self.current_answer = None
        self.answered = False

        self._build_menu()
        self._build_widgets()
        self._bind_events()

    def _build_menu(self):
        self.menu_bar = create_menu_bar(
            root=self.app,
            on_new_random_note=self.show_random_pdf,
            on_show_answer=self.show_answer,
            on_exit=self.app.quit,
            on_about=self.show_about,
        )

    def _build_widgets(self):
        self.button_frame = tk.Frame(self.app)
        self.button_frame.pack(pady=5)

        for note_group in NOTES_IN_OCTAVE:
            group_frame = tk.Frame(self.button_frame)
            group_frame.pack(side=tk.LEFT, padx=2)

            for note in note_group:
                button = tk.Button(
                    group_frame,
                    text=note,
                    width=4,
                    command=lambda n=note: self.on_note_button_clicked(n)
                )
                button.pack()

        self.canvas = Canvas(self.app, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.random_button = tk.Button(
            self.app,
            text="Show Random PDF",
            command=self.show_random_pdf
        )
        self.random_button.pack()

        self.answer_label = Label(self.app, text="", wraplength=600, justify="center")
        self.answer_label.pack(pady=10)

        self.feedback_label = Label(self.app, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=5)

    def _bind_events(self):
        self.app.bind("<Configure>", self.on_resize)
        self.app.bind_all("<space>", self.show_random_pdf)

    def on_resize(self, event):
        if self.current_pdf is None:
            return
        render_pdf(self.canvas, self.current_pdf)

    def show_answer(self):
        if self.current_answer is not None:
            self.answer_label.config(text=self.current_answer)

    def show_about(self):
        self.feedback_label.config(text=APP_TITLE)

    def check_answer(self, user_answer):
        if self.current_answer is None or self.answered:
            return

        self.answered = True

        if is_correct_answer(user_answer, self.current_answer):
            self.feedback_label.config(text="Correct ✅")
        else:
            self.feedback_label.config(
                text=f"Incorrect ❌ (Correct: {self.current_answer})"
            )

    def on_note_button_clicked(self, note_name):
        self.check_answer(note_name)

    def show_random_pdf(self, event=None):
        self.answered = False

        _, self.current_pdf, self.current_answer = load_random_question(self.pdf_files)

        render_pdf(self.canvas, self.current_pdf)
        self.answer_label.config(text="")
        self.feedback_label.config(text="")

    def run(self):
        self.app.mainloop()