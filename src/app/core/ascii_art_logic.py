import pyfiglet
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QCompleter
from ..ui.custom_widgets import Worker
from .converters import text_to_ascii_art
from .data import ASCII_ART_FONTS


def load_ascii_fonts_in_background(window_instance):
    """Loads pyfiglet fonts in a background thread to avoid UI lag."""
    # Worker function to load fonts
    def load_fonts():
        all_fonts = pyfiglet.FigletFont.getFonts()
        return [f for f in ASCII_ART_FONTS if f in all_fonts]

    # Callback function when font loading is finished
    def on_finished(reliable_fonts):
        combo_box = window_instance.combo_box_ascii_font
        combo_box.clear()
        combo_box.addItems(reliable_fonts)
        combo_box.setEditable(True) # Ensure it's editable for search
        completer = QCompleter(reliable_fonts, combo_box)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        combo_box.lineEdit().setPlaceholderText(window_instance.tr("Search fonts...")) # Add placeholder text
        combo_box.setCompleter(completer)
        window_instance.thread.quit()

    window_instance.thread = QThread()
    window_instance.worker = Worker(load_fonts)
    window_instance.worker.moveToThread(window_instance.thread)
    window_instance.thread.started.connect(window_instance.worker.run)
    window_instance.worker.finished.connect(on_finished)
    window_instance.thread.finished.connect(window_instance.thread.deleteLater)
    window_instance.worker.finished.connect(window_instance.worker.deleteLater)
    window_instance.thread.start()

def generate_ascii_art(window_instance):
    """Generates ASCII art and displays it in the UI."""
    text = window_instance.line_edit_ascii.text().strip()
    if not text:
        return
    
    font = window_instance.combo_box_ascii_font.currentText()
    color_name = window_instance.color_selector.currentText()
    result = text_to_ascii_art(text, font=font)

    color_map = {'white': Qt.GlobalColor.white, 'red': Qt.GlobalColor.red, 'green': Qt.GlobalColor.green, 'yellow': Qt.GlobalColor.yellow, 'blue': Qt.GlobalColor.blue, 'magenta': Qt.GlobalColor.magenta, 'cyan': Qt.GlobalColor.cyan, 'gray': Qt.GlobalColor.gray}
    window_instance.result_ascii.setTextColor(color_map.get(color_name.lower(), Qt.GlobalColor.white))
    window_instance.result_ascii.setPlainText(result)