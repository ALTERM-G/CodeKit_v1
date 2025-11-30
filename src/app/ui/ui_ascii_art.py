from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt, QTimer
from functools import partial

from ..core.data import STYLES, DARK_MODE_STYLES, ASCII_ART_FONTS
from ..core.ascii_art_logic import generate_ascii_art, load_ascii_fonts_in_background

def setup_ascii_art_page(window_instance):
    """Sets up the UI for the ASCII Text Art page."""
    page = QWidget()
    layout = QVBoxLayout(page)
    container_widget = QWidget()
    view_layout = QVBoxLayout(container_widget)
    view_layout.setContentsMargins(0, 60, 0, 0)
    view_layout.setSpacing(10)
    
    title = window_instance.widget_factory.create_label(window_instance.tr("ASCII Text Art"))
    title.setStyleSheet(STYLES["tab_title"])
    view_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
    
    bottom_container = QWidget()
    bottom_layout = QVBoxLayout(bottom_container)
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    bottom_layout.setSpacing(1)
    bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    window_instance.line_edit_ascii = window_instance.widget_factory.create_line_edit(
        w=700, h=45, placeholder=window_instance.tr("Enter Text"))
    window_instance.line_edit_ascii.returnPressed.connect(partial(generate_ascii_art, window_instance))
    bottom_layout.addWidget(window_instance.line_edit_ascii)
    
    options_container = QWidget()
    options_container.setFixedWidth(700)
    options_layout = QHBoxLayout(options_container)
    options_layout.setSpacing(0)

    window_instance.combo_box_ascii_font = window_instance.widget_factory.create_combo_box(
        w=430, h=40, Items_list=[window_instance.tr("Loading fonts...")], editable=True
    )
    options_layout.addWidget(window_instance.combo_box_ascii_font)
    options_layout.addSpacing(40)
    
    load_ascii_fonts_in_background(window_instance)
    
    window_instance.color_selector = window_instance.widget_factory.create_combo_box(
        w=230, h=40, Items_list=['white', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray'],
        editable=False, read_only_text=True
    )
    options_layout.addWidget(window_instance.color_selector)
    bottom_layout.addWidget(options_container)
    
    window_instance.result_ascii = window_instance.widget_factory.create_black_rect(h=340)
    bottom_layout.addWidget(window_instance.result_ascii)
    
    view_layout.addWidget(bottom_container)
    view_layout.addSpacing(30)
    
    QTimer.singleShot(0, lambda: window_instance.create_btn(None, copy_btn=True, black_rect_widget=window_instance.result_ascii))
    
    layout.addWidget(container_widget, 0, Qt.AlignmentFlag.AlignCenter)
    return page

def apply_ascii_art_theme(window_instance):
    """Applies the current theme to the ASCII Text Art UI."""
    if "ascii_text_art" not in window_instance.pages:
        return

    dark_mode = window_instance.settings.get("dark_mode", False)
    
    if dark_mode:
        window_instance.line_edit_ascii.setStyleSheet(DARK_MODE_STYLES["line_edit"])
        combo_box_style = STYLES["combo_box"].format(arrow_down_path=window_instance.arrow_down_path, arrow_up_path=window_instance.arrow_up_path)
        window_instance.combo_box_ascii_font.setStyleSheet(combo_box_style)
        window_instance.color_selector.setStyleSheet(combo_box_style)
        window_instance.result_ascii.setStyleSheet(DARK_MODE_STYLES["text_edit"])
    else:
        window_instance.line_edit_ascii.setStyleSheet(STYLES["line_edit"]) 
        combo_box_style = STYLES["combo_box"].format(arrow_down_path=window_instance.arrow_down_path, arrow_up_path=window_instance.arrow_up_path)
        combo_box_style = combo_box_style.replace("#2D2D30", "white").replace("#FFFFFF", "black").replace("#555555", "black")
        window_instance.combo_box_ascii_font.setStyleSheet(combo_box_style)
        window_instance.color_selector.setStyleSheet(combo_box_style)
        window_instance.result_ascii.setStyleSheet(STYLES["text_edit"]) 

    title = window_instance.pages["ascii_text_art"].findChild(QLabel)
    if title:
        title.setStyleSheet(STYLES["tab_title"])