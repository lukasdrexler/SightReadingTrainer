import tkinter as tk


def create_menu_bar(root, on_new_random_note, on_show_answer, on_exit, on_about):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    options_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu = tk.Menu(menu_bar, tearoff=0)

    file_menu.add_command(label="New Random Note", command=on_new_random_note)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=on_exit)

    options_menu.add_command(label="Show Answer", command=on_show_answer)

    help_menu.add_command(label="About", command=on_about)

    menu_bar.add_cascade(label="File", menu=file_menu)
    menu_bar.add_cascade(label="Options", menu=options_menu)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    return menu_bar