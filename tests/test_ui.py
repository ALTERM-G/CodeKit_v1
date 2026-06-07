import sys
import os
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app.ui.main_window import Window

@pytest.fixture
def app(qtbot):
    """Create and return the main application window."""
    if not QApplication.instance():
        QApplication(sys.argv)

    window = Window()
    qtbot.addWidget(window)
    window.show()
    return window

def test_app_launches_and_has_correct_title(app):
    """
    Tests that the main window launches, is visible, and has the correct title.
    """
    assert app.isVisible()
    assert app.windowTitle() == "ALTERM Converter"

def test_modes_button_navigation(app, qtbot):
    """
    Tests that clicking the 'Modes' button on the welcome screen
    correctly navigates to the modes menu.
    """
    modes_button = app.button
    assert modes_button.text() == "Modes"
    qtbot.mouseClick(modes_button, Qt.MouseButton.LeftButton)
    assert app.title_label.text() == "Modes_"