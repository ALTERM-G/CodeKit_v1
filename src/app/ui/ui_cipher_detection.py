from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from functools import partial

from ..core.data import STYLES, DARK_MODE_STYLES

def setup_cipher_detection_page(window_instance):
    """Sets up the widgets for the Cipher Detection page."""
    page = QWidget()
    layout = QVBoxLayout(page)
    container_widget = QWidget()
    view_layout = QVBoxLayout(container_widget)
    view_layout.setContentsMargins(0, 60, 0, 0)
    view_layout.setSpacing(10)

    title = window_instance.widget_factory.create_label(window_instance.tr("Cipher Detection"))
    title.setStyleSheet(STYLES["tab_title"])
    view_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

    window_instance.cipher_detection_input = window_instance.widget_factory.create_line_edit(style=STYLES["line_edit_v2"], text_edit=True, w=700, h=170, placeholder=window_instance.tr("Enter Text"))
    window_instance.cipher_detection_input.setProperty("is_code_analyzer", True)
    window_instance.cipher_detection_input.installEventFilter(window_instance)
    view_layout.addWidget(window_instance.cipher_detection_input, alignment=Qt.AlignmentFlag.AlignCenter)

    window_instance.cipher_detection_output = window_instance.widget_factory.create_black_rect(h=220)
    view_layout.addWidget(window_instance.cipher_detection_output, alignment=Qt.AlignmentFlag.AlignCenter)

    run_button = window_instance.widget_factory.create_run_button(
        button_type='icon_inside', parent_widget=window_instance.cipher_detection_input)
    run_button.clicked.connect(partial(window_instance.update_black_rect, window_instance.cipher_detection_input, window_instance.cipher_detection_output, None, "Cipher Detection"))
    window_instance.create_btn(None, copy_btn=True, black_rect_widget=window_instance.cipher_detection_output)
    layout.addWidget(container_widget, 0, Qt.AlignmentFlag.AlignCenter)
    return page

def apply_cipher_detection_theme(window_instance):
    """Applies the current theme to the Cipher Detection UI."""
    if "cipher_detection" not in window_instance.pages:
        return

    dark_mode = window_instance.settings.get("dark_mode", False)

    if dark_mode:
        window_instance.cipher_detection_input.setStyleSheet(DARK_MODE_STYLES["text_edit"])
        window_instance.cipher_detection_output.setStyleSheet(DARK_MODE_STYLES["text_edit"])
    else: 
        window_instance.cipher_detection_input.setStyleSheet(STYLES["line_edit_v2"]) 
        window_instance.cipher_detection_output.setStyleSheet(STYLES["text_edit"]) 
    
    if hasattr(window_instance.cipher_detection_input, 'run_button'):
        icon_path = window_instance.run_button_svg_path if dark_mode else window_instance.run_button_black_svg_path
        window_instance.cipher_detection_input.run_button.setIcon(QIcon(icon_path))