from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QFont

from ..core.data import STYLES, DARK_MODE_STYLES

def setup_repl_page(window_instance):
    """Sets up the UI for the Python REPL page."""
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(10, 60, 10, 10)
    
    window_instance.repl_output = QTextEdit()
    repl_output_style = STYLES["text_edit"].replace(
        "border: 4px solid white;", "border: none;")
    window_instance.repl_output.setStyleSheet(repl_output_style)
    repl_output_font = QFont(window_instance.Font1)
    repl_output_font.setPointSize(window_instance.Font1.pointSize() + 3)
    window_instance.repl_output.setFont(repl_output_font)
    window_instance.repl_output.setReadOnly(True)
    window_instance.repl_output.append(window_instance.tr("Python REPL - Press Enter to execute."))
    
    window_instance.repl_input = QTextEdit()
    window_instance.repl_input.setPlaceholderText(">>>")
    repl_input_font = QFont(window_instance.Font1)
    repl_input_font.setPointSize(window_instance.Font1.pointSize() + 3)
    window_instance.repl_input.setFont(repl_input_font)
    window_instance.repl_input.setStyleSheet(DARK_MODE_STYLES["text_edit"] + "font-size: 15px; border-radius: 15px;") # Explicitly dark
    window_instance.repl_input.setFixedHeight(100)
    window_instance.repl_input.installEventFilter(window_instance)
    
    layout.addWidget(window_instance.repl_output)
    layout.addWidget(window_instance.repl_input)
    return page