from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QTextEdit, QComboBox, QSpinBox, QPushButton
)
from PyQt6.QtGui import QFont, QTextOption, QIcon
from PyQt6.QtCore import Qt, QSize

from ..core.data import STYLES, DARK_MODE_STYLES


class WidgetFactory:
    """A factory class for creating styled widgets."""

    def __init__(self, window_instance):
        self.window = window_instance

    def create_label(self, text: str):
        label = QLabel(text)
        label.setFont(self.window.Font3)
        label.setStyleSheet(STYLES["title_label"])
        return label

    def create_line_edit(self, w=700, h=45, style=STYLES["line_edit"], placeholder=None, text_edit=False, parent=None):
        if not text_edit:
            line_edit = QLineEdit(parent)
        else:
            line_edit = QTextEdit(parent)
            vertical_scrollbar = line_edit.verticalScrollBar()
            if vertical_scrollbar:
                vertical_scrollbar.setCursor(Qt.CursorShape.PointingHandCursor)
            horizontal_scrollbar = line_edit.horizontalScrollBar()
            if horizontal_scrollbar:
                horizontal_scrollbar.setCursor(Qt.CursorShape.PointingHandCursor)
        
        line_edit.setPlaceholderText(placeholder)
        input_font = QFont(self.window.Font1)
        input_font.setPointSize(10)
        line_edit.setFont(input_font)
        line_edit.setFixedSize(w, h)

        dark_mode = self.window.settings.get("dark_mode", False)
        if dark_mode:
            current_style = DARK_MODE_STYLES.get("text_edit" if text_edit else "line_edit", style)
        else:
            current_style = style
        line_edit.setStyleSheet(current_style)

        if text_edit and (style == STYLES["line_edit_v2"] or dark_mode):
            line_edit.setViewportMargins(0, 0, 50, 0)
        
        line_edit.setFocus()
        return line_edit

    def create_black_rect(self, w=700, h=350, style=STYLES["text_edit"]):
        black_rect = QTextEdit()
        black_rect.setFixedSize(w, h)
        
        dark_mode = self.window.settings.get("dark_mode", False)
        current_style = DARK_MODE_STYLES.get("text_edit", style) if dark_mode else style
        black_rect.setStyleSheet(current_style)
        
        black_rect.setReadOnly(True)
        black_rect.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        black_rect.setFontFamily(self.window.family1)
        black_rect.setViewportMargins(0, 0, 105, 0)
        black_rect.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        
        for scrollbar in [black_rect.verticalScrollBar(), black_rect.horizontalScrollBar()]:
            if scrollbar:
                scrollbar.setCursor(Qt.CursorShape.PointingHandCursor)
        return black_rect

    def create_combo_box(self, w=140, h=45, Items_list=[], editable=False, read_only_text=False, parent=None):
        mode_selector = QComboBox(parent)
        mode_selector.original_items = Items_list
        mode_selector.addItems([self.window.tr(item) for item in Items_list])
        mode_selector.setFont(self.window.Font1)
        mode_selector.setEditable(True)
        line_edit = mode_selector.lineEdit()
        line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_edit.setReadOnly(not editable or read_only_text)
        mode_selector.setFixedSize(w, h)
        mode_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        mode_selector.view().setCursor(self.window.Cursor)
        
        style = STYLES["combo_box"].format(arrow_down_path=self.window.arrow_down_path, arrow_up_path=self.window.arrow_up_path)
        mode_selector.setStyleSheet(style)
        view_style = style + " QAbstractItemView::item:selected { background-color: #dd1124; color: white; }"
        mode_selector.view().setStyleSheet(view_style)
        line_edit.setStyleSheet("selection-background-color: #dd1124; selection-color: white;")
        return mode_selector

    def create_spin_box(self, w=94, h=45, min_val=0, max_val=999999, placeholder=""):
        spin_box = QSpinBox()
        spin_box.setRange(min_val, max_val)
        spin_box.setFont(self.window.Font3)
        spin_box.setFixedSize(w, h)
        spin_box.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        spin_box.lineEdit().setPlaceholderText(placeholder)
        spin_box.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        spin_box.setCursor(self.window.Cursor)
        style = STYLES["spin_box"].format(arrow_up_path=self.window.arrow_up_path, arrow_down_path=self.window.arrow_down_path)
        spin_box.setStyleSheet(style)
        return spin_box

    def create_run_button(self, button_type: str, parent_widget = None) -> QPushButton:
        """
        Creates a 'Run' button with a specified style.

        Args:
            button_type: 'icon_inside' for a transparent button inside a QTextEdit,
                         'standalone' for a regular styled button.
            parent_widget: The parent widget, required for 'icon_inside' type.
        """
        run_button = QPushButton(parent_widget)
        run_button.setCursor(self.window.Cursor)
        run_button.setFixedSize(50, 50)

        dark_mode = self.window.settings.get("dark_mode", False)
        icon_path = self.window.run_button_svg_path if dark_mode else self.window.run_button_black_svg_path

        if button_type == 'icon_inside':
            if not parent_widget or not isinstance(parent_widget, QTextEdit):
                raise ValueError("A QTextEdit 'parent_widget' is required for 'icon_inside' button type.")
            
            run_button.setIcon(QIcon(icon_path))
            run_button.setIconSize(QSize(36, 36))
            run_button.setStyleSheet(STYLES["Run_Button"])
            run_button.move(parent_widget.width() - run_button.width() - 5, 5)
            parent_widget.run_button = run_button

        elif button_type == 'standalone':
            run_button.setIcon(QIcon(icon_path))
            run_button.setIconSize(QSize(32, 32))
            # The specific theme-dependent style is applied in `apply_color_converter_theme`

        else:
            raise ValueError(f"Unknown run button type: {button_type}")

        return run_button