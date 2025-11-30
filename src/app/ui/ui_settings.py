from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence

from ..core.data import STYLES, DARK_MODE_STYLES
from .custom_widgets import HoverSlider, CustomKeySequenceEdit

def _create_shortcut_row(window_instance, index):
    """Creates a layout for a single shortcut setting."""
    row_layout = QHBoxLayout()
    
    key_edit = CustomKeySequenceEdit(window_instance)
    window_instance.shortcut_key_edits.append(key_edit)
    is_dark = window_instance.settings.get("dark_mode", False)
    key_edit.setKeySequence(QKeySequence(window_instance.settings["shortcuts"][index]["key"]))
    key_edit.setFixedWidth(120)
    key_edit.setStyleSheet(DARK_MODE_STYLES["line_edit"] if is_dark else STYLES["line_edit"])
    key_edit.keySequenceChanged.connect(lambda seq, i=index: window_instance.shortcut_manager.update_shortcut_key(i, seq))
    
    action_combo = window_instance.widget_factory.create_combo_box(
        w=300, h=40, Items_list=window_instance.shortcut_manager.get_shortcut_action_keys(), editable=False, read_only_text=True
    )
    if is_dark:
        style = STYLES["combo_box"].format(arrow_down_path=window_instance.arrow_down_path, arrow_up_path=window_instance.arrow_up_path)
        dark_style = DARK_MODE_STYLES.get("combo_box", style)
        action_combo.setStyleSheet(dark_style)

    action_combo.setProperty("action_index", index)
    action_key = window_instance.settings["shortcuts"][index]["action"]
    if action_key in action_combo.original_items:
        idx = action_combo.original_items.index(action_key)
        action_combo.setCurrentIndex(idx)
    action_combo.currentIndexChanged.connect(lambda _, i=index, c=action_combo: window_instance.shortcut_manager.update_shortcut_action(i, c))
    window_instance.shortcut_action_combos.append(action_combo)
    row_layout.addWidget(key_edit)
    row_layout.addWidget(action_combo)
    return row_layout

def setup_settings_page(window_instance):
    """
    Sets up the UI for the settings page.
    
    Args:
        window_instance: The main Window instance to attach widgets and connect signals.
    """
    page = QWidget()
    layout = QVBoxLayout(page)
    title = window_instance.widget_factory.create_label(window_instance.tr("Settings"))
    title.original_text = "Settings"
    title.setStyleSheet(STYLES["main_title_label"] + "margin-bottom: 20px; margin-top: 20px;")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    settings_container = QWidget()
    settings_container.setFixedWidth(500)
    settings_layout = QVBoxLayout(settings_container)
    settings_layout.setContentsMargins(0, 0, 0, 0)
    settings_layout.setSpacing(15)
    settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    settings_layout.addWidget(title)

    # --- Sound Settings Group ---
    sound_group = QFrame()
    sound_group.setStyleSheet(STYLES["settings_group"])
    sound_group_layout = QVBoxLayout(sound_group)
    sound_group_layout.setContentsMargins(10, 10, 10, 10)
    sound_group_layout.setSpacing(15)
    
    volume_control_layout = QHBoxLayout()
    volume_control_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    volume_label = QLabel(window_instance.tr("Sound Volume"))
    volume_label.original_text = "Sound Volume"
    volume_label.setFont(window_instance.Font1)
    volume_label.setStyleSheet(STYLES["settings_label"])
    volume_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    
    sound_button_container = QFrame()
    sound_button_container.setFixedSize(40, 45) 
    sound_button_container.setStyleSheet("background: transparent; border: none;")

    window_instance.sound_toggle_button = QPushButton()
    window_instance.sound_toggle_button.setParent(sound_button_container) 
    window_instance.sound_toggle_button.setFixedSize(40, 40)
    window_instance.sound_toggle_button.setCursor(window_instance.Cursor)
    window_instance.sound_toggle_button.clicked.connect(window_instance.toggle_sound)
    window_instance.sound_toggle_button.setStyleSheet("background: transparent; border: none;")
    window_instance.sound_toggle_button.move(0, 5) 
    window_instance.update_sound_toggle_icon()

    window_instance.volume_slider = HoverSlider(Qt.Orientation.Horizontal) 
    window_instance.volume_slider.setRange(0, 100)
    window_instance.volume_slider.setValue(window_instance.settings["volume"])
    window_instance.volume_slider.setFixedWidth(220)
    window_instance.volume_slider.valueChanged.connect(window_instance.set_sound_volume)

    volume_control_layout.addWidget(volume_label)
    volume_control_layout.addWidget(sound_button_container, alignment=Qt.AlignmentFlag.AlignVCenter)
    volume_control_layout.addStretch()
    volume_control_layout.addWidget(window_instance.volume_slider)
    sound_group_layout.addLayout(volume_control_layout)
    settings_layout.addWidget(sound_group)

    # --- Language Settings Group ---
    language_group = QFrame()
    language_group.setStyleSheet(STYLES["settings_group"])
    language_layout = QHBoxLayout(language_group)
    language_layout.setContentsMargins(10, 10, 10, 10)
    language_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    language_label = QLabel(window_instance.tr("Language"))
    language_label.original_text = "Language"
    language_label.setFont(window_instance.Font1)
    language_label.setStyleSheet(STYLES["settings_label"])
    language_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    window_instance.language_selector = window_instance.widget_factory.create_combo_box(
        w=220, Items_list=list(window_instance.translations.keys()), editable=False, read_only_text=True)
    window_instance.language_selector.setCurrentText(window_instance.settings["language"])
    window_instance.language_selector.currentTextChanged.connect(window_instance.change_language)
    language_layout.addWidget(language_label)
    language_layout.addStretch()
    language_layout.addWidget(window_instance.language_selector)
    settings_layout.addWidget(language_group)

    # --- Shortcuts Group ---
    shortcuts_group = QFrame()
    shortcuts_group.setStyleSheet(STYLES["settings_group"])
    shortcuts_layout = QVBoxLayout(shortcuts_group)
    shortcuts_layout.setContentsMargins(10, 10, 10, 10)
    shortcuts_layout.setSpacing(10)
    shortcuts_title = QLabel(window_instance.tr('Shortcuts'))
    shortcuts_title.original_text = "Shortcuts"
    shortcuts_title.setFont(window_instance.Font1)
    shortcuts_title.setStyleSheet(STYLES["settings_label"])
    shortcuts_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    shortcuts_layout.addWidget(shortcuts_title)
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet("QFrame { border: 1px solid #555; }")
    shortcuts_layout.addWidget(line) 
    for i in range(4):
        shortcuts_layout.addLayout(_create_shortcut_row(window_instance, i)) 
    settings_layout.addWidget(shortcuts_group)

    layout.addStretch(1)
    layout.addWidget(settings_container, 0, Qt.AlignmentFlag.AlignCenter)
    layout.addStretch(1)

    return page