from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon, QTextOption
from functools import partial

from ..core.data import (
    STYLES, DARK_MODE_STYLES, UI_KEYWORDS_WITH_BASE, UI_KEYWORDS_BINARY_ENCODING,
    UI_KEYWORDS_ANALYZERS, UNIT_CATEGORIES, Unit_Items, PRESERVE_NEWLINES_MODES
)

def setup_tabs_widget(window_instance, tabs_info, base_placeholder="Base", parent_widget=None, menu_name=None):
    """
    Dynamically creates a QTabWidget with multiple tabs based on the provided configuration.
    This function is extracted from the main Window class for modularity.
    """
    window_instance.delete_tabs()
    tab_widget = QTabWidget(parent_widget)
    tab_widget.setTabPosition(QTabWidget.TabPosition.South)
    tab_widget.setMovable(False)
    tab_widget.setTabsClosable(False)
    tab_widget.setStyleSheet(STYLES["tab_widget"])
    tab_widget.setFont(window_instance.Font2)
    tab_widget.tabBar().setCursor(window_instance.Cursor)

    win_width = window_instance.width()
    content_width = 700
    start_x = (win_width - content_width) // 2

    if parent_widget:
        tab_widget.setFixedSize(parent_widget.width() - 30, parent_widget.height())
        tab_widget.move(30, 0)
        start_x -= 30

    for name, placeholder in tabs_info:
        widget = QWidget()
        y_pos = 100
        if menu_name in ["Character Stats", "Number Analysis", "Code Analyzer"]:
            y_pos -= 20

        Title_Label = QLabel(window_instance.tr(name), widget)
        Title_Label.setFont(window_instance.Font3)
        Title_Label.setWordWrap(True)
        Title_Label.setObjectName("tabTitleLabel")
        Title_Label.original_text = name
        Title_Label.setStyleSheet(STYLES["tab_title"])
        Title_Label.setFixedWidth(content_width)
        Title_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Title_Label.move(start_x, y_pos)
        y_pos += Title_Label.height() + 15

        if "Random" in name:
            limit = ""
            if "Password" in name or "Letters" in name or "Number" in name:
                limit = " (max 100,000)"
            elif "ID" in name or "IP" in name:
                limit = " (max 10,000)"
            elif "Coprimes" in name:
                limit = " (max 1,000,000)"
            elif "Equation" in name:
                limit = " (max 1000)"
            placeholder += limit
        translated_placeholder = window_instance.tr(placeholder)

        if any(keyword in name for keyword in UI_KEYWORDS_WITH_BASE) and name not in ["Divisibility Checker"]:
            line_edit = window_instance.widget_factory.create_line_edit(w=590, h=45, placeholder=translated_placeholder, parent=widget)
            line_edit.move(start_x, y_pos)

            if name == "Custom":
                base_input = window_instance.widget_factory.create_spin_box(min_val=2, max_val=62, placeholder=base_placeholder)
            elif name == "ROT-N":
                base_input = window_instance.widget_factory.create_spin_box(min_val=-25, max_val=25, placeholder=base_placeholder)
            else:
                base_input = window_instance.widget_factory.create_line_edit(w=100, h=45, placeholder=base_placeholder)

            base_input.setParent(widget)
            base_input.move(start_x + 600, y_pos)
            y_pos += line_edit.height() + 8

            black_rect = window_instance.widget_factory.create_black_rect()
            black_rect.setParent(widget)
            black_rect.move(start_x, y_pos)

            if name in ("ROT-N", "Custom"):
                line_edit.returnPressed.connect(partial(window_instance.update_black_rect, line_edit, black_rect, base_input, name, None))
                base_input.returnPressed.connect(partial(window_instance.update_black_rect, line_edit, black_rect, base_input, name, None))
            else:
                line_edit.returnPressed.connect(partial(window_instance.update_black_rect, line_edit, black_rect, base_input, name, None, None, True))

        elif any(k in name for k in ("RSA", "ECC", "ElGamal")):
            if "Generate" in name:
                gen_btn = QPushButton(window_instance.tr("Generate"), widget)
                gen_btn.setCursor(window_instance.Cursor)
                gen_btn.setFont(window_instance.Font1)
                gen_btn.setFixedSize(190, 45)
                gen_btn.setObjectName("mainMenuButton")
                button_style = DARK_MODE_STYLES["mainMenuButton_dark"] if window_instance.settings.get("dark_mode") else STYLES["menu_button"]
                gen_btn.setStyleSheet(button_style)
                gen_btn.clicked.connect(partial(window_instance.play_sound, "click"))

                key_size_input = None
                if "ECC" in name:
                    key_size_input = window_instance.widget_factory.create_combo_box(w=250, Items_list=["SECP256R1", "SECP384R1", "SECP521R1", "SECP256K1"])
                    key_size_input.setParent(widget)
                    key_size_input.move(start_x + 120, y_pos)
                    gen_btn.move(start_x + 380, y_pos)
                elif "RSA" in name:
                    key_size_input = window_instance.widget_factory.create_combo_box(w=250, Items_list=["2048", "4096"])
                    key_size_input.setParent(widget)
                    key_size_input.move(start_x + 120, y_pos)
                    gen_btn.move(start_x + 380, y_pos)
                else:  # ElGamal
                    key_size_input = None # No key size selection for ElGamal
                    gen_btn.setFixedWidth(250)
                    gen_btn.move(start_x + 225, y_pos)
                
                y_pos += gen_btn.height() + 8

                black_rect = window_instance.widget_factory.create_black_rect(h=335)
                black_rect.setParent(widget)
                black_rect.move(start_x, y_pos)
                gen_btn.clicked.connect(partial(window_instance._generate_keys, name, black_rect, key_size_input))
                window_instance.create_btn(None, True, black_rect_widget=black_rect)
            else:
                line_edit = window_instance.widget_factory.create_line_edit(style=STYLES["line_edit_v2"], text_edit=True, w=345, h=150, placeholder=translated_placeholder, parent=widget)
                line_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
                line_edit.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
                line_edit.setAcceptRichText(False)
                line_edit.installEventFilter(window_instance)
                line_edit.move(start_x, y_pos)

                placeholder_text = window_instance.tr("Public Key") if "Encrypt" in name else window_instance.tr("Private Key")
                base_input = window_instance.widget_factory.create_line_edit(style=STYLES["line_edit_v2"], text_edit=True, w=345, h=150, placeholder=placeholder_text, parent=widget)
                base_input.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
                base_input.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
                base_input.setAcceptRichText(False)
                base_input.move(start_x + 355, y_pos)
                y_pos += line_edit.height() + 8

                black_rect = window_instance.widget_factory.create_black_rect(h=245)
                black_rect.setParent(widget)
                black_rect.move(start_x, y_pos)

                run_button = QPushButton(line_edit)
                run_button.setCursor(window_instance.Cursor)
                run_button.setFont(window_instance.Font1)
                icon_path = window_instance.run_button_black_svg_path if not window_instance.settings.get("dark_mode") else window_instance.run_button_svg_path
                run_button.setIcon(QIcon(icon_path))
                run_button.setIconSize(QSize(36, 36))
                run_button.setFixedSize(50, 50)
                run_button.setStyleSheet(STYLES["Run_Button"])
                run_button.move(line_edit.width() - run_button.width() - 7, line_edit.height() - run_button.height() - 2)
                run_button.clicked.connect(partial(window_instance.update_black_rect, line_edit, black_rect, base_input, name, None, Encryption_1=True))
                line_edit.run_button = run_button

        elif any(k in name for k in UI_KEYWORDS_BINARY_ENCODING):
            line_edit = window_instance.widget_factory.create_line_edit(w=550, h=45, placeholder=translated_placeholder, parent=widget)
            line_edit.move(start_x, y_pos)

            mode_selector = window_instance.widget_factory.create_combo_box(Items_list=['Encode', 'Decode'], parent=widget)
            mode_selector.move(start_x + 560, y_pos)
            y_pos += line_edit.height() + 8

            black_rect = window_instance.widget_factory.create_black_rect()
            black_rect.setParent(widget)
            black_rect.move(start_x, y_pos)

            line_edit.returnPressed.connect(partial(window_instance.update_black_rect, line_edit, black_rect, None, name, mode_selector))
            mode_selector.currentTextChanged.connect(partial(window_instance.update_black_rect, line_edit, black_rect, None, name, mode_selector))

        elif name in UNIT_CATEGORIES:
            line_edit = window_instance.widget_factory.create_line_edit(w=490, h=45, placeholder=translated_placeholder, parent=widget)
            line_edit.move(start_x, y_pos)

            Item_list_1, Item_list_2 = Unit_Items.get(name, ([], []))
            mode_selector = window_instance.widget_factory.create_combo_box(w=100, Items_list=Item_list_1, parent=widget)
            mode_selector.move(start_x + 500, y_pos)

            mode_selector_2 = window_instance.widget_factory.create_combo_box(w=100, Items_list=Item_list_2, parent=widget)
            mode_selector_2.move(start_x + 605, y_pos)
            y_pos += line_edit.height() + 8

            black_rect = window_instance.widget_factory.create_black_rect()
            black_rect.setParent(widget)
            black_rect.move(start_x, y_pos)

            line_edit.returnPressed.connect(partial(window_instance.update_black_rect, line_edit, black_rect, None, name, mode_selector=mode_selector, mode_selector_2=mode_selector_2))

        elif any(k in name for k in UI_KEYWORDS_ANALYZERS):
            line_edit = window_instance.widget_factory.create_line_edit(style=STYLES["line_edit_v2"], text_edit=True, w=700, h=170, placeholder=translated_placeholder, parent=widget)
            line_edit.move(start_x, y_pos)
            if name in ["Language Detection", "Cipher Detection"]:
                line_edit.setProperty("is_code_analyzer", True)
            line_edit.installEventFilter(window_instance)

            if name == "Syntax Analysis":
                black_rect = window_instance.widget_factory.create_black_rect(h=180)
            else:
                black_rect = window_instance.widget_factory.create_black_rect(h=220)
            black_rect.setParent(widget)            
            run_button = window_instance.widget_factory.create_run_button(button_type='icon_inside', parent_widget=line_edit)
            y_pos += line_edit.height() + 8

            run_button.clicked.connect(partial(window_instance.update_black_rect, line_edit, black_rect, None, name, mode_selector=None))

            black_rect.move(start_x, y_pos)

        else:
            if name == "Divisibility Checker":
                line_edit = window_instance.widget_factory.create_line_edit(w=590, h=45, placeholder=window_instance.tr("Enter Number"), parent=widget)
                line_edit.move(start_x, y_pos)
                base_input = window_instance.widget_factory.create_line_edit(w=100, h=45, placeholder=window_instance.tr("Divider"), parent=widget)
                base_input.move(start_x + 600, y_pos)
            else:
                base_input = None
                line_edit = window_instance.widget_factory.create_line_edit(placeholder=translated_placeholder, parent=widget)
                line_edit.move(start_x, y_pos)

            y_pos += line_edit.height() + 8
            black_rect = window_instance.widget_factory.create_black_rect()
            black_rect.setParent(widget)
            black_rect.move(start_x, y_pos)

            line_edit.returnPressed.connect(partial(window_instance.update_black_rect, line_edit, black_rect, base_input if name == "Divisibility Checker" else None, name, None))

        QTimer.singleShot(0, lambda b=black_rect: window_instance.create_btn(None, copy_btn=True, black_rect_widget=b))

        short_name = window_instance.short_names.get(name, name)
        index = tab_widget.addTab(widget, window_instance.tr(short_name))
        window_instance.line_edits.append(line_edit)
        tab_widget.setTabToolTip(index, window_instance.tr(name))

    try:
        tab_widget.currentChanged.disconnect()
    except TypeError:
        pass

    tab_widget.show()
    tab_widget.currentChanged.connect(partial(window_instance.play_sound, "tab"))

    return tab_widget