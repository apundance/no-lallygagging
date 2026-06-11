from pathlib import Path
import json
import xml.etree.ElementTree as ET


class BibleService:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.bible_data = {}
        self.book_list = []
        self.current_version = None
        self.versions = {}

        self._discover_versions()

        # book ordering
        self.OT_BOOKS = [
            "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
            "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
            "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
            "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
            "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
            "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
            "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
            "Zephaniah", "Haggai", "Zechariah", "Malachi"
        ]

        self.NT_BOOKS = [
            "Matthew", "Mark", "Luke", "John", "Acts",
            "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
            "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
            "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
            "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
            "Jude", "Revelation"
        ]

        self.OT_BOOKS_ZH = [
            "創世記", "出埃及記", "利未記", "民數記", "申命記",
            "約書亞記", "士師記", "路得記", "撒母耳記上", "撒母耳記下",
            "列王紀上", "列王紀下", "歷代志上", "歷代志下", "以斯拉記",
            "尼希米記", "以斯帖記", "約伯記", "詩篇", "箴言",
            "傳道書", "雅歌", "以賽亞書", "耶利米書", "耶利米哀歌",
            "以西結書", "但以理書", "何西阿書", "約珥書", "阿摩司書",
            "俄巴底亞書", "約拿書", "彌迦書", "那鴻書", "哈巴谷書",
            "西番雅書", "哈該書", "撒迦利亞書", "瑪拉基書"
        ]

        self.NT_BOOKS_ZH = [
            "馬太福音", "馬可福音", "路加福音", "約翰福音", "使徒行傳",
            "羅馬書", "哥林多前書", "哥林多後書", "加拉太書", "以弗所書",
            "腓立比書", "歌羅西書", "帖撒羅尼迦前書", "帖撒羅尼迦後書",
            "提摩太前書", "提摩太後書", "提多書", "腓利門書", "希伯來書",
            "雅各書", "彼得前書", "彼得後書", "約翰一書", "約翰二書",
            "約翰三書", "猶大書", "啟示錄"
        ]

    # ---------------- VERSION DISCOVERY ---------------- #
    def _discover_versions(self):
        base = self.project_root / "bibles"
        self.versions = {}

        if not base.exists():
            return

        for item in base.iterdir():
            if item.is_dir():
                books_folder = item / f"{item.name.lower()}_books"
                if books_folder.exists():
                    self.versions[item.name] = ("json", books_folder)

            elif item.suffix.lower() == ".xml":
                self.versions[item.stem] = ("usfx", item)

    # ---------------- PUBLIC API ---------------- #
    def get_versions(self):
        return list(self.versions.keys())

    def load_version(self, version_name):
        if version_name not in self.versions:
            return

        self.current_version = version_name
        self.bible_data = {}

        vtype, path = self.versions[version_name]

        if vtype == "json":
            for file in path.glob("*.json"):
                with open(file, "r", encoding="utf-8") as f:
                    self.bible_data.update(json.load(f))

        elif vtype == "usfx":
            self._load_usfx(path)

        self._build_book_list()

    def _load_usfx(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for book_elem in root.findall("book"):
            book_name = (
                book_elem.find("h").text
                if book_elem.find("h") is not None
                else book_elem.get("id")
            )

            self.bible_data[book_name] = {}
            current_chap = None

            for elem in book_elem:
                if elem.tag == "c":
                    current_chap = elem.get("id")
                    self.bible_data[book_name][current_chap] = {}

                elif elem.tag == "v" and current_chap:
                    vid = elem.get("id")
                    text = (elem.tail or "").strip()
                    self.bible_data[book_name][current_chap][vid] = text

    def _build_book_list(self):
        if any(b in self.bible_data for b in self.OT_BOOKS):
            self.book_list = (
                [b for b in self.OT_BOOKS if b in self.bible_data] +
                [b for b in self.NT_BOOKS if b in self.bible_data]
            )
        else:
            self.book_list = (
                [b for b in self.OT_BOOKS_ZH if b in self.bible_data] +
                [b for b in self.NT_BOOKS_ZH if b in self.bible_data]
            )

    # ---------------- DATA ACCESS ---------------- #
    def get_books(self):
        return self.book_list

    def get_chapters(self, book):
        return list(self.bible_data.get(book, {}).keys())

    def get_verses(self, book, chapter):
        return self.bible_data.get(book, {}).get(chapter, {})