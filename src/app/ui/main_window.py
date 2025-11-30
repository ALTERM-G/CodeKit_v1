from ..core.dispatcher import detect_conversion_type
from ..core.converters import convert_color
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QFrame,
    QVBoxLayout, QHBoxLayout, QTabWidget, QGridLayout, QGraphicsOpacityEffect,
    QComboBox, QColorDialog, QCheckBox, QSlider, QFileDialog, QSpinBox,
    QStyle, QSizePolicy, QStackedWidget, QMainWindow
)
from PyQt6.QtCore import (
    QTimer, QUrl, Qt,
    QPoint, QSize, QEvent, QThread
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import (QIcon, QFont, QCursor, QPixmap,
                         QFontDatabase, QPainter, QTextCursor, QGuiApplication, QTextOption, QColor, QTextCharFormat, QShortcut, QKeySequence)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import platform
import json
from functools import partial, wraps
import io
import contextlib
import pyfiglet
import re
from .custom_widgets import Worker, HoverSlider, CustomKeySequenceEdit
from ..core.shortcut_manager import ShortcutManager
from .ui_settings import setup_settings_page
from .ui_tabs import setup_tabs_widget
from .ui_color_converter import setup_color_converter_page, apply_color_converter_theme
from .ui_ascii_art import setup_ascii_art_page, apply_ascii_art_theme
from .ui_cipher_detection import setup_cipher_detection_page, apply_cipher_detection_theme
from .ui_repl import setup_repl_page
from .widget_factory import WidgetFactory
from .ui_regex_tester import setup_regex_visualizer_page
from ..core.data import APP_CONFIG, SHORT_NAMES, SOUNDS, REPL_CONTEXT, STYLES, DARK_MODE_STYLES, BRAILLE_CHARS, MENU_DEFINITIONS, PRESERVE_NEWLINES_MODES, UNIT_CATEGORIES, MENU_STRUCTURE
import os


class Window(QMainWindow):
    """
    The main application window, managing UI, state, and interactions.
    """
    def __init__(self, base_path=None):
        super().__init__()
        self.setWindowTitle(APP_CONFIG["window_title"])
        self.setFixedSize(*APP_CONFIG["window_size"])
        self.base_path = base_path if base_path else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.central_widget = QWidget() 
        self.setCentralWidget(self.central_widget)
        style_no_radius = APP_CONFIG["background_style"].replace(
            "border-radius: 20px;", "border-radius: 0px;")
        self.central_widget.setStyleSheet(style_no_radius)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        self.pages = {}

        self.widget_factory = WidgetFactory(self)
        welcome_page = QWidget()
        welcome_layout = QVBoxLayout(welcome_page)
        self.stacked_widget.addWidget(welcome_page)
        self.pages["welcome"] = welcome_page

        self.assets_dir = os.path.join(self.base_path, "assets")
        self.app_data_dir = os.path.join(self.base_path, "data")
        self.layout_buttons = QVBoxLayout()
        
        if platform.system() == "Windows":
            self.user_data_dir = os.path.join(os.getenv('APPDATA'), "AltermApp")
        else:
            self.user_data_dir = os.path.expanduser("~/.config/alterm-app")
        self.buttons_layout_index = 1
        self.layout_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setContentsMargins(5, 5, 5, 10)
        self.Font1 = QFont()
        self.Font2 = QFont()
        self.Font3 = QFont()
        self.Font_ID1 = QFontDatabase.addApplicationFont(
            os.path.join(self.assets_dir, "fonts", "JetBrainsMono-SemiBold.ttf"))
        self.Font_ID2 = QFontDatabase.addApplicationFont(
            os.path.join(self.assets_dir, "fonts", "Quicksand-SemiBold.ttf"))
        self.Font_ID3 = QFontDatabase.addApplicationFont(
            os.path.join(self.assets_dir, "fonts", "NotoSansSymbols-Black.ttf"))
        self.Font_ID4 = QFontDatabase.addApplicationFont(
            os.path.join(self.assets_dir, "fonts", "IntelOneMono-Bold.ttf"))
        if self.Font_ID1 != -1:
            self.family1 = QFontDatabase.applicationFontFamilies(self.Font_ID1)[
                0]
            self.Font1.setFamily(self.family1)
            self.Font1.setBold(True)
            self.Font1.setPointSize(12)
        if self.Font_ID2 != -1:
            self.family2 = QFontDatabase.applicationFontFamilies(self.Font_ID2)[
                0]
            self.Font2.setFamily(self.family2)
            self.Font2.setBold(True)
            self.Font2.setPointSize(12)
        if self.Font_ID3 != -1:
            self.family_braille = QFontDatabase.applicationFontFamilies(self.Font_ID3)[
                0]
        if self.Font_ID4 != -1:
            self.family3 = QFontDatabase.applicationFontFamilies(self.Font_ID4)[
                0]
            self.Font3.setFamily(self.family3)
            self.Font3.setPointSize(10)
        self.Cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        self.arrow_back_path = os.path.join(
            self.assets_dir, "icons", "arrow_back.svg")
        self.arrow_back_red_path = os.path.join(
            self.assets_dir, "icons", "arrow_back_red.svg").replace(os.sep, "/")
        self.close_icon_path = os.path.join(
            self.assets_dir, "icons", "close_icon.svg").replace(os.sep, "/")
        self.close_icon_red_path = os.path.join(
            self.assets_dir, "icons", "close_icon_red.svg").replace(os.sep, "/")
        self.minimize_icon_path = os.path.join(
            self.assets_dir, "icons", "minimize_icon.svg").replace(os.sep, "/")
        self.minimize_icon_red_path = os.path.join(
            self.assets_dir, "icons", "minimize_icon_red.svg").replace(os.sep, "/")
        self.arrow_down_path = os.path.join(
            self.assets_dir, "icons", "arrow_down.svg").replace(os.sep, "/")
        self.arrow_up_path = os.path.join(
            self.assets_dir, "icons", "arrow_up.svg").replace(os.sep, "/")
        self.sun_icon_path = os.path.join(  
            self.assets_dir, "icons", "Light_mode.svg").replace(os.sep, "/")
        self.moon_icon_path = os.path.join( 
            self.assets_dir, "icons", "Dark_mode.svg").replace(os.sep, "/")
        self.run_button_svg_path = os.path.join(
            self.assets_dir, "icons", "run_button.svg").replace(os.sep, "/")
        self.run_button_black_svg_path = os.path.join(
            self.assets_dir, "icons", "run_button_black.svg").replace(os.sep, "/")
        self.sound_icon_path = os.path.join(
            self.assets_dir, "icons", "sound.svg").replace(os.sep, "/")
        self.no_sound_icon_path = os.path.join(
            self.assets_dir, "icons", "no_sound.svg").replace(os.sep, "/")
        self.button_back = QPushButton(self)
        self.button_back.setIcon(QIcon(self.arrow_back_path))
        self.button_back.setIconSize(QSize(48, 48))
        self.button_back.setFixedSize(50, 50)
        self.button_back.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: none; }}
            QPushButton:hover {{ icon: url('{self.arrow_back_red_path}'); }}
        """)
        self.button_back.move(10, 10)
        self.button_back.clicked.connect(self.go_back)
        self.button_back.clicked.connect(partial(self.play_sound, "back"))
        self.button_back.setCursor(self.Cursor)
        self.button_back.hide()
        self.button_dyna = []
        self.line_edits = []
        self.color_widgets = []
        self.shortcut_action_combos = []
        self.shortcut_key_edits = []
        self._is_going_back = False
        self.Result = ""
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.7)
        self.short_names = SHORT_NAMES
        self.history = []
        self.old_pos = None
        self.central_widget.installEventFilter(self)
        self.settings_file = os.path.join(self.user_data_dir, "settings.json")
        self.translations_file = os.path.join(
            self.app_data_dir, "translations.json")
        self.load_translations()
        self.load_settings()

        self.button = QPushButton(self.tr("Modes"), self)
        self.button.setObjectName("welcomeScreenButton")
        self.button.original_text = "Modes"
        self.button.setFont(self.Font1)
        self.button.setCursor(self.Cursor)
        self.button.setFixedWidth(245)
        self.opacity_button = QGraphicsOpacityEffect()
        self.opacity_button.setOpacity(0)
        self.button.clicked.connect(self.show_modes_menu)
        self.button.clicked.connect(partial(self.play_sound, "click"))
        self.repl_button_main = QPushButton(self.tr("Python REPL"), self)
        self.repl_button_main.setCursor(self.Cursor)
        self.repl_button_main.setObjectName("welcomeScreenButton")
        self.repl_button_main.original_text = "Python REPL"
        self.repl_button_main.setFont(self.Font1)
        self.repl_button_main.setFixedWidth(245)
        self.repl_button_main.clicked.connect(self.show_repl_ui)
        self.repl_button_main.clicked.connect(
            partial(self.play_sound, "click"))
        self.ascii_text_art_button_main = QPushButton(
            self.tr("ASCII Text Art"), self)
        self.ascii_text_art_button_main.setCursor(self.Cursor)
        self.ascii_text_art_button_main.setObjectName("welcomeScreenButton")
        self.ascii_text_art_button_main.original_text = "ASCII Text Art"
        self.ascii_text_art_button_main.setFont(self.Font1)
        self.ascii_text_art_button_main.setFixedWidth(245)
        self.ascii_text_art_button_main.clicked.connect(self._show_ascii_text_art_ui)
        self.ascii_text_art_button_main.clicked.connect(
            partial(self.play_sound, "click"))
        self.regex_button_main = QPushButton(
            self.tr("Regex Tester"), self)
        self.regex_button_main.setCursor(self.Cursor)
        self.regex_button_main.setObjectName("welcomeScreenButton")
        self.regex_button_main.original_text = "Regex Tester"
        self.regex_button_main.setFont(self.Font1)
        self.regex_button_main.setFixedWidth(245)
        self.regex_button_main.clicked.connect(self._show_regex_visualizer_ui)
        self.regex_button_main.clicked.connect(
            partial(self.play_sound, "click"))

        self.apply_theme(is_startup=True)
        self.audio_output = QAudioOutput()
        self.sound_outputs = []
        self.Image_url = os.path.join(
            self.assets_dir, "icons", "logo Alterm Appv2.svg")
        self.Icon_url = os.path.join(
            self.assets_dir, "icons", "alterm-app.png")
        self.sound_players = {}
        self.sounds = {name: os.path.join(self.assets_dir, path) for name, path in SOUNDS.items()}
        self.Copy_svg = os.path.join(
            self.assets_dir, "icons", "Copy_button.svg")
        self.Copied_svg = os.path.join(
            self.assets_dir, "icons", "Copied_button.svg")
        self.palette_black_svg_path = os.path.join(
            self.assets_dir, "icons", "palette_black.svg")
        self.palette_svg_path = os.path.join(
            self.assets_dir, "icons", "palette.svg")
        self.setWindowIcon(QIcon(self.Icon_url))
        for name, path in self.sounds.items():
            self.add_sound_player(name, path)
        self.repl_context = {
            "__builtins__": REPL_CONTEXT["__builtins__"], **REPL_CONTEXT}
        self.Title = QLabel("CodeKit_")
        self.Title.setStyleSheet(STYLES["main_title_label"])
        self.Title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.Title.setFont(self.Font1)
        self.Title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        renderer = QSvgRenderer(self.Image_url)
        width, height = 400, 178
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.image = QLabel(self)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(False)
        self.image.setFixedSize(width, height)
        self.image.setStyleSheet("background: transparent")
        welcome_layout.addStretch(2)
        welcome_layout.addSpacing(40)
        welcome_layout.addWidget(
            self.image, alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(
            self.Title, alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addSpacing(20)
        welcome_layout.addWidget(
            self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(self.repl_button_main,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(self.ascii_text_art_button_main,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(self.regex_button_main,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addStretch(3)
        self.home_button = QPushButton(self)
        home_icon_path = os.path.join(
            self.assets_dir, "icons", "home_icon.svg").replace(os.sep, "/")
        home_icon_red_path = os.path.join(
            self.assets_dir, "icons", "home_icon_red.svg").replace(os.sep, "/")
        self.home_button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                icon: url('{home_icon_path}');
            }}
            QPushButton:hover {{ icon: url('{home_icon_red_path}'); }}
        """)
        self.home_button.setIconSize(QSize(35, 35))
        self.home_button.setFixedSize(60, 45)
        self.home_button.move(10, 10)
        self.home_button.clicked.connect(self.show_welcome_screen)
        self.home_button.clicked.connect(partial(self.play_sound, "click"))
        self.home_button.setCursor(self.Cursor)
        self.home_button.hide()
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(
            QIcon(os.path.join(self.assets_dir, "icons", "settings_icon.svg")))
        self.settings_button.setIconSize(QSize(35, 35))
        settings_icon_path = os.path.join(
            self.assets_dir, "icons", "settings_icon.svg").replace(os.sep, "/")
        settings_icon_red_path = os.path.join(
            self.assets_dir, "icons", "settings_icon_red.svg").replace(os.sep, "/")
        self.settings_button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                icon: url('{settings_icon_path}');
            }}
            QPushButton:hover {{ icon: url('{settings_icon_red_path}'); }}
        """)
        self.settings_button.setFixedSize(60, 45)
        self.settings_button.move(10, 10)
        self.settings_button.clicked.connect(self.show_settings_ui)
        self.settings_button.clicked.connect(partial(self.play_sound, "click"))
        self.settings_button.setCursor(self.Cursor)
        self.shortcut_manager = ShortcutManager(self)
        self._initialize_menu_definitions()
        self.shortcut_manager.setup_shortcuts()

    def _capture_output(self, func, *args, **kwargs):
        """
        Captures stdout and stderr from a function call.
        Useful for running logic functions and displaying their output in the UI.
        """
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(
                stdout_capture
            ), contextlib.redirect_stderr(stderr_capture):
                func(*args, **kwargs)
            stdout = stdout_capture.getvalue()
            stderr = stderr_capture.getvalue()
            if stderr:
                return f"{stdout}\nError: {stderr}"
            return stdout
        except Exception as e:
            return f"Exception: {e}"

    def _execute_python_code(self):
        """
        Executes the code from the REPL input and displays the result in the output.
        """
        code = self.repl_input.toPlainText().strip()
        if not code:
            return
        self.repl_output.append(f">>> {code}")
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            try:
                try:
                    result = eval(code, self.repl_context)
                    if result is not None:
                        print(repr(result))
                except SyntaxError:
                    exec(code, self.repl_context)
            except Exception as e:
                print(f"Error: {e}")
        output = stdout_capture.getvalue().strip()
        error = stderr_capture.getvalue().strip()
        if output:
            if '\n' in output:
                self.repl_output.append("<<<")
                self.repl_output.append(output)
            else:
                self.repl_output.append(f"<<< {output}")
        if error:
            self.repl_output.append(f"Error: {error}")
        self.repl_input.clear()

    def add_sound_player(self, name, path):
        """
        Creates and stores a QMediaPlayer instance for a given sound name and path.
        """
        player = QMediaPlayer()
        audio_output = QAudioOutput() 
        player.setAudioOutput(audio_output) 
        player.setSource(QUrl.fromLocalFile(path))
        self.sound_players[name] = (player, audio_output) 

    def _create_theme_toggle_button(self):
        """
        Creates the sun/moon button for toggling between light and dark themes.
        """
        self.theme_toggle_button = QPushButton(self)
        self.theme_toggle_button.setFixedSize(45, 45)
        self.theme_toggle_button.setCursor(self.Cursor)
        self.theme_toggle_button.setStyleSheet(
            "background-color: transparent; border: none;"
        )
        self.theme_toggle_button.clicked.connect(self._on_theme_toggle_clicked)
        self.theme_toggle_button.move(self.width() - self.theme_toggle_button.width() - 10, 10)
        self.update_theme_toggle_button_icon()
        self.play_sound("click")

    def _on_theme_toggle_clicked(self):
        new_state = not self.settings.get("dark_mode", False)
        self.play_sound("click")
        self.toggle_dark_mode(new_state)

    def play_sound(self, sound_name: str):
        if self.settings.get("sound_enabled", True):
            player, _ = self.sound_players.get(sound_name, (None, None))
            if player:
                if player.isPlaying():
                    player.stop()
                player.setPosition(0)
                player.play()

    def update_theme_toggle_button_icon(self):
        if self.settings.get("dark_mode"):
            self.theme_toggle_button.setIcon(QIcon(self.sun_icon_path))
        else:
            self.theme_toggle_button.setIcon(QIcon(self.moon_icon_path))
        self.theme_toggle_button.setIconSize(QSize(28, 28))
        self.theme_toggle_button.show()

    def update_sound_toggle_icon(self):
        if self.settings.get("sound_enabled", True):
            self.sound_toggle_button.setIcon(QIcon(self.sound_icon_path))
        else:
            self.sound_toggle_button.setIcon(QIcon(self.no_sound_icon_path))
        self.sound_toggle_button.setIconSize(QSize(24, 24))
        self.sound_toggle_button.show()

    def tr(self, text_key):
        if not text_key:
            return ""
        if text_key.startswith("Go to: "):
            menu_name = text_key.replace("Go to: ", "")
            return f"Go to: {self.tr(menu_name)}"
        return self.translations.get(self.settings.get("language", "English"), {}).get(text_key, text_key)

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                loaded_settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            loaded_settings = {}

        defaults = {
            "sound_enabled": True,
            "volume": 80,
            "language": "English",
            "dark_mode": False,
            "shortcuts": [
                {"key": "", "action": "None"},
                {"key": "", "action": "None"},
                {"key": "", "action": "None"},
                {"key": "", "action": "None"}
            ]
        }

        self.settings = defaults
        self.settings.update(loaded_settings)

        # Ensure shortcuts list is the correct length
        num_shortcuts = 4
        if len(self.settings.get("shortcuts", [])) < num_shortcuts:
            self.settings["shortcuts"].extend([{"key": "", "action": "None"}] * (num_shortcuts - len(self.settings["shortcuts"])))
            loaded_settings = {} 

        if loaded_settings != self.settings:
            self.save_settings()

    def save_settings(self):
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)
        
        shortcuts = self.settings.get("shortcuts", [])
        clean_shortcuts = []
        if isinstance(shortcuts, list):
            for sc in shortcuts:
                if isinstance(sc, dict) and "key" in sc and "action" in sc:
                    clean_shortcuts.append({
                        "key": str(sc.get("key", "")),
                        "action": str(sc.get("action", "None"))
                    })

        clean_settings = {
            "sound_enabled": bool(self.settings.get("sound_enabled", True)),
            "volume": int(self.settings.get("volume", 80)),
            "language": str(self.settings.get("language", "English")),
            "dark_mode": bool(self.settings.get("dark_mode", False)),
            "shortcuts": clean_shortcuts
        }

        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(clean_settings, f, indent=4)

    def load_translations(self):
        try:
            with open(self.translations_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.translations = {}

    def copy_text(self, widget, button):
        if not isinstance(widget, QTextEdit):
            return

        full_text = widget.toPlainText()
        last_output_marker = '<<<'
        last_marker_pos = full_text.rfind(last_output_marker)

        if last_marker_pos != -1:
            # Copy everything after the last '<<<'
            text_to_copy = full_text[last_marker_pos + len(last_output_marker):].strip()
        else:
            # Fallback for modes that don't use the marker
            text_to_copy = full_text.strip()
        
        if text_to_copy:
            QApplication.clipboard().setText(text_to_copy)
            old_icon = QIcon(self.Copy_svg)
            old_size = button.iconSize()
            button.setText(self.tr("Copied"))
            button.setIcon(
                QIcon(os.path.join(self.assets_dir, "icons", "Copied_button.svg")))
            button.setIconSize(QSize(17, 17))
            QTimer.singleShot(1000, lambda: (
                button.setText(self.tr("Copy")),
                button.setIcon(old_icon),
                button.setIconSize(old_size)
            ))

    def eventFilter(self, obj, event):
        """
        Global event filter to handle special key presses like auto-pairing brackets
        in code editors and executing actions with Shift+Enter.
        - Auto-pairs brackets, quotes.
        - Handles smart backspace for paired characters.
        - Triggers 'run' actions on Shift+Enter.
        """
        is_code_input_widget = (isinstance(obj, QTextEdit) and 
                                (obj.property("is_code_analyzer") or (hasattr(self, 'repl_input') and obj is self.repl_input)))

        if is_code_input_widget and event.type() == QEvent.Type.KeyPress:
            cursor = obj.textCursor()
            key = event.key()
            text = event.text()
            pairs = {"(": ")", "[": "]", "{": "}", "'": "'", '"': '"'}

            if text in pairs:
                cursor.insertText(text + pairs[text])
                cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter)
                obj.setTextCursor(cursor)
                return True
            elif key == Qt.Key.Key_Backspace and not cursor.hasSelection():
                pos = cursor.position()
                doc = obj.document()
                char_before = doc.characterAt(pos - 1)
                char_after = doc.characterAt(pos)
                if pos > 0 and char_before in pairs and pairs.get(char_before) == char_after:
                    cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter)
                    cursor.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor, 2)
                    cursor.removeSelectedText()
                    return True

        if event.type() == QEvent.Type.KeyPress and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                if hasattr(obj, 'run_button') and obj.run_button:
                    obj.run_button.click()
                    return True
                elif hasattr(obj, 'parent') and hasattr(obj.parent(), 'run_button') and obj.parent().run_button:
                     obj.parent().run_button.click()
                     return True
            elif hasattr(self, 'repl_input') and obj is self.repl_input and self.repl_input.isVisible():
                self._execute_python_code()
                return True

        return super().eventFilter(obj, event)

    def _generate_keys(self, tab_name: str, black_rect: QTextEdit, key_size_input: QWidget = None):
        """
        Asynchronously generates cryptographic keys and displays them in the UI.
        """
        def generation_task():
            ks = None
            if isinstance(key_size_input, QComboBox):
                ks = key_size_input.currentText()
            elif isinstance(key_size_input, QLineEdit):
                ks = key_size_input.text().strip()
                if not ks:
                    ks = "2048"
            res = detect_conversion_type("", tab_name, base=ks, mode=None)
            return ks, res

        def on_finished(result):
            ks, res = result
            black_rect.append(f"> generate (param={ks})")
            processed_res = str(res).replace('\n', '').replace('\r', '')
            processed_res = processed_res.replace(
                "PRIVATE KEY:", "\n\nPRIVATE KEY:")
            processed_res = processed_res.replace(
                "-----BEGIN", "\n-----BEGIN").replace("-----END", "\n-----END")
            processed_res = processed_res.replace("KEY-----", "KEY-----\n")
            black_rect.append(f"< {processed_res}\n")
            QApplication.restoreOverrideCursor()
            self.thread.quit() # Ask the thread to stop

        def on_error(err_msg):
            black_rect.append(f"! Error: {err_msg}\n")
            QApplication.restoreOverrideCursor()
            self.thread.quit() # Ask the thread to stop
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.thread = QThread()
        self.worker = Worker(generation_task)
        self.worker.moveToThread(self.thread)
        # Clean up thread and worker automatically when the thread is finished
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(on_finished)
        self.worker.error.connect(on_error)
        self.thread.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.button_back.isVisible():
                self.button_back.click()
            elif self.home_button.isVisible():
                self.home_button.click()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def create_btn(self, buttons_info, copy_btn=False, w=255, h=45, style=None, return_btn=False, black_rect_widget=None):
        if style is None:
            is_dark = self.settings.get("dark_mode", False)
            style = DARK_MODE_STYLES["mainMenuButton_dark"] if is_dark else STYLES["menu_button"]

        self.clear_layout_buttons()
        if copy_btn:
            copy_button = QPushButton(self.tr("Copy"), black_rect_widget)
            copy_button.setStyleSheet(STYLES["copy_button"])
            copy_button.setIcon(QIcon(self.Copy_svg))
            copy_button.setIconSize(QSize(17, 17))
            copy_button.setFont(self.Font2) 
            copy_button.setFixedSize(100, 40)
            copy_button.move(black_rect_widget.width() - copy_button.width() - 5, 5)
            copy_button.show()
            copy_button.raise_()
            copy_button.setCursor(Qt.CursorShape.DragCopyCursor)
            copy_button.clicked.connect(partial(self.copy_text, black_rect_widget, copy_button))
            copy_button.clicked.connect(partial(self.play_sound, "click"))
        else:
            for idx, (label, function) in enumerate(buttons_info):
                button = QPushButton(self.tr(label), self)
                button.setObjectName("mainMenuButton") 
                button.original_text = label
                button.clicked.connect(function)
                button.clicked.connect(partial(self.play_sound, "click"))
                button.setStyleSheet(style)
                button.setCursor(self.Cursor)
                button.setFont(self.Font1)
                button.setFixedSize(w, h)
                self.button_dyna.append(button)
                if isinstance(self.layout_buttons, QGridLayout):
                    row = idx // 2
                    col = (idx % 2) + 1
                    self.layout_buttons.addWidget(
                        button, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
                else:
                    self.layout_buttons.addWidget(
                        button, alignment=Qt.AlignmentFlag.AlignCenter)
                if return_btn:
                    return button 

    def clear_layout_buttons(self):
        while self.layout_buttons.count():
            item = self.layout_buttons.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self.button_dyna.clear()

    def is_braille(self, text):
        return any(c in BRAILLE_CHARS for c in text)

    def delete_tabs(self):
        if hasattr(self, 'tab') and self.tab:
            self.tab.setParent(None)
            self.tab.deleteLater()
            self.tab = None
        self.line_edits.clear()
        self.clear_layout_buttons()

    def create_tabs(self, tabs_info, base_placeholder="Base", parent_widget=None, menu_name=None):
        """
        Dynamically creates a QTabWidget with multiple tabs based on the provided configuration.
        """
        self.tab = setup_tabs_widget(self, tabs_info, base_placeholder, parent_widget, menu_name)

    def update_black_rect(self, line_edit, black_rect, base_input=None, tab_name=None, mode_selector=None, mode_selector_2=None, Encryption_1=False, Encryption_2=False):
        if isinstance(line_edit, QTextEdit):
            text = line_edit.toPlainText().strip()
        else:
            text = line_edit.text() 
        
        if not text.strip() and self.sender() is line_edit:
            black_rect.append(f"! Error: {self.tr('Input is empty.')}\n")
            return

        base_value = None
        if Encryption_1 or Encryption_2:
            if isinstance(base_input, QTextEdit):
                key_text = base_input.toPlainText().strip()
            elif isinstance(base_input, QLineEdit):
                key_text = base_input.text().strip()
            else:
                key_text = ""
            if key_text.isascii():
                base_value = str(key_text)
        elif base_input:
            if isinstance(base_input, QTextEdit):
                base_text = base_input.toPlainText().strip()
            elif isinstance(base_input, QLineEdit):
                base_text = base_input.text().strip()
            if base_text.isdigit():
                base_value = int(base_text)
        
        if not text.strip():
            return

        def conversion_task():
            mode = mode_selector.currentText() if mode_selector else None
            mode2 = mode_selector_2.currentText() if mode_selector_2 else None

            return detect_conversion_type(text, tab_name, base=base_value, mode=mode, mode2=mode2)

        def on_finished(result):
            """Handles the successful result from the worker thread."""
            self.display_result(result, text, tab_name, black_rect, line_edit)
            QApplication.restoreOverrideCursor()
            self.thread.quit() 

        def on_error(err_msg):
            """Handles any error from the worker thread."""
            self.display_result(f"! Error: {self.tr(err_msg)}", text, tab_name, black_rect, line_edit)
            QApplication.restoreOverrideCursor()
            self.thread.quit() # 

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.thread = QThread()
        self.worker = Worker(conversion_task)
        self.worker.moveToThread(self.thread)
        # Clean up thread and worker automatically when the thread is finished
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(on_finished)
        self.worker.error.connect(on_error)
        self.thread.start()

    def display_result(self, result, text, tab_name, black_rect, line_edit_to_clear=None):
        if result is None:
            result = "! Error: empty result"
        preserve_newlines = any(generator in tab_name for generator in PRESERVE_NEWLINES_MODES) or tab_name in UNIT_CATEGORIES
        if isinstance(result, bytes):
            display_text = result.decode("utf-8", errors="replace")
        else:
            display_text = str(result)

        if self.is_braille(display_text) and black_rect:
            black_rect.setFontFamily(
                getattr(self, "family_braille", "DejaVu Sans"))
        if tab_name == "Cipher Detection" and isinstance(result, dict):
            display_text = "\n".join([f"• {key}: {value}" for key, value in result.items()])
        elif isinstance(result, dict):
            display_text = "\n".join(f"{key}: {value}" for key, value in result.items())

        use_pretty_format = tab_name != "ASCII Text"

        if use_pretty_format:
            if black_rect:
                safe_text = text.replace('<', '&lt;').replace('>', '&gt;')
                black_rect.append(f">>> {safe_text}")

                display_text_with_newlines = display_text.replace('\\n', '\n')

                if "\n" in display_text_with_newlines:
                    black_rect.append("<<<")
                    black_rect.append(display_text_with_newlines)
                else:
                    black_rect.append(f"<<< {display_text_with_newlines}")
                black_rect.append("")
        else:
            if black_rect:
                safe_display_text = display_text.replace(
                    '<', '&lt;').replace('>', '&gt;')
                black_rect.append(f"{safe_display_text}\n")

        if line_edit_to_clear:
            line_edit_to_clear.clear()

    def show_welcome_screen(self):
        self.stacked_widget.setCurrentWidget(self.pages["welcome"])
        self.home_button.hide()
        self.settings_button.show()
        self.apply_theme(is_startup=False)
        if hasattr(self, 'theme_toggle_button'):
            self.theme_toggle_button.hide()

    def show_modes_menu(self):
        if "modes" not in self.pages:
            page = QWidget()
            self._setup_modes_page(page)
            self.pages["modes"] = page
            self.stacked_widget.addWidget(page)

        self.stacked_widget.setCurrentWidget(self.pages["modes"])
        self.create_btn([
            (label, partial(self.show_submenu, label)) for label in [
                "Base Converter", "Binary Encoding", "Character Encoding", "Hashing",
                "Classical Ciphers", "Cipher Detection", "Symmetric Encryption", "Asymmetric Encryption", 
                "Random Generators", "Character Stats", "Number Analysis", "Number Checker", 
                "Unit Converter", "Color Converter"
            ]
        ])

        self._update_nav_buttons(show_home=True)
        self.history.clear() 

    def _update_nav_buttons(self, show_home=False, show_back=False, show_settings=False):
        if show_home:
            self.home_button.show()
        else:
            self.home_button.hide()

        if show_back:
            self.button_back.show()
        else:
            self.button_back.hide()

        if show_settings:
            self.settings_button.show()
        else:
            self.settings_button.hide()

    def go_back(self):
        """
        Navigates to the previous screen in the UI history.
        """
        if self._is_going_back or not self.history:
            return
        self._is_going_back = True

        current_widget = self.stacked_widget.currentWidget()
        is_dynamic_page = current_widget not in self.pages.values()

        last_state = self.history.pop()

        def execute_last_state():
            try:
                if is_dynamic_page:
                    self.stacked_widget.removeWidget(current_widget)
                    current_widget.deleteLater()
                    if hasattr(self, 'title_label'):
                        self.title_label = None 
                    self.delete_tabs()
                last_state()
                if not self.history: 
                    self._update_nav_buttons(show_home=True, show_settings=False)
                else:
                    self._update_nav_buttons(show_home=True, show_back=False, show_settings=False)
            finally:
                self._is_going_back = False

        QTimer.singleShot(0, execute_last_state)

    def _initialize_menu_definitions(self):
        """Dynamically create actions for menu definitions."""
        self.menu_definitions = {}
        for name, (menu_type, data, *rest) in MENU_DEFINITIONS.items():
            if menu_type == "vbox":
                actions = []
                for item_data in data:
                    if len(item_data) == 3:
                        label, action_key, placeholder = item_data
                    else:
                        label, action_key = item_data
                        placeholder = "Base"
                    
                    if action_key in MENU_DEFINITIONS:
                        actions.append((label, partial(self.show_submenu, label)))
                    else:
                        action_target = self.menu_definitions.get(action_key)
                        if action_target and action_target[0] == 'custom':
                            actions.append((label, action_target[1]))
                        else:
                            actions.append((label, partial(self._show_tabs_view, MENU_STRUCTURE["main"][action_key], placeholder)))
                self.menu_definitions[name] = (menu_type, actions, *rest)
            elif menu_type == "custom":
                self.menu_definitions[name] = (menu_type, getattr(self, data, None), *rest)
            else:
                self.menu_definitions[name] = (menu_type, data, *rest)

    def _setup_modes_page(self, page):
        layout = QVBoxLayout(page)
        layout.addStretch(2)
        self.title_label = self.widget_factory.create_label("Modes_")
        self.title_label.original_text = "Modes"
        self.title_label.setStyleSheet(
            STYLES["title_label"] + "margin-top: 20px; margin-bottom: 20px;")
        layout.addWidget(
            self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.menu_buttons_container = QWidget()
        self.menu_buttons_container.setFixedWidth(520)
        self.layout_buttons = QGridLayout(self.menu_buttons_container)
        self.layout_buttons.setColumnStretch(0, 1)
        self.layout_buttons.setColumnStretch(3, 1)
        self.layout_buttons.setContentsMargins(0, 0, 0, 0)
        self.layout_buttons.setHorizontalSpacing(8)
        self.layout_buttons.setVerticalSpacing(6) 
        self.menu_buttons_container.setStyleSheet("background: transparent;")
        layout.addWidget(self.menu_buttons_container,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(3)
        if hasattr(self, 'theme_toggle_button'):
            self.theme_toggle_button.hide()
        self.apply_theme(is_startup=False)

    def apply_settings(self):
        self.set_sound_volume(self.settings["volume"])
        self.update_ui_text()
        self.apply_theme()
        
    def apply_theme(self, is_startup=False):
        """
        Applies the current theme (light or dark) to all relevant UI elements.
        """
        dark_mode_enabled = self.settings.get("dark_mode", False)
        
        if dark_mode_enabled:
            self.central_widget.setStyleSheet(DARK_MODE_STYLES["background"])
            self.setStyleSheet(DARK_MODE_STYLES["app_stylesheet_dark"])
        else:
            background_style = APP_CONFIG["background_style"].replace("border-radius: 20px;", "border-radius: 0px;") if is_startup else APP_CONFIG["background_normal"]
            self.central_widget.setStyleSheet(background_style)
            self.setStyleSheet("") 
        
        button_style = DARK_MODE_STYLES["mainMenuButton_dark"] if dark_mode_enabled else STYLES["main_button"]

        for name in ["mainMenuButton", "welcomeScreenButton"]:
            for button in self.findChildren(QPushButton, name):
                button.setStyleSheet(button_style)
                button.setCursor(self.Cursor)
        
        if hasattr(self, 'volume_slider'):
            self.volume_slider.setStyleSheet(STYLES["slider"])

        key_edit_style = DARK_MODE_STYLES["line_edit"] if dark_mode_enabled else STYLES["line_edit"]
        for key_edit in self.shortcut_key_edits:
            key_edit.setStyleSheet(key_edit_style)

        if hasattr(self, 'theme_toggle_button') and self.theme_toggle_button.isVisible():
            self.update_theme_toggle_button_icon()
        
        if "color_converter" in self.pages:
            self._apply_color_converter_theme()

    def retranslate_ui(self):
        """Update the entire UI with new translations."""
        for widget in self.findChildren(QWidget):
            if hasattr(widget, 'original_text') and widget.original_text:
                try:
                    if isinstance(widget, (QPushButton, QLabel)):
                        suffix = "_" if isinstance(widget, QLabel) and widget.text().endswith("_") else ""
                        widget.setText(self.tr(widget.original_text) + suffix)
                except RuntimeError:
                    continue
        
        for combo_box in self.findChildren(QComboBox):
            if hasattr(combo_box, 'original_items'):
                try:
                    self._translate_combobox_items(combo_box)
                except RuntimeError:
                    continue
        
        if hasattr(self, 'tab') and self.tab:
            for i in range(self.tab.count()):
                tooltip_text = self.tab.tabToolTip(i)
                if tooltip_text:
                    self.tab.setTabText(i, self.tr(tooltip_text))

        self.shortcut_manager.update_shortcut_action_translations()

    def set_sound_volume(self, value):
        self.settings["volume"] = value
        volume_float = value / 100.0
        for _, audio_output in self.sound_players.values():
            audio_output.setVolume(volume_float)
        self.save_settings()

    def change_language(self, language_name):
        if self.settings.get("language") == language_name:
            return
        self.settings["language"] = language_name
        self.retranslate_ui()
        self.save_settings()

    def _translate_combobox_items(self, combo_box):
        """Helper to re-translate items in a QComboBox using its stored original items."""
        if not hasattr(combo_box, 'original_items'):
            return

        current_index = combo_box.currentIndex()
        
        combo_box.blockSignals(True)
        combo_box.clear()
        combo_box.addItems([self.tr(item) for item in combo_box.original_items])
        
        if current_index != -1:
            combo_box.setCurrentIndex(current_index)
        combo_box.blockSignals(False)

    def toggle_dark_mode(self, state):
        self.settings["dark_mode"] = bool(state)
        self.save_settings()
        self.apply_theme(is_startup=False) 

    def show_submenu(self, menu_name):
        if menu_name not in self.menu_definitions:
            return
        self.history.append(self.show_modes_menu)
        
        menu_config = self.menu_definitions.get(menu_name)
        if not menu_config: return
        menu_type, data, *rest = menu_config

        if menu_type == "custom":
            if callable(data):
                data()
                return
        
        if menu_type == "tabs":
            placeholder = self.tr(rest[0]) if rest else self.tr("Base")
            self._show_tabs_view(data, base_placeholder=placeholder)
            return

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch(1)
        self.title_label = self.widget_factory.create_label(
            self.tr(menu_name.replace("_", " ")))
        self.title_label.original_text = menu_name
        self.title_label.setStyleSheet(STYLES["title_label"])
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(30)
        original_layout_buttons = self.layout_buttons
        vbox_layout_buttons = QVBoxLayout()
        vbox_layout_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(vbox_layout_buttons)
        self.layout_buttons = vbox_layout_buttons
        btn_width = rest[0] if rest else 255
        self.create_btn(data, w=btn_width)
        self.layout_buttons = original_layout_buttons
        layout.addStretch(1)
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)
        self._update_nav_buttons(show_back=True)

        self.apply_theme(is_startup=False)
    def _show_tabs_view(self, tabs_info, base_placeholder="Base"):
        page = QWidget()
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

        self.history.append(self.show_modes_menu)
        self._update_nav_buttons(show_back=True)
        self.apply_theme(is_startup=False)

        QTimer.singleShot(0, lambda: self.create_tabs(tabs_info, 
            base_placeholder=self.tr(base_placeholder), 
            parent_widget=page, menu_name=self.title_label.original_text if hasattr(self, 'title_label') and self.title_label else None
        ))

    def update_color_result(self):
        color_text = self.line_edit_color.text().strip()
        target_format = self.combo_box_color.currentText()
        if not color_text: 
            self.result_line.append(f"! Error: {self.tr('Enter value')}\n")
            return
        try:
            result = convert_color(color_text, target_format)
            self.result_line.setFont(self.Font1)
            self.result_line.append(f"> {color_text}")
            self.result_line.append(f"< {result}")
        except ValueError as e:
            self.result_line.append(f"! Error: {e}")
        self.result_line.append("")
    
    def _show_page(self, page_name, setup_function, theme_function=None, show_home_button=False, add_to_history=False):
        """Generic method to show a page, creating it if it doesn't exist."""
        if page_name not in self.pages:
            self.pages[page_name] = setup_function(self)
            self.stacked_widget.addWidget(self.pages[page_name])

        self.stacked_widget.setCurrentWidget(self.pages[page_name])
        
        if add_to_history:
            self.history.append(self.show_modes_menu)
            self._update_nav_buttons(show_back=True)
        else:
            self._update_nav_buttons(show_home=show_home_button)

        self.apply_theme(is_startup=False)
        if theme_function:
            theme_function()

    def _show_color_converter_ui(self):
        self._show_page("color_converter", setup_color_converter_page, self._apply_color_converter_theme, add_to_history=True)

    def _apply_color_converter_theme(self):
        if "color_converter" in self.pages:
            apply_color_converter_theme(self)

    def _show_ascii_text_art_ui(self):
        self._show_page("ascii_text_art", setup_ascii_art_page, self._apply_ascii_art_theme, show_home_button=True)

    def _apply_ascii_art_theme(self):
        if "ascii_text_art" in self.pages:
            apply_ascii_art_theme(self)

    def _show_regex_visualizer_ui(self):
        self._show_page("regex_visualizer", setup_regex_visualizer_page, self._apply_regex_theme, show_home_button=True)

    def _apply_regex_theme(self):
        """Applies a specific dark theme to the regex page."""
        page = self.pages.get("regex_visualizer")
        if page:
            page.setStyleSheet("background-color: black;")
            if hasattr(self, 'regex_input'):
                self.regex_input.setStyleSheet(DARK_MODE_STYLES["line_edit"])
            if hasattr(self, 'regex_text_area'):
                self.regex_text_area.setStyleSheet(DARK_MODE_STYLES["text_edit"])

    def _show_cipher_detection_ui(self):
        self._show_page("cipher_detection", setup_cipher_detection_page, self._apply_cipher_detection_theme, add_to_history=True)
    
    def _apply_cipher_detection_theme(self):
        if "cipher_detection" in self.pages:
            apply_cipher_detection_theme(self)

    def toggle_sound(self):
        current_state = self.settings.get("sound_enabled", True)
        self.settings["sound_enabled"] = not current_state
        self.save_settings()
        self.play_sound("click")
        self.update_sound_toggle_icon()

    def show_repl_ui(self):
        self._show_page("repl", setup_repl_page, self._apply_repl_theme, show_home_button=True)

    def _apply_repl_theme(self):
        """Applies a specific dark theme to the REPL page."""
        page = self.pages.get("repl")
        if page:
            page.setStyleSheet("background-color: black;")
            self.home_button.raise_()

    def show_settings_ui(self):
        self._show_page("settings", setup_settings_page, show_home_button=True)
        self.history.clear()
        self._update_nav_buttons(show_back=True)
        self._update_nav_buttons(show_home=True)
        self._create_theme_toggle_button()