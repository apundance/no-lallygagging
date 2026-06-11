import tkinter as tk
from tkinter import ttk, messagebox
from core.base_screen import BaseScreen


class HomeScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app)

        nav = tk.Frame(self, bg="#1e1e1e")
        nav.pack(fill=tk.X, pady=5)

        tk.Button(
            nav,
            text="Bible",
            command=lambda: self.app.show_screen("home")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            nav,
            text="Quiz",
            command=lambda: self.app.show_screen("quiz")
        ).pack(side=tk.LEFT, padx=5)

        self.service = app.services["bible"]

        self.current_book = None
        self.current_chapter = None

        self.version_var = tk.StringVar()
        self.book_var = tk.StringVar()
        self.chapter_var = tk.StringVar()

        # ---------------- TOP ---------------- #
        top = tk.Frame(self, bg="#1e1e1e")
        top.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(top, text="Version:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)

        self.version_menu = ttk.Combobox(
            top,
            textvariable=self.version_var,
            values=self.service.get_versions(),
            state="readonly"
        )
        self.version_menu.pack(side=tk.LEFT)
        self.version_menu.bind("<<ComboboxSelected>>", self.load_version)

        tk.Label(top, text="Book:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT, padx=10)

        self.book_menu = ttk.Combobox(top, textvariable=self.book_var, state="readonly")
        self.book_menu.pack(side=tk.LEFT)
        self.book_menu.bind("<<ComboboxSelected>>", self.load_book)

        tk.Label(top, text="Chapter:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT, padx=10)

        self.chapter_menu = ttk.Combobox(top, textvariable=self.chapter_var, state="readonly")
        self.chapter_menu.pack(side=tk.LEFT)
        self.chapter_menu.bind("<<ComboboxSelected>>", self.load_chapter)

        # ---------------- TEXT ---------------- #
        self.text_area = tk.Text(self, wrap=tk.WORD, bg="#111", fg="white")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # ---------------- VERSION ---------------- #
    def load_version(self, event=None):
        version = self.version_var.get()
        self.service.load_version(version)

        books = self.service.get_books()
        self.book_menu["values"] = books

        if books:
            self.book_var.set(books[0])
            self.load_book()

    # ---------------- BOOK ---------------- #
    def load_book(self, event=None):
        book = self.book_var.get()
        self.current_book = book

        chapters = self.service.get_chapters(book)
        self.chapter_menu["values"] = chapters

        if chapters:
            self.chapter_var.set(chapters[0])
            self.load_chapter()

    # ---------------- CHAPTER ---------------- #
    def load_chapter(self, event=None):
        chapter = self.chapter_var.get()
        self.current_chapter = chapter

        self.text_area.delete("1.0", tk.END)

        verses = self.service.get_verses(self.current_book, chapter)

        for v in sorted(verses, key=lambda x: int(x)):
            self.text_area.insert(tk.END, f"{v}. {verses[v]}\n\n")