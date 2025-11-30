import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, QLabel
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from ..core.data import STYLES, DARK_MODE_STYLES, COLOR_FORMAT_LIST
from ..core.converters import convert_color

def setup_color_converter_page(window_instance):
    """
    Sets up the UI for the color converter page.
    This function is extracted from the main Window class for modularity.
    """
    page = QWidget()
    container_widget = QWidget()
    container_widget.setContentsMargins(0, 0, 10, 0)
    view_layout = QVBoxLayout(container_widget)
    view_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    view_layout.setContentsMargins(0, 0, 0, 0)
    view_layout.setSpacing(15)
    
    title = window_instance.widget_factory.create_label(window_instance.tr("Color Converter"))
    title.setObjectName("colorConverterTitle")
    view_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
    
    input_container = QWidget()
    input_container.setFixedWidth(700)
    hbox_top = QHBoxLayout(input_container)
    hbox_top.setContentsMargins(0, 0, 0, 0)

    def choose_color():
        dialog = QColorDialog(window_instance)
        dialog.setStyleSheet("")
        dialog.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        picker_icon_path = os.path.join(window_instance.assets_dir, "icons", "color_picker.svg").replace("\\", "/")
        dialog.setCursor(window_instance.Cursor)
        for widget in dialog.findChildren(QWidget):
            if isinstance(widget, QPushButton):
                text = widget.text().lower()
                widget.setCursor(window_instance.Cursor)
                if "screen" in text:
                    widget.setIcon(QIcon(picker_icon_path))
                    widget.setIconSize(QSize(24, 24))
                    widget.setStyleSheet("padding-left: 5px;")
        dialog.setStyleSheet(f"""
            QColorDialog {{ background-color: #1f1f1f; }}
            QLabel {{ color: white; font-family: "{window_instance.Font2.family()}"; font-size: 14px; background: transparent; }}
            QPushButton {{ background-color: #333333; border: 2px solid black; border-radius: 5px; padding: 8px 16px; color: white; font-family: "{window_instance.Font2.family()}"; font-size: 13px; font-weight: bold; }}
            QPushButton:hover {{ background-color: #dd1124; color: white; }}
            QPushButton:pressed {{ background-color: #b60f20; }}
            QLineEdit {{ color: black; background-color: white; border: 2px solid black; border-radius: 5px; padding: 6px; font-weight: bold; selection-background-color: #dd1124; selection-color: black; }}
            QLineEdit:focus, QLineEdit:hover {{ background-color: #dd1124; color: white; }}
            QSpinBox {{ color: white; background-color: #2D2D30; border: 1px solid #555; padding: 4px; border-radius: 0px; selection-background-color: #dd1124; }}
            QSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; width: 15px; height: 12px; image: url({window_instance.arrow_up_path}); border-left: none; }}
            QSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; width: 15px; height: 12px; image: url({window_instance.arrow_down_path}); border-left: none; }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background-color: #3E3E42; }}
            QSpinBox::up-button:pressed {{ background-color: #dd1124; border-top-right-radius: 0px; }}
            QSpinBox::down-button:pressed {{ background-color: #dd1124; border-bottom-right-radius: 0px; }}
        """)
        if dialog.exec():
            color = dialog.selectedColor()
            hex_color = color.name()
            window_instance.line_edit_color.setText(hex_color)
            window_instance.color_button.setProperty("color_selected", True)
            window_instance.color_button.setIcon(QIcon())

            hover_color = "#555555" if window_instance.settings.get("dark_mode", False) else "#f0f0f0"
            window_instance.color_button.setStyleSheet(f"""
                QPushButton {{ background-color: {hex_color}; border: 2px solid {'#CCCCCC' if window_instance.settings.get("dark_mode", False) else 'black'}; border-radius: 6px; padding: 5px; }}
                QPushButton:hover {{ background-color: {hover_color}; }}
            """)

    def on_enter(event):
        if window_instance.color_button.property("color_selected"):
            dark_mode = window_instance.settings.get("dark_mode", False)
            icon_path = window_instance.palette_svg_path if dark_mode else window_instance.palette_black_svg_path
            window_instance.color_button.setIcon(QIcon(icon_path))
            window_instance.color_button.setIconSize(QSize(30, 30))

    def on_leave(event):
        if window_instance.color_button.property("color_selected"):
            window_instance.color_button.setIcon(QIcon())

    window_instance.color_button = QPushButton()
    window_instance.color_button.setFixedSize(45, 45)
    window_instance.color_button.setCursor(window_instance.Cursor)
    window_instance.color_button.setProperty("color_selected", False)
    window_instance.color_button.clicked.connect(choose_color)
    window_instance.color_button.enterEvent = on_enter
    window_instance.color_button.leaveEvent = on_leave 
    
    window_instance.line_edit_color = window_instance.widget_factory.create_line_edit(w=635, h=45, placeholder=window_instance.tr("Choose color or enter value (ex: #FF0000, red, rgb(255,0,0))"))
    window_instance.line_edit_color.returnPressed.connect(window_instance.update_color_result)

    hbox_top.addStretch(1)
    hbox_top.addWidget(window_instance.color_button)
    hbox_top.addWidget(window_instance.line_edit_color)
    hbox_top.addStretch(1)
    view_layout.addWidget(input_container)

    controls_container = QWidget()
    controls_container.setFixedWidth(700)
    hbox_controls = QHBoxLayout(controls_container)
    hbox_controls.setContentsMargins(0, 0, 0, 0)
    
    window_instance.Color_list = COLOR_FORMAT_LIST
    window_instance.combo_box_color = window_instance.widget_factory.create_combo_box(540, 50, Items_list=window_instance.Color_list)
    
    window_instance.run_button_color = window_instance.widget_factory.create_run_button(button_type='standalone')
    window_instance.run_button_color.clicked.connect(window_instance.update_color_result)

    hbox_controls.addStretch(1)
    hbox_controls.addWidget(window_instance.combo_box_color)
    hbox_controls.addSpacing(10)
    hbox_controls.addWidget(window_instance.run_button_color)
    hbox_controls.addStretch(1)
    view_layout.addWidget(controls_container)

    window_instance.result_line = window_instance.widget_factory.create_black_rect(h=240)
    view_layout.addWidget(window_instance.result_line)

    layout = QVBoxLayout(page)
    layout.addWidget(container_widget, 1, Qt.AlignmentFlag.AlignCenter)
    window_instance.color_widgets.append(container_widget)
    
    return page

def apply_color_converter_theme(window_instance):
    """Applies the current theme to the widgets in the Color Converter UI."""
    dark_mode = window_instance.settings.get("dark_mode", False)
    button_style = """
        QPushButton {{ background-color: {bg_color}; border: 2px solid {border_color}; border-radius: 6px; }}
        QPushButton:hover {{ background-color: {hover_bg_color}; }}
    """
    
    if dark_mode:
        window_instance.run_button_color.setStyleSheet(button_style.format(bg_color="#3C3C3C", border_color="#CCCCCC", hover_bg_color="#555555"))
        window_instance.color_button.setStyleSheet(button_style.format(bg_color="#3C3C3C", border_color="white", hover_bg_color="#555555"))
        window_instance.line_edit_color.setStyleSheet(DARK_MODE_STYLES["line_edit"].replace("border: 2px solid black;", "border: none;"))
        window_instance.result_line.setStyleSheet(DARK_MODE_STYLES["text_edit"].replace("border: 4px solid white;", "border: none;"))
        window_instance.run_button_color.setIcon(QIcon(window_instance.run_button_svg_path))
        window_instance.color_button.setIcon(QIcon(window_instance.palette_svg_path))
        window_instance.color_button.setIconSize(QSize(30, 30))
    else:
        window_instance.run_button_color.setStyleSheet(button_style.format(bg_color="white", border_color="black", hover_bg_color="#dd1124"))
        window_instance.color_button.setStyleSheet(button_style.format(bg_color="white", border_color="black", hover_bg_color="#f0f0f0").replace("border-radius: 5px;", "border-radius: 6px;"))
        window_instance.line_edit_color.setStyleSheet(STYLES["line_edit"])
        window_instance.result_line.setStyleSheet(STYLES["text_edit"])
        window_instance.run_button_color.setIcon(QIcon(window_instance.run_button_black_svg_path))
        window_instance.color_button.setIcon(QIcon(window_instance.palette_black_svg_path))
        window_instance.color_button.setIconSize(QSize(30, 30))
    
    title = window_instance.pages["color_converter"].findChild(QLabel, "colorConverterTitle")
    if title:
        title.setStyleSheet(STYLES["main_title_label"])