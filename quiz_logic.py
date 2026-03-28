import random

import fitz

from pdf_utils import extract_note_name


def choose_random_pdf(pdf_files):
    return random.choice(pdf_files)


def load_random_question(pdf_files):
    pdf_path = choose_random_pdf(pdf_files)
    pdf_document = fitz.open(pdf_path)
    correct_answer = extract_note_name(pdf_path)
    return pdf_path, pdf_document, correct_answer


def is_correct_answer(user_answer, correct_answer):
    return user_answer == correct_answer