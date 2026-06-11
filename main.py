from pathlib import Path

from core.app import Application

from screens.home_screen import HomeScreen
from screens.quiz_screen import QuizScreen

from services.bible_service import BibleService


PROJECT_ROOT = Path(__file__).parent


services = {
    "bible": BibleService(
        PROJECT_ROOT
    )
}

screens = {
    "home": HomeScreen,
    "quiz": QuizScreen
}

app = Application(
    screen_registry=screens,
    start_screen="home",
    project_root=PROJECT_ROOT,
    services=services
)

app.run()