import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import random
from services.quiz_utils import get_blank_indices

from core.base_screen import BaseScreen


class QuizScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app)

        self.service = app.services["bible"]

        # ---------------- STATE ---------------- #
        self.current_book = None
        self.current_chapter = None
        self.quiz_data = []

        self.version_var = tk.StringVar()
        self.book_var = tk.StringVar()
        self.chapter_var = tk.StringVar()
        self.verse_range_var = tk.StringVar()
        self.difficulty_var = tk.StringVar(value="Medium")

        # sets the default/initial size
        self.font_size_var = tk.IntVar(value=22)
        self.base_font_size = 22

        # ---------------- NAV ---------------- #
        nav = tk.Frame(self, bg="#1e1e1e")
        nav.pack(fill=tk.X, pady=5)

        tk.Button(
            nav,
            text="Bible",
            command=lambda: self.app.show_screen("home")
        ).pack(side=tk.LEFT, padx=5)

        # Text size controls on top-right
        font_frame = tk.Frame(nav, bg="#1e1e1e")
        font_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(
            font_frame,
            text="Text Size:",
            fg="white",
            bg="#1e1e1e"
        ).pack(side=tk.LEFT)

        size_slider = tk.Scale(
            font_frame,
            from_=10,
            to=40,
            orient="horizontal",
            variable=self.font_size_var,
            command=self.update_font,
            bg="#1e1e1e",
            fg="white",
            highlightthickness=0,
            troughcolor="#333",
            length=150
        )
        size_slider.pack(side=tk.LEFT)

        # ---------------- VERSION ---------------- #
        version_frame = tk.Frame(self, bg="#1e1e1e")
        version_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(version_frame, text="Version:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)

        self.version_menu = ttk.Combobox(
            version_frame,
            textvariable=self.version_var,
            values=self.service.get_versions(),
            state="readonly",
            width=20
        )
        self.version_menu.pack(side=tk.LEFT)
        self.version_menu.bind("<<ComboboxSelected>>", self.load_version)

        # ---------------- BOOK / CHAPTER ---------------- #
        top = tk.Frame(self, bg="#1e1e1e")
        top.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(top, text="Book:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)

        self.book_menu = ttk.Combobox(top, textvariable=self.book_var, state="readonly", width=25)
        self.book_menu.pack(side=tk.LEFT)
        self.book_menu.bind("<<ComboboxSelected>>", self.load_chapters)

        tk.Label(top, text="Chapter:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT, padx=10)

        self.chapter_menu = ttk.Combobox(top, textvariable=self.chapter_var, state="readonly", width=10)
        self.chapter_menu.pack(side=tk.LEFT)
        self.chapter_menu.bind("<<ComboboxSelected>>", self.load_verses)

        # ---------------- VERSE RANGE ---------------- #
        range_frame = tk.Frame(self, bg="#1e1e1e")
        range_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(range_frame, text="Verses:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)

        tk.Entry(range_frame, textvariable=self.verse_range_var, width=25).pack(side=tk.LEFT, padx=5)

        tk.Label(range_frame, text="e.g. 1-10 or 1,3,5", fg="gray", bg="#1e1e1e").pack(side=tk.LEFT)

        # ---------------- DIFFICULTY ---------------- #
        difficulty_frame = tk.Frame(self, bg="#1e1e1e")
        difficulty_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            fg="white",
            bg="#1e1e1e"
        ).pack(side=tk.LEFT)

        self.difficulty_menu = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty_var,
            state="readonly",
            width=15,
            values=[
                "Wittle Baby",
                "Easy",
                "Medium",
                "Hard",
                "All"
            ]
        )

        self.difficulty_menu.pack(side=tk.LEFT, padx=5)

        # ---------------- BUTTONS ---------------- #
        btns = tk.Frame(self, bg="#1e1e1e")
        btns.pack(fill=tk.X, pady=5)

        self.generate_btn = tk.Button(btns, text="Generate Quiz", command=self.generate_quiz)
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.random_btn = tk.Button(btns, text="Reveal Random", command=self.reveal_random, state="disabled")
        self.random_btn.pack(side=tk.LEFT, padx=5)

        self.reveal_all_btn = tk.Button(btns, text="Reveal All", command=self.reveal_all, state="disabled")
        self.reveal_all_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(btns, text="Clear", command=self.clear, state="disabled")
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # ---------------- OUTPUT ---------------- #
        output_frame = tk.Frame(self, bg="#111")
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output = tk.Text(
            output_frame,
            bg="#111",
            fg="white",
            wrap="word",
            relief="flat",
            insertbackground="white",
            font=self.get_font()
        )

        scrollbar = tk.Scrollbar(
            output_frame,
            orient="vertical",
            command=self.output.yview
        )

        self.output.configure(yscrollcommand=scrollbar.set)

        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ---------------- LOAD VERSION ---------------- #
    def load_version(self, event=None):
        version = self.version_var.get()
        if not version:
            return

        self.service.load_version(version)

        books = self.service.get_books()
        self.book_menu["values"] = books

        if books:
            self.book_var.set(books[0])
            self.load_chapters()

    # ---------------- LOAD CHAPTERS ---------------- #
    def load_chapters(self, event=None):
        self.current_book = self.book_var.get()

        chapters = self.service.get_chapters(self.current_book)
        self.chapter_menu["values"] = chapters

        if chapters:
            self.chapter_var.set(chapters[0])
            self.load_verses()

    # ---------------- LOAD VERSES ---------------- #
    def load_verses(self, event=None):
        self.output.config(state="normal")
        self.current_chapter = self.chapter_var.get()

        verses = self.service.get_verses(
            self.current_book,
            self.current_chapter
        )

        self.clear_canvas()

        for v in sorted(verses.keys(), key=int):
            self.output.insert(
                tk.END,
                f"{v}. {verses[v]}\n\n"
            )
        self.output.config(state="disabled")

    # ---------------- PARSE RANGE ---------------- #
    def parse_range(self, text):
        result = set()

        for part in text.split(","):
            part = part.strip()

            if "-" in part:
                a, b = part.split("-")
                for i in range(int(a), int(b) + 1):
                    result.add(str(i))
            else:
                if part:
                    result.add(str(int(part)))

        return sorted(result, key=int)

    # ---------------- GENERATE QUIZ ---------------- #
    def generate_quiz(self):
        if not self.current_book or not self.current_chapter:
            messagebox.showwarning("Missing", "Select book & chapter")
            return

        verse_range = self.verse_range_var.get().strip()
        if not verse_range:
            messagebox.showwarning("Missing", "Enter verse range")
            return

        verses = self.service.get_verses(self.current_book, self.current_chapter)
        selected = self.parse_range(verse_range)

        self.quiz_data = []
        self.clear_canvas()

        for verse_num in selected:
            if verse_num not in verses:
                continue

            text = verses[verse_num]
            words = text.split()

            if len(words) <= 2:
                continue

            blank_indexes = get_blank_indices(
                words,
                difficulty_percent=self.get_difficulty_percent()
            )

            blanks = []

            for i in blank_indexes:
                blanks.append({
                    "index": i,
                    "answer": words[i],
                    "revealed": False
                })

            self.quiz_data.append({
                "verse": verse_num,
                "words": words,
                "blanks": blanks
            })

        self.render()

        self.random_btn.config(state="normal")
        self.reveal_all_btn.config(state="normal")
        self.clear_btn.config(state="normal")

    # ---------------- RENDER ---------------- #
    def render(self):
        self.output.config(state="normal")
        self.clear_canvas()

        for verse in self.quiz_data:

            self.output.insert(
                tk.END,
                f"{verse['verse']}. "
            )

            for i, word in enumerate(verse["words"]):

                blank = next(
                    (
                        b
                        for b in verse["blanks"]
                        if b["index"] == i
                    ),
                    None
                )

                if blank:

                    if blank["revealed"]:
                        self.output.insert(
                            tk.END,
                            f"({blank['answer']}) "
                        )

                    else:
                        blank_text = "_" * max(
                            3,
                            len(blank["answer"])
                        )

                        btn = tk.Label(
                            self.output,
                            text=blank_text,
                            fg="white",
                            bg="#111",
                            cursor="hand2",
                            font=self.get_font()
                        )

                        btn.bind(
                            "<Button-1>",
                            lambda e, b=blank:
                            self.reveal_specific_blank(b)
                        )

                        self.output.window_create(
                            tk.END,
                            window=btn
                        )

                        self.output.insert(
                            tk.END,
                            " "
                        )

                else:
                    self.output.insert(
                        tk.END,
                        word + " "
                    )

            self.output.insert(
                tk.END,
                "\n\n"
            )
        self.output.config(state="disabled")
    # ---------------- REVEAL ---------------- #
    def reveal_specific_blank(self, blank):
        blank["revealed"] = True
        self.render()

    def reveal_random(self):
        hidden = [
            b for v in self.quiz_data
            for b in v["blanks"]
            if not b["revealed"]
        ]

        if hidden:
            random.choice(hidden)["revealed"] = True
            self.render()

    def reveal_all(self):
        for v in self.quiz_data:
            for b in v["blanks"]:
                b["revealed"] = True

        self.render()

    # ---------------- CLEAR ---------------- #
    def clear(self):
        self.quiz_data = []
        self.clear_canvas()

        self.random_btn.config(state="disabled")
        self.reveal_all_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")

        if self.current_book and self.current_chapter:
            self.load_verses()

    # ---------------- UTIL ---------------- #
    def clear_canvas(self):
        self.output.delete("1.0", tk.END)

    def get_font(self):
        return ("Helvetica", self.font_size_var.get())
    
    def update_font(self, event=None):
        self.output.config(font=self.get_font())

        # If quiz is displayed, rerender blanks with new size
        if self.quiz_data:
            self.render()

    def get_difficulty_percent(self):
        return {
            "Wittle Baby": 10,
            "Easy": 25,
            "Medium": 50,
            "Hard": 75,
            "All": 100
        }.get(
            self.difficulty_var.get(),
            25
        )