import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QTextCharFormat, QTextCursor

from ..core.data import STYLES, DARK_MODE_STYLES

def setup_regex_visualizer_page(window_instance):
    """Sets up the UI for the Regex Visualizer page."""
    page = QWidget()
    layout = QVBoxLayout(page)
    container_widget = QWidget()
    view_layout = QVBoxLayout(container_widget)
    view_layout.setContentsMargins(0, 40, 0, 0)
    view_layout.setSpacing(10)

    title = window_instance.widget_factory.create_label(window_instance.tr("Regex Tester"))
    title.setStyleSheet(STYLES["tab_title"])
    view_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

    window_instance.regex_input = window_instance.widget_factory.create_line_edit(w=700, h=45, placeholder=window_instance.tr("Enter Regex Pattern"))
    view_layout.addWidget(window_instance.regex_input, alignment=Qt.AlignmentFlag.AlignCenter)

    window_instance.regex_text_area = window_instance.widget_factory.create_black_rect(h=400)
    window_instance.regex_text_area.setReadOnly(False)
    window_instance.regex_text_area.setPlaceholderText(window_instance.tr("Enter Text to Test"))
    
    font = window_instance.regex_text_area.font()
    font.setPointSize(font.pointSize() + 2)
    window_instance.regex_text_area.setFont(font)
    view_layout.addWidget(window_instance.regex_text_area, alignment=Qt.AlignmentFlag.AlignCenter)

    window_instance.regex_input.textChanged.connect(lambda: update_regex_highlighting(window_instance))
    window_instance.regex_text_area.textChanged.connect(lambda: update_regex_highlighting(window_instance))

    layout.addWidget(container_widget, 0, Qt.AlignmentFlag.AlignCenter)
    return page

def update_regex_highlighting(window_instance):
    """Highlights regex matches in the text area."""
    pattern = window_instance.regex_input.text()
    text = window_instance.regex_text_area.toPlainText()
    window_instance.regex_text_area.blockSignals(True)
    cursor = window_instance.regex_text_area.textCursor()
    cursor.select(QTextCursor.SelectionType.Document)
    cursor.setCharFormat(QTextCharFormat()) 
    cursor.clearSelection()

    highlight_format = QTextCharFormat()
    highlight_format.setBackground(QColor("#dd1124"))

    if pattern:
        try:
            for match in re.finditer(pattern, text):
                start, end = match.span()
                cursor.setPosition(start)
                cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, end - start)
                cursor.mergeCharFormat(highlight_format)
        except re.error:
            pass 
    window_instance.regex_text_area.blockSignals(False)