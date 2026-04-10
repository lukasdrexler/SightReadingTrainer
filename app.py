import tkinter as tk
from tkinter import ttk

from config import APP_TITLE, ALL_NOTES
from menu import create_menu_bar
from pdf_utils import render_pdf, build_pdf_file_list
from quiz_logic import load_random_question, is_correct_answer
from modes.standard_mode import StandardModeFrame
from modes.keys_mode import KeysModeFrame


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
        self.notebook = ttk.Notebook(self.app)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.standard_mode = StandardModeFrame(
            self.notebook,
            on_note_click=self.on_note_button_clicked,
            on_show_random_pdf=self.show_random_pdf
        )

        self.keys_mode = KeysModeFrame(
            self.notebook,
            on_note_click=self.on_note_button_clicked,
            on_show_random_pdf=self.show_random_pdf
        )

        self.notebook.add(self.standard_mode, text="Free Mode")
        self.notebook.add(self.keys_mode, text="Key Mode")

    def _bind_events(self):
        self.app.bind("<Configure>", self.on_resize)
        self.app.bind_all("<space>", self.show_random_pdf)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def get_active_mode_frame(self):
        current_tab_id = self.notebook.select()
        return self.notebook.nametowidget(current_tab_id)

    def on_resize(self, event):
        if self.current_pdf is None:
            return

        active_frame = self.get_active_mode_frame()
        render_pdf(active_frame.canvas, self.current_pdf)


    def on_tab_changed(self, event):
        self.app.focus_set()


    def show_answer(self):
        if self.current_answer is None:
            return

        active_frame = self.get_active_mode_frame()
        active_frame.answer_label.config(text=self.current_answer)

    def show_about(self):
        active_frame = self.get_active_mode_frame()
        active_frame.feedback_label.config(text=APP_TITLE)

    def check_answer(self, user_answer):
        if self.current_answer is None or self.answered:
            return

        self.answered = True
        active_frame = self.get_active_mode_frame()

        if is_correct_answer(user_answer, self.current_answer):
            active_frame.feedback_label.config(text="Correct ✅")
        else:
            active_frame.feedback_label.config(
                text=f"Incorrect ❌ (Correct: {self.current_answer})"
            )

    def on_note_button_clicked(self, note_name):
        self.check_answer(note_name)
        self.app.after(1500, self.show_random_pdf)


    def show_random_pdf(self, event=None):
        self.answered = False

        _, self.current_pdf, self.current_answer = load_random_question(self.pdf_files)

        for frame in (self.standard_mode, self.keys_mode):
            render_pdf(frame.canvas, self.current_pdf)
            frame.answer_label.config(text="")
            frame.feedback_label.config(text="")

        self.app.focus_set()

    def run(self):
        self.app.mainloop()