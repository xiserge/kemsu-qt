import pytest
from PyQt5.QtWidgets import QApplication

from main import LibrarySystem


@pytest.fixture
def app():
    app = QApplication([])
    yield app
    app.quit()


def test_initialization(app):
    widget = LibrarySystem()
    assert widget.label.text() == 'Welcome to the Library System'
