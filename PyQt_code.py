from Logic_code import *
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QTabWidget, QGridLayout, QGraphicsOpacityEffect,
    QMainWindow, QComboBox, QColorDialog, QCheckBox, QSlider, QFileDialog, QSpinBox,
    QCompleter, QStyleOptionSlider, QStyle
)
from PyQt6.QtCore import (
    QTimer, QUrl, Qt,
    QPoint, QSize, QEvent, QObject, pyqtSignal, QThread
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import (QIcon, QFont, QCursor, QPixmap,
                         QFontDatabase, QPainter, QTextCursor, QGuiApplication,
                         QTextOption, QColor)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from sys import exit, argv
import platform
import json
from PyQt6 import sip
from functools import partial, wraps
import io
import ctypes
import contextlib
import pyfiglet
import re
import os


def convert_color(color_input, target_format):
    try:
        color_input = color_input.strip().lower()
        color = QColor()
        input_type = "Unknown"

        if color_input.startswith('#'):
            color.setNamedColor(color_input)
            input_type = "HEX"
        elif color_input.startswith('rgb'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 3:
                r, g, b = map(int, values)
                color.setRgb(r, g, b)
                input_type = "RGB"
            else:
                return "Invalid RGB format. Use: rgb(255, 0, 0)"
        elif color_input.startswith('hsl'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 3:
                h, s, l = map(int, values)
                color.setHsl(h % 360, s * 255 // 100, l * 255 // 100)
                input_type = "HSL"
            else:
                return "Invalid HSL format. Use: hsl(360, 100, 100)"
        elif color_input.startswith('hsv'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 3:
                h, s, v = map(int, values)
                color.setHsv(h % 360, s * 255 // 100, v * 255 // 100)
                input_type = "HSV"
            else:
                return "Invalid HSV format. Use: hsv(360, 100, 100)"
        elif color_input.startswith('cmyk'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 4:
                c, m, y, k = map(int, values)
                color.setCmyk(c * 255 // 100, m * 255 // 100,
                              y * 255 // 100, k * 255 // 100)
                input_type = "CMYK"
        else:
            color.setNamedColor(color_input)
            if not color.isValid():
                color.setNamedColor('#' + color_input)
            if color.isValid():
                input_type = "HEX"
        if not color.isValid():
            return "Invalid color input. Use hex (#FF0000), rgb(255,0,0), or color names."
        if target_format == input_type:
            return color_input
        if target_format == "RGB":
            return f"rgb({color.red()}, {color.green()}, {color.blue()})"
        elif target_format == "HSL":
            h, s, l, _ = color.getHslF()
            return f"hsl({round(h*360)}, {round(s*100)}%, {round(l*100)}%)"
        elif target_format == "HSV":
            h, s, v, _ = color.getHsvF()
            return f"hsv({round(h*360)}, {round(s*100)}%, {round(v*100)}%)"
        elif target_format == "CMYK":
            c, m, y, k, _ = color.getCmykF()
            return f"cmyk({round(c*100)}%, {round(m*100)}%, {round(y*100)}%, {round(k*100)}%)"
        elif target_format == "HEX":
            return color.name()
        else:
            return f"Unknown conversion target: {target_format}"
    except Exception as e:
        return f"Error: {str(e)}"


class Worker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class HoverSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        handle_rect = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt,
                                                  QStyle.SubControl.SC_SliderHandle, self)
        if handle_rect.contains(event.pos()):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()

        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.unsetCursor()
        super().leaveEvent(event)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_CONFIG["window_title"])
        self.setFixedSize(*APP_CONFIG["window_size"])
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        IS_WINDOWS = platform.system() == "Windows"
        if IS_WINDOWS:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.central_widget.setStyleSheet(APP_CONFIG["background_style"])
        else:
            style_no_radius = APP_CONFIG["background_style"].replace(
                "border-radius: 20px;", "border-radius: 0px;")
            self.central_widget.setStyleSheet(style_no_radius)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout_buttons = QVBoxLayout()
        if os.path.exists("/usr/share/alterm-app"):
            self.assets_dir = "/usr/share/alterm-app/assets"
            self.app_data_dir = "/usr/share/alterm-app/data"
        else:
            self.assets_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "assets")
            self.app_data_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "data")
        self.user_data_dir = os.path.expanduser("~/.config/alterm-app")
        self.buttons_layout_index = 1
        self.layout_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(5, 5, 5, 10)
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
            self.Font1.setPointSize(8)
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

        self.audio_output = QAudioOutput()
        self.sound_outputs = []
        self.sound_players = {}
        self.Image_url = os.path.join(
            self.assets_dir, "icons", "logo Alterm Appv2.svg")
        self.sounds = {
            "intro": os.path.join(self.assets_dir, "sounds", "sound_intro.mp3"),
            "tab": os.path.join(self.assets_dir, "sounds", "sound_tab.mp3"),
            "click": os.path.join(self.assets_dir, "sounds", "sound_1.mp3"),
            "back": os.path.join(self.assets_dir, "sounds", "sound_2.mp3")
        }
        self.Icon_url = os.path.join(
            self.assets_dir, "icons", "alterm-app.png")
        self.Copy_svg = os.path.join(
            self.assets_dir, "icons", "Copy_button.svg")
        self.Copied_svg = os.path.join(
            self.assets_dir, "icons", "Copied_button.svg")
        self.palette_svg_path = os.path.join(
            self.assets_dir, "icons", "palette.svg")
        self.setWindowIcon(QIcon(self.Icon_url))
        for name, path in self.sounds.items():
            self.add_sound_player(name, path)
        self.repl_context = {
            "__builtins__": __builtins__,
            "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
            "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10
        }

        if IS_WINDOWS:
            def window_button_style(icon_path, hover_icon_path):
                return f"""
                    QPushButton {{
                        background: transparent;
                        border: none;
                        icon: url('{icon_path}');
                    }}
                    QPushButton:hover {{
                        icon: url('{hover_icon_path}');
                    }}
                """

            self.button_X = QPushButton(self)
            self.button_X.setStyleSheet(window_button_style(
                self.close_icon_path, self.close_icon_red_path))
            self.button_X.setFixedSize(30, 30)
            self.button_X.clicked.connect(self.close)

            self.button_min = QPushButton(self)
            self.button_min.setStyleSheet(window_button_style(
                self.minimize_icon_path, self.minimize_icon_red_path))
            self.button_min.setFixedSize(30, 30)
            self.button_min.clicked.connect(self.showMinimized)

            self.button_min.setParent(self.central_widget)
            self.button_X.setParent(self.central_widget)
            self.button_min.move(self.width() - 70, 5)
            self.button_X.move(self.width() - 35, 5)
            self.button_min.raise_()

        self.Title = QLabel("CodeKit_")
        self.Title.setStyleSheet(STYLES["title_label"])
        self.Title.setFixedWidth(140)
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

        self.button = QPushButton(self.tr("Modes"), self)
        self.button.setStyleSheet(STYLES["main_button"])
        self.button.setCursor(self.Cursor)
        self.button.setFont(self.Font2)
        self.button.setFixedWidth(200)
        self.opacity_button = QGraphicsOpacityEffect()
        self.opacity_button.setOpacity(0)
        self.button.clicked.connect(self.show_modes_menu)
        self.button.clicked.connect(partial(self.play_sound, "click"))

        self.repl_button_main = QPushButton(self.tr("Python Terminal"), self)
        self.repl_button_main.setStyleSheet(STYLES["main_button"])
        self.repl_button_main.setCursor(self.Cursor)
        self.repl_button_main.setFont(self.Font2)
        self.repl_button_main.setFixedWidth(200)
        self.repl_button_main.clicked.connect(self.show_repl_ui)
        self.repl_button_main.clicked.connect(
            partial(self.play_sound, "click"))

        self.ascii_art_button_main = QPushButton(
            self.tr("ASCII Art Generator"), self)
        self.ascii_art_button_main.setStyleSheet(STYLES["main_button"])
        self.ascii_art_button_main.setCursor(self.Cursor)
        self.ascii_art_button_main.setFont(self.Font2)
        self.ascii_art_button_main.setFixedWidth(200)
        self.ascii_art_button_main.clicked.connect(self._show_ascii_art_ui)
        self.ascii_art_button_main.clicked.connect(
            partial(self.play_sound, "click"))

        self.layout.addStretch(2)
        self.layout.addSpacing(40)
        self.layout.addWidget(
            self.image, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.Title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(
            self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.repl_button_main,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.ascii_art_button_main,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(3)

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

        self.apply_settings()

    def _capture_output(self, func, *args, **kwargs):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                func(*args, **kwargs)
            stdout = stdout_capture.getvalue()
            stderr = stderr_capture.getvalue()
            if stderr:
                return f"{stdout}\nError: {stderr}"
            return stdout
        except Exception as e:
            return f"Exception: {e}"

    def _execute_python_code(self):
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
        audio_output = QAudioOutput()
        player = QMediaPlayer()
        player.setAudioOutput(audio_output)
        player.setSource(QUrl.fromLocalFile(path))
        self.sound_players[name] = (player, audio_output)
        self.sound_outputs.append(audio_output)

    def play_sound(self, sound_name: str):
        if self.settings["sound_enabled"]:
            current_player, _ = self.sound_players.get(
                sound_name, (None, None))
            if current_player and current_player.isPlaying():
                current_player.stop()

            player, _ = self.sound_players.get(sound_name, (None, None))
            if player:
                player.setPosition(0)
                player.play()

    def tr(self, text_key):
        return self.translations.get(self.settings.get("language", "English"), {}).get(text_key, text_key)

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {
                "sound_enabled": True,
                "volume": 80,
                "language": "English"
            }
            self.save_settings()

    def save_settings(self):
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)

    def load_translations(self):
        try:
            with open(self.translations_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.translations = {}
            # Create a dummy entry if file is missing

    def copy_text(self, widget, button):
        if isinstance(widget, QTextEdit):
            text = widget.toPlainText()
            QApplication.clipboard().setText(text)
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
        if hasattr(self, 'repl_input') and obj is self.repl_input and event.type() == QEvent.Type.KeyPress and self.repl_input.isVisible():
            cursor = self.repl_input.textCursor()
            key = event.key()
            text = event.text()
            pairs = {"(": ")", "[": "]", "{": "}", "'": "'", '"': '"'}
            if text in pairs:
                cursor.insertText(text + pairs[text])
                cursor.movePosition(
                    QTextCursor.MoveOperation.PreviousCharacter)
                self.repl_input.setTextCursor(cursor)
                return True
            elif key == Qt.Key.Key_Backspace and not cursor.hasSelection():
                pos = cursor.position()
                if pos > 0:
                    doc = self.repl_input.document()
                    char_before = doc.characterAt(pos - 1)
                    char_after = doc.characterAt(pos)
                    if char_before in pairs and pairs.get(char_before) == char_after:
                        cursor.movePosition(
                            QTextCursor.MoveOperation.PreviousCharacter)
                        cursor.movePosition(
                            QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor, 2)
                        cursor.removeSelectedText()
                        return True
            elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                    self.repl_input.insertPlainText("\n")
                else:
                    self._execute_python_code()
                return True
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Type.KeyPress and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() != Qt.KeyboardModifier.ShiftModifier:
                for info in getattr(self, "_asym_text_edits", []):
                    if info.get("input_edit") is obj:
                        self.update_black_rect(
                            info["input_edit"],
                            info["self.black_rect"],
                            base_input=info["base_input"],
                            tab_name=info["tab_name"],
                            mode_selector=None,
                            Encryption_2=True
                        )
                        return True
        return super().eventFilter(obj, event)

    def _generate_keys(self, tab_name: str, black_rect: QTextEdit, key_size_input: QWidget = None):
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
            self.black_rect.append(f"> generate (param={ks})")
            processed_res = str(res).replace('\n', '').replace('\r', '')
            processed_res = processed_res.replace(
                "PRIVATE KEY:", "\n\nPRIVATE KEY:")
            processed_res = processed_res.replace(
                "-----BEGIN", "\n-----BEGIN").replace("-----END", "\n-----END")
            processed_res = processed_res.replace("KEY-----", "KEY-----\n")
            self.black_rect.append(f"< {processed_res}\n")
            QApplication.restoreOverrideCursor()
            self.thread.quit()
            self.thread.wait()

        def on_error(err_msg):
            self.black_rect.append(f"! Error: {err_msg}\n")
            QApplication.restoreOverrideCursor()
            self.thread.quit()
            self.thread.wait()

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self.thread = QThread()
        self.worker = Worker(generation_task)
        self.worker.moveToThread(self.thread)

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

    def create_btn(self, buttons_info, copy_btn=False, w=230, h=45, style=STYLES["menu_button"], return_btn=False):
        self.delete_button()
        if copy_btn:
            copy_button = QPushButton(self.tr("Copy"), self.black_rect)
            copy_button.setStyleSheet(STYLES["copy_button"])
            copy_button.setIcon(QIcon(self.Copy_svg))
            copy_button.setIconSize(QSize(17, 17))
            copy_button.setFont(self.Font2)
            copy_button.setFixedSize(100, 40)
            copy_button.move(580, 5)
            copy_button.show()
            copy_button.raise_()
            copy_button.setCursor(Qt.CursorShape.DragCopyCursor)
            copy_button.clicked.connect(
                partial(self.copy_text, self.black_rect, copy_button))
        else:
            for idx, (label, function) in enumerate(buttons_info):
                button = QPushButton(self.tr(label), self)
                button.original_text = label
                button.clicked.connect(function)
                button.clicked.connect(partial(self.play_sound, "click"))
                button.setStyleSheet(style)
                button.setCursor(self.Cursor)
                button.setFont(self.Font2)
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

    def return_label(self, text: str):
        label = QLabel(text)
        label.setFont(self.Font3)
        label.setStyleSheet(STYLES["title_label"])
        return label

    def clear_layout_buttons(self):
        while self.layout_buttons.count():
            item = self.layout_buttons.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self.button_dyna.clear()

    def is_braille(self, text):
        return any(c in BRAILLE_CHARS for c in text)

    def return_line_edit(self, w=700, h=45, style=STYLES["line_edit"], placeholder=None, text_edit=False):
        if not text_edit:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(placeholder)
            line_edit.setFont(self.Font3)
            line_edit.setFixedSize(w, h)
            line_edit.setStyleSheet(style)
            line_edit.setFocus()
            return line_edit
        else:
            line_edit = QTextEdit()
            line_edit.setPlaceholderText(placeholder)
            line_edit.setFont(self.Font3)
            line_edit.setFixedSize(w, h)
            line_edit.setStyleSheet(style)
            return line_edit

    def return_black_rect(self, w=700, h=350, style=STYLES["text_edit"]):
        black_rect = QTextEdit()
        black_rect.setFixedSize(w, h)
        black_rect.setStyleSheet(style)
        black_rect.setReadOnly(True)
        black_rect.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        black_rect.setFontFamily(self.family1)
        black_rect.setViewportMargins(0, 0, 120, 0)
        black_rect.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        return black_rect

    def return_combo_box(self, w=140, h=45, Items_list=["Text → Base", "Base → Text"], editable=False, read_only_text=False):
        mode_selector = QComboBox()
        mode_selector.addItems(Items_list)
        mode_selector.setFont(self.Font2)
        mode_selector.setEditable(True)
        line_edit = mode_selector.lineEdit()
        line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_edit.setReadOnly(not editable or read_only_text)
        mode_selector.setFixedSize(w, h)
        mode_selector.setCursor(self.Cursor)
        mode_selector.view().setCursor(self.Cursor)
        style = STYLES["combo_box"].format(
            arrow_down_path=self.arrow_down_path, arrow_up_path=self.arrow_up_path)
        mode_selector.setStyleSheet(style)
        return mode_selector

    def return_non_editable_combo_box(self, w=140, h=45, Items_list=[]):
        combo_box = QComboBox()
        combo_box.addItems(Items_list)
        combo_box.setFont(self.Font2)
        combo_box.setEditable(False)
        combo_box.setFixedSize(w, h)
        combo_box.setCursor(self.Cursor)
        combo_box.view().setCursor(self.Cursor)

        # Utilise un style dédié pour les combobox non éditables
        style = STYLES["non_editable_combo_box"].format(
            arrow_down_path=self.arrow_down_path, arrow_up_path=self.arrow_up_path
        )
        combo_box.setStyleSheet(style)
        return combo_box

    def return_spin_box(self, w=94, h=45, min_val=0, max_val=999999, placeholder=""):
        spin_box = QSpinBox()
        spin_box.setRange(min_val, max_val)
        spin_box.setFont(self.Font3)
        spin_box.setFixedSize(w, h)
        spin_box.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        spin_box.lineEdit().setPlaceholderText(placeholder)
        spin_box.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        style = STYLES["spin_box"].format(
            arrow_up_path=self.arrow_up_path, arrow_down_path=self.arrow_down_path)
        spin_box.setStyleSheet(style)
        return spin_box

    def create_tabs(self, tabs_info, base_placeholder="Base"):
        self.delete_tabs()
        self.tab = QTabWidget()
        self.tab.setTabPosition(QTabWidget.TabPosition.South)
        self.tab.setMovable(False)
        self.tab.setTabsClosable(False)
        self.tab.setStyleSheet(STYLES["tab_widget"])
        self.tab.setFont(self.Font2)
        self.tab.tabBar().setCursor(self.Cursor)
        for name, placeholder in tabs_info:
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            Title_Label = QLabel(self.tr(name))
            Title_Label.setFont(self.Font3)
            Title_Label.setObjectName("tabTitleLabel")
            Title_Label.original_text = name
            Title_Label.setStyleSheet(STYLES["tab_title"])
            Title_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            layout.addWidget(Title_Label)
            self.black_rect = self.return_black_rect()
            translated_placeholder = self.tr(placeholder)
            if any(keyword in name for keyword in UI_KEYWORDS_WITH_BASE) and name not in ["Divisibility Checker"]:
                hbox = QHBoxLayout()
                line_edit = self.return_line_edit(
                    w=600, h=45, placeholder=translated_placeholder)
                hbox.addWidget(line_edit)
                if name == "Custom":
                    base_input = self.return_spin_box(
                        min_val=2, max_val=len(digits), placeholder=base_placeholder)
                elif name == "ROT-N":
                    base_input = self.return_spin_box(
                        min_val=-25, max_val=25, placeholder=base_placeholder)
                else:
                    base_input = self.return_line_edit(
                        w=94, h=45, placeholder=base_placeholder)

                hbox.addWidget(base_input)
                layout.addLayout(hbox)
                if name in ("ROT-N", "Custom"):
                    line_edit.returnPressed.connect(
                        partial(self.update_black_rect, line_edit, self.black_rect, base_input, name, None))
                    base_input.returnPressed.connect(
                        partial(self.update_black_rect, line_edit, self.black_rect, base_input, name, None))
                else:
                    line_edit.returnPressed.connect(
                        partial(self.update_black_rect, line_edit, self.black_rect, base_input, name, None, None, True))
                    base_input.returnPressed.connect(
                        partial(self.update_black_rect, line_edit, self.black_rect, base_input, name, None, None, True))
            elif any(k in name for k in ("RSA", "ECC", "ElGamal")):
                # Container for generation controls
                gen_controls_container = QWidget()
                gen_controls_layout = QHBoxLayout(gen_controls_container)
                gen_controls_layout.setContentsMargins(0, 0, 0, 0)
                gen_controls_layout.setSpacing(10)
                gen_controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                if "Generate" in name:
                    gen_btn = QPushButton(self.tr("Generate"))
                    gen_btn.setCursor(self.Cursor)
                    gen_btn.setFont(self.Font2)
                    gen_btn.setFixedSize(190, 45)
                    gen_btn.setStyleSheet(STYLES["menu_button"])

                    key_size_input = None
                    gen_btn.clicked.connect(
                        partial(self.play_sound, "click"))
                    if "ECC" in name:
                        key_size_input = self.return_combo_box(
                            w=250, Items_list=["SECP256R1", "SECP384R1", "SECP521R1", "SECP256K1"])
                    else:
                        key_size_input = self.return_combo_box(
                            w=250, Items_list=["2048", "4096"])
                    layout.addWidget(self.black_rect)
                    gen_btn.clicked.connect(
                        partial(self._generate_keys, name, self.black_rect, key_size_input))
                    self.create_btn(None, True, 580, 5)
                    short_name = self.short_names.get(name, name)
                    index = self.tab.addTab(widget, self.tr(short_name))
                    gen_controls_layout.addWidget(key_size_input)
                    gen_controls_layout.addWidget(gen_btn)
                    layout.insertWidget(1, gen_controls_container,
                                        alignment=Qt.AlignmentFlag.AlignHCenter)
                    self.tab.setTabToolTip(index, name)
                    continue

                hbox = QHBoxLayout()
                line_edit = self.return_line_edit(
                    style=STYLES["line_edit_v2"], text_edit=True, w=350, h=150, placeholder=translated_placeholder)
                line_edit.setLineWrapMode(
                    QTextEdit.LineWrapMode.FixedColumnWidth)
                line_edit.setLineWrapColumnOrWidth(30)
                line_edit.setAcceptRichText(False)
                hbox.addWidget(line_edit)
                base_input = QTextEdit()
                if "Encrypt" in name:
                    base_input.setPlaceholderText(self.tr("Public Key"))
                elif "Decrypt" in name:
                    base_input.setPlaceholderText(self.tr("Private Key"))
                else:
                    base_input.setPlaceholderText(base_placeholder)
                base_input.setFont(self.Font3)
                base_input.setFixedSize(340, 150)
                base_input.setStyleSheet(STYLES["line_edit_v2"])
                base_input.setLineWrapMode(
                    QTextEdit.LineWrapMode.FixedColumnWidth)
                base_input.setLineWrapColumnOrWidth(30)
                base_input.setAcceptRichText(False)
                hbox.addWidget(base_input)
                layout.addLayout(hbox) 
                layout.addWidget(self.black_rect)
                run_button = QPushButton(self.tr("Run"), widget)
                run_button.setCursor(self.Cursor)
                run_button.setFont(self.Font2)
                run_button.setFixedSize(90, 34)
                run_button.setStyleSheet(STYLES["Run_Button"])
                run_button.clicked.connect(partial(
                    self.update_black_rect, line_edit, self.black_rect, base_input, name, None, Encryption_1=True))
                x_pos = line_edit.x() + line_edit.width() - run_button.width() + 20
                y_pos = line_edit.y() + line_edit.height() + 15
                run_button.move(x_pos, y_pos)
                run_button.show()
                if not hasattr(self, "_asym_text_edits"):
                    self._asym_text_edits = []
                self._asym_text_edits.append({
                    "input_edit": line_edit,
                    "self.black_rect": self.black_rect,
                    "base_input": base_input,
                    "tab_name": name
                })
                self.create_btn(None, True)
                short_name = self.short_names.get(name, name)
                index = self.tab.addTab(widget, self.tr(short_name))
                self.line_edits.append(line_edit)
            elif any(k in name for k in UI_KEYWORDS_BINARY_ENCODING):
                line_edit = self.return_line_edit(
                    w=550, h=45, placeholder=translated_placeholder)
                mode_selector = self.return_combo_box()
                hbox = QHBoxLayout()
                hbox.addWidget(line_edit)
                hbox.addWidget(mode_selector)
                layout.addLayout(hbox)
                line_edit.returnPressed.connect(partial(
                    self.update_black_rect, line_edit, self.black_rect, None, name, mode_selector))
            elif name in UNIT_CATEGORIES:
                line_edit = self.return_line_edit(
                    w=490, h=45, placeholder=translated_placeholder)
                self.Item_list_1, self.Item_list_2 = Unit_Items.get(
                    name, ([], []))
                mode_selector = self.return_combo_box(
                    w=100, Items_list=self.Item_list_1)
                mode_selector_2 = self.return_combo_box(
                    w=100, Items_list=self.Item_list_2)
                hbox = QHBoxLayout()
                hbox.addWidget(line_edit)
                hbox.addWidget(mode_selector)
                hbox.addWidget(mode_selector_2)
                layout.addLayout(hbox)
                line_edit.returnPressed.connect(partial(
                    self.update_black_rect, line_edit, self.black_rect, None, name, mode_selector=mode_selector, mode_selector_2=mode_selector_2))
            elif any(k in name for k in UI_KEYWORDS_ANALYZERS):
                mode_selector = None  # Default to no mode selector
                text_edit_container = QWidget()
                text_edit_layout = QVBoxLayout(text_edit_container)
                text_edit_layout.setContentsMargins(0, 0, 0, 0)
                text_edit_layout.setSpacing(0)
                line_edit = self.return_line_edit(
                    style=STYLES["line_edit_v2"], text_edit=True, w=700, h=200, placeholder=translated_placeholder)
                line_edit.setViewportMargins(0, 0, 110, 0)
                text_edit_layout.addWidget(line_edit)
                run_button = QPushButton(self.tr("Run"), line_edit)
                run_button.setCursor(self.Cursor)
                run_button.setFont(self.Font2)
                run_button.setFixedSize(90, 34)
                run_button.setStyleSheet(STYLES["Run_Button"])
                run_button.move(line_edit.width() - run_button.width() - 8, 10)
                layout.addWidget(text_edit_container)
                run_button.clicked.connect(partial(
                    self.update_black_rect, line_edit, self.black_rect, None, name, mode_selector=mode_selector
                ))

                if name == "Syntax Analysis":
                    mode_selector = self.return_combo_box(
                        w=700, Items_list=list(LANGUAGE_PATTERNS.keys()))
                    layout.addWidget(mode_selector)
                    run_button.clicked.disconnect()
                    run_button.clicked.connect(partial(
                        self.update_black_rect, line_edit, self.black_rect, None, name, mode_selector
                    ))

                if name == "Language Detection":
                    self.black_rect.setFixedHeight(220 + 45 + 10)
                else:
                    self.black_rect.setFixedHeight(220)
            else:
                if name == "Divisibility Checker":
                    base_input = None
                    hbox = QHBoxLayout() 
                    line_edit = self.return_line_edit(
                        w=600, h=45, placeholder=self.tr("Enter Number"))
                    base_input = self.return_line_edit(w=94, h=45, placeholder=self.tr("Divider"))
                    hbox.addWidget(line_edit)
                    hbox.addWidget(base_input)
                    layout.addLayout(hbox)
                else:
                    base_input = None
                    line_edit = self.return_line_edit(
                        placeholder=translated_placeholder)
                    layout.addWidget(line_edit)
                line_edit.returnPressed.connect(
                    partial(self.update_black_rect, line_edit, self.black_rect, base_input if name == "Divisibility Checker" else None, name, None))
            layout.addWidget(self.black_rect)
            layout.addStretch(1)
            self.create_btn(None, True, 580, 5)
            short_name = self.short_names.get(name, name)
            index = self.tab.addTab(widget, self.tr(short_name))
            self.line_edits.append(line_edit)
            self.tab.setTabToolTip(index, name)

        try:
            self.tab.currentChanged.disconnect()
        except TypeError:
            pass

        self.layout.addWidget(self.tab)
        self.tab.show()
        self.tab.currentChanged.connect(partial(self.play_sound, "tab"))

    def update_black_rect(self, line_edit, black_rect, base_input=None, tab_name=None, mode_selector=None, mode_selector_2=None, Encryption_1=False, Encryption_2=False):
        if isinstance(line_edit, QTextEdit):
            text = line_edit.toPlainText().strip()
        else:
            text = line_edit.text().strip()
        if not text:
            return
        result = ""
        base_value = None
        if Encryption_1:
            if isinstance(base_input, QTextEdit):
                Key = base_input.toPlainText().strip()
            else:
                Key = base_input.text().strip()
            if Key.isascii():
                base_value = str(Key)
        elif Encryption_2:
            if isinstance(base_input, QTextEdit):
                Key = base_input.toPlainText().strip()
            else:
                Key = base_input.text().strip()
            if Key.isascii():
                base_value = str(Key)
        elif base_input:
            if isinstance(base_input, QTextEdit):
                base_text = base_input.toPlainText().strip()
            else:
                base_text = base_input.text().strip()
            if base_text.isdigit():
                base_value = int(base_text)

        def conversion_task():
            mode = mode_selector.currentText() if mode_selector else None
            mode2 = mode_selector_2.currentText() if mode_selector_2 else None
            result = detect_conversion_type(
                text, tab_name, base=base_value, mode=mode, mode2=mode2)
            return result

        def on_finished(result):
            self.display_result(result, text, tab_name, black_rect, line_edit)
            QApplication.restoreOverrideCursor()
            self.thread.quit()
            self.thread.wait()

        def on_error(err_msg):
            try:
                self.display_result(
                    f"! Error: {err_msg}", text, tab_name, black_rect, line_edit)
            finally:
                QApplication.restoreOverrideCursor()
                self.thread.quit()
                self.thread.wait()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.thread = QThread()
        self.worker = Worker(conversion_task)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(on_finished)
        self.worker.error.connect(on_error)
        self.thread.start()

    def display_result(self, result, text, tab_name, black_rect, line_edit_to_clear=None):
        if result is None:
            result = "! Error: empty result"
        preserve_newlines = any(generator in tab_name for generator in [
            "Random Equation Generator",
            "Random ID Generator",
            "Random IP Generator",
            "Coprimes Generator"
        ]) or tab_name in UNIT_CATEGORIES
        if isinstance(result, bytes):
            display_text = result.decode("utf-8", errors="replace")
        else:
            display_text = str(result)

        if self.is_braille(display_text) and black_rect and not sip.isdeleted(black_rect):
            black_rect.setFontFamily(
                getattr(self, "family_braille", "DejaVu Sans"))

        use_pretty_format = (tab_name not in UI_KEYWORDS_ANALYZERS and
                             not preserve_newlines and
                             tab_name != "ASCII Art")

        if use_pretty_format:
            if black_rect and not sip.isdeleted(black_rect):
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
            if black_rect and not sip.isdeleted(black_rect):
                safe_display_text = display_text.replace(
                    '<', '&lt;').replace('>', '&gt;')
                black_rect.append(f"{safe_display_text}\n")

        if line_edit_to_clear and not sip.isdeleted(line_edit_to_clear):
            line_edit_to_clear.clear()

    def show_welcome_screen(self):
        self.clear_all_widgets()

        # Recréer les widgets de l'écran d'accueil pour éviter les erreurs de référence
        self.Title = QLabel("CodeKit_")
        self.Title.setStyleSheet(STYLES["title_label"])
        self.Title.setFixedWidth(140)
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

        self.button = QPushButton(self.tr("Modes"), self)
        self.button.setStyleSheet(STYLES["main_button"])
        self.button.setCursor(self.Cursor)
        self.button.setFont(self.Font2)
        self.button.setFixedWidth(200)
        self.button.clicked.connect(self.show_modes_menu)
        self.button.clicked.connect(partial(self.play_sound, "click"))

        self.repl_button_main = QPushButton(self.tr("Python Terminal"), self)
        self.repl_button_main.setStyleSheet(STYLES["main_button"])
        self.repl_button_main.setCursor(self.Cursor)
        self.repl_button_main.setFont(self.Font2)
        self.repl_button_main.setFixedWidth(200)
        self.repl_button_main.clicked.connect(self.show_repl_ui)
        self.repl_button_main.clicked.connect(
            partial(self.play_sound, "click"))

        self.ascii_art_button_main = QPushButton(
            self.tr("ASCII Art Generator"), self)
        self.ascii_art_button_main.setStyleSheet(STYLES["main_button"])
        self.ascii_art_button_main.setCursor(self.Cursor)
        self.ascii_art_button_main.setFont(self.Font2)
        self.ascii_art_button_main.setFixedWidth(200)
        self.ascii_art_button_main.clicked.connect(self._show_ascii_art_ui)
        self.ascii_art_button_main.clicked.connect(
            partial(self.play_sound, "click"))

        if platform.system() == "Windows":
            self.central_widget.setStyleSheet(APP_CONFIG["background_style"])
        else:
            style_no_radius = APP_CONFIG["background_style"].replace(
                "border-radius: 20px;", "border-radius: 0px;")
            self.central_widget.setStyleSheet(style_no_radius)
        self.layout.setContentsMargins(5, 5, 5, 10)
        self.layout.addStretch(2)
        self.layout.addSpacing(40)
        self.layout.addWidget(
            self.image, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.Title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(
            self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.repl_button_main,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.ascii_art_button_main,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(3)
        self.home_button.hide()
        self.settings_button.show()

    def show_modes_menu(self):
        self.clear_all_widgets()
        self.hide_intro()
        self.button_back.hide()
        self.home_button.show()

    def go_back(self):
        if not self.history:
            return
        last_state = self.history.pop()
        QTimer.singleShot(0, last_state)

    def delete_button(self):
        for button in self.button_dyna:
            self.layout_buttons.removeWidget(button)
            button.deleteLater()
        self.button_dyna.clear()

    def delete_label(self):
        if hasattr(self, 'title_label') and self.title_label:
            self.layout.removeWidget(self.title_label)
            self.title_label.deleteLater()
            del self.title_label

    def _delete_menu_container(self):
        if hasattr(self, "menu_buttons_container"):
            self.layout.removeWidget(self.menu_buttons_container)
            self.menu_buttons_container.deleteLater()
            del self.menu_buttons_container

    def delete_tabs(self):
        if hasattr(self, "tab"):
            if self.tab.parent() == self.central_widget:
                self.layout.removeWidget(self.tab)
            self.tab.hide()
            while self.tab.count() > 0:
                widget = self.tab.widget(0)
                self.tab.removeTab(0)
                widget.deleteLater()

    def delete_color_widget(self):
        for widget in self.color_widgets:
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.color_widgets.clear()

    def hide_intro(self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget():
                item.widget().hide()
            self.layout.removeItem(item)
        self.layout.addStretch(2)
        self.title_label = self.return_label("Modes_")
        self.title_label.original_text = "Modes"
        self.title_label.setStyleSheet(
            STYLES["title_label"] + "margin-top: 20px; margin-bottom: 20px;")
        self.layout.addWidget(
            self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.menu_buttons_container = QWidget()
        self.menu_buttons_container.setFixedWidth(500)
        self.layout_buttons = QGridLayout(self.menu_buttons_container)
        self.layout_buttons.setColumnStretch(0, 1)
        self.layout_buttons.setColumnStretch(3, 1)
        self.layout_buttons.setContentsMargins(0, 0, 0, 0)
        self.layout_buttons.setHorizontalSpacing(5)
        self.layout_buttons.setVerticalSpacing(6)
        self.menu_buttons_container.setStyleSheet("background: transparent;")
        self.central_widget.setStyleSheet(APP_CONFIG["background_normal"])
        self.layout.addWidget(self.menu_buttons_container,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.settings_button.hide()
        self.layout.addStretch(3)
        self.home_button.show()

        def create_tabs_action(menu_key, placeholder="Base"):
            return partial(self._show_tabs_view, MENU_STRUCTURE["main"][menu_key], placeholder)

        self.menu_definitions = {
            "Base Converter": ("vbox", [("Binary", create_tabs_action("Binary")), ("Octal", create_tabs_action("Octal")), ("Hexadecimal", create_tabs_action("Hexadecimal")), ("Custom Base", create_tabs_action("Custom", "Base")), ("Roman Num", create_tabs_action("Roman Num"))]),
            "Binary Encoding": ("tabs", MENU_STRUCTURE["main"]["bases"]),
            "Character Encoding": ("vbox", [("ASCII", create_tabs_action("ASCII")), ("UTF-N", create_tabs_action("UTF-N", "N")), ("ISO", create_tabs_action("ISO", "N"))]),
            "Hashing": ("vbox", [("Cryptographic", create_tabs_action("hash")), ("Checksum", create_tabs_action("cheksum"))]),
            "Random Generators": ("tabs", MENU_STRUCTURE["main"]["Random"], "Enter number"),
            "Character Stats": ("tabs", MENU_STRUCTURE["main"]["Character and Symbol"], "Enter Text"),
            "Number Analysis": ("tabs", MENU_STRUCTURE["main"]["Number analysis"], "Enter Numbers"),
            "Number Checker": ("tabs", MENU_STRUCTURE["main"]["Number Checker"], "Enter Number"),
            "Unit Converter": ("tabs", MENU_STRUCTURE["main"]["Unit Converter"], "Enter value"),
            "Color Converter": ("custom", self._show_color_converter_ui),
            "Code Analyzer": ("tabs", MENU_STRUCTURE["main"]["Code Analyzer"]),
            "Classical Ciphers": ("vbox", [("Morse", create_tabs_action("Morse")), ("Braille", create_tabs_action("Braille")), ("Grid Cipher", create_tabs_action("Grid Cipher")), ("Emoji Cipher", create_tabs_action("Emoji Cipher")), ("Affine Cipher", create_tabs_action("Affine Cipher")), ("ROT-N", create_tabs_action("ROT-N", "N"))]),
            "Symmetric Encryption": ("vbox", [("AES", create_tabs_action("AES", "Key")), ("ChaCha20", create_tabs_action("ChaCha20", "Key")), ("DES", create_tabs_action("DES", "Key")), ("3DES", create_tabs_action("3DES", "Key")), ("Blowfish", create_tabs_action("Blowfish", "Key"))]),
            "Asymmetric Encryption": ("vbox", [("RSA", create_tabs_action("RSA", "Key Size")), ("ECC", create_tabs_action("ECC", "Curve")), ("ElGamal", create_tabs_action("ElGamal", "Key Size"))]),
            "Hashing": ("vbox", [("Cryptographic", create_tabs_action("hash")), ("Checksum", create_tabs_action("cheksum"))]),
        }
        self.create_btn([
            (label, partial(self.show_submenu, label)) for label in [
                "Base Converter", "Binary Encoding", "Character Encoding", "Hashing",
                "Classical Ciphers", "Symmetric Encryption", "Asymmetric Encryption", "Random Generators",
                "Character Stats", "Number Analysis", "Number Checker", "Unit Converter", "Color Converter", "Code Analyzer"
            ]
        ])

    def show_settings_ui(self):
        self.clear_all_widgets()
        self.settings_button.hide()
        self.history.append(self.show_welcome_screen)
        self.central_widget.setStyleSheet(APP_CONFIG["background_normal"])
        self.home_button.show()

        title = self.return_label(self.tr("Settings"))
        title.setStyleSheet(STYLES["title_label"] + "margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        settings_container = QWidget()
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(15)
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(title)

        self.sound_checkbox = QCheckBox(self.tr("Enable Sound"))
        self.sound_checkbox.setFont(self.Font2)
        self.sound_checkbox.setStyleSheet(STYLES["checkbox"])
        self.sound_checkbox.setChecked(self.settings["sound_enabled"])
        self.sound_checkbox.setCursor(self.Cursor)
        self.sound_checkbox.stateChanged.connect(self.toggle_sound)
        settings_layout.addWidget(
            self.sound_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        volume_label = self.return_label(self.tr("Sound Volume"))
        volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(volume_label)

        self.volume_slider = HoverSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.settings["volume"])
        self.volume_slider.setFixedWidth(200)
        self.volume_slider.setStyleSheet(STYLES["slider"])
        self.volume_slider.valueChanged.connect(self.set_sound_volume)
        settings_layout.addWidget(
            self.volume_slider, alignment=Qt.AlignmentFlag.AlignCenter)

        language_label = self.return_label(self.tr("Language"))
        language_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(language_label)

        self.language_selector = self.return_combo_box(
            w=200, Items_list=list(self.translations.keys()), editable=False, read_only_text=True)
        self.language_selector.setCurrentText(self.settings["language"])
        self.language_selector.currentTextChanged.connect(self.change_language)
        settings_layout.addWidget(
            self.language_selector, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addStretch(1)
        self.layout.addWidget(settings_container)
        self.layout.addStretch(1)

    def apply_settings(self):
        self.set_sound_volume(self.settings["volume"])
        self.update_ui_text()

    def update_tab_translations(self):
        if hasattr(self, 'tab') and self.tab:
            for i in range(self.tab.count()):
                tooltip_text = self.tab.tabToolTip(i)
                short_name = self.short_names.get(tooltip_text, tooltip_text)
                self.tab.setTabText(i, self.tr(short_name))

                widget = self.tab.widget(i)
                title_label = widget.findChild(QLabel, "tabTitleLabel")
                if title_label and hasattr(title_label, 'original_text'):
                    title_label.setText(self.tr(title_label.original_text))

    def update_ui_text(self):
        if hasattr(self, 'button') and not sip.isdeleted(self.button):
            self.button.setText(self.tr("Modes"))
        if hasattr(self, 'repl_button_main') and not sip.isdeleted(self.repl_button_main):
            self.repl_button_main.setText(self.tr("Python Terminal"))
        if hasattr(self, 'title_label') and self.title_label:
            if self.title_label.text().endswith("_"):
                if hasattr(self.title_label, 'original_text'):
                    self.title_label.setText(
                        self.tr(self.title_label.original_text) + "_")
            else:
                if hasattr(self.title_label, 'original_text'):
                    self.title_label.setText(
                        self.tr(self.title_label.original_text))
        for button in self.button_dyna:
            if hasattr(button, 'original_text'):
                button.setText(self.tr(button.original_text))
        self.update_tab_translations()

    def set_sound_volume(self, value):
        self.settings["volume"] = value
        volume_float = value / 100.0
        for _, audio_output in self.sound_players.values():
            audio_output.setVolume(volume_float)
        self.save_settings()

    def change_language(self, language_name):
        self.settings["language"] = language_name
        self.save_settings()
        self.update_ui_text()

    def show_submenu(self, menu_name):
        if menu_name not in self.menu_definitions:
            return
        self._delete_menu_container()
        self.layout_buttons = QVBoxLayout()
        self.layout_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.insertLayout(
            self.buttons_layout_index, self.layout_buttons)
        self.delete_button()
        self.history.append(self.show_modes_menu)
        self.delete_label()
        menu_type, data, *rest = self.menu_definitions[menu_name]
        if menu_type == "vbox":
            self.layout.insertStretch(1, 1)
            self.title_label = self.return_label(
                self.tr(menu_name.replace("_", " ")))
            self.title_label.original_text = menu_name.replace("_", " ")
            self.title_label.setStyleSheet(
                STYLES["title_label"] + "margin-bottom: 15px;")
            self.layout.insertWidget(
                2, self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
            btn_width = rest[0] if rest else 230
            self.create_btn(data, w=btn_width)
        elif menu_type == "tabs":
            placeholder = self.tr(rest[0]) if rest else self.tr("Base")
            self.layout.setContentsMargins(30, 5, 5, 0)
            self.create_tabs(data, base_placeholder=placeholder)
        elif menu_type == "custom" and callable(data):
            data()
        self.home_button.hide()
        self.button_back.show()

    def _show_tabs_view(self, tabs_info, base_placeholder="Base"):
        self._delete_menu_container()
        self.layout_buttons = QVBoxLayout()
        self.layout_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.insertLayout(
            self.buttons_layout_index, self.layout_buttons)
        self.delete_label()
        self.layout.setContentsMargins(30, 5, 5, 0)
        self.create_tabs(tabs_info, base_placeholder=self.tr(base_placeholder))
        self.history.append(self.show_modes_menu)
        self.home_button.hide()
        self.button_back.show()

    def update_color_result(self, run_button):
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

    def _show_color_converter_ui(self):
        self._delete_menu_container()
        self.clear_all_widgets()
        self.central_widget.setStyleSheet(APP_CONFIG["background_normal"])
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.delete_button()
        self.delete_label()
        container_widget = QWidget()
        view_layout = QVBoxLayout(container_widget)
        view_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        view_layout.setContentsMargins(0, 0, 0, 0)
        view_layout.setSpacing(15)
        title = self.return_label(self.tr("Color Converter"))
        title.setStyleSheet(STYLES["title_label"])
        view_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
        input_container = QWidget()
        input_container.setFixedWidth(700)
        hbox_top = QHBoxLayout(input_container)
        hbox_top.setContentsMargins(0, 0, 0, 0)
        color_button_style = f"""
            QPushButton {{ background-color: #3E3E42; border: 2px solid white; border-radius: 6px; padding: 5px; }}
            QPushButton:hover {{
                background-color: #555555;
            }}
        """

        def choose_color():
            dialog = QColorDialog(self)
            dialog.setStyleSheet("")
            dialog.setOption(
                QColorDialog.ColorDialogOption.DontUseNativeDialog, True
            )
            picker_icon_path = os.path.join(
                self.assets_dir, "icons", "color_picker.svg").replace("\\", "/")
            for widget in dialog.findChildren(QWidget):
                if isinstance(widget, QPushButton):
                    text = widget.text().lower()
                    widget.setCursor(self.Cursor)
                    if "screen" in text:
                        widget.setIcon(QIcon(picker_icon_path))
                        widget.setIconSize(QSize(24, 24))
                        widget.setStyleSheet("padding-left: 5px;")
            dialog.setStyleSheet(f"""
                QColorDialog {{
                    background-color: #1f1f1f;
                }}
                QLabel {{
                    color: white;
                    font-family: "{self.Font2.family()}";
                    font-size: 14px;
                    background: transparent;
                }}
                QPushButton {{
                    background-color: #333333;
                    border: 2px solid black;
                    border-radius: 5px;
                    padding: 8px 16px;
                    color: white;
                    font-family: "{self.Font2.family()}";
                    font-size: 13px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #dd1124;
                    color: white;
                }}
                QPushButton:pressed {{
                    background-color: #b60f20;
                }}
                QLineEdit {{
                    color: black;
                    background-color: white;
                    border: 2px solid black;
                    border-radius: 5px;
                    padding: 6px;
                    font-weight: bold;
                }}
                QLineEdit:focus, QLineEdit:hover {{
                    background-color: #dd1124;
                    color: white;
                }}
                QSpinBox {{
                    color: white;
                    background-color: #2D2D30;
                    border: 1px solid #555;
                    padding: 4px;
                    border-radius: 3px;
                }}
                QSpinBox::up-button, QSpinBox::down-button {{
                    background-color: #3E3E42;
                    border-radius: 3px;
                }}
                QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                    background-color: #dd1124;
                }}
            """)
            if dialog.exec():
                color = dialog.selectedColor()
                hex_color = color.name()
                self.line_edit_color.setText(hex_color)
                self.color_button.setProperty("color_selected", True)
                self.color_button.setIcon(QIcon())
                self.color_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {hex_color};
                        border: 2px solid white;
                        border-radius: 6px;
                        padding: 5px;
                    }}
                    QPushButton:hover {{
                        background-color: #555555;
                    }}
                """)

        def on_enter(event):
            if self.color_button.property("color_selected"):
                self.color_button.setIcon(QIcon(self.palette_svg_path))
                self.color_button.setIconSize(QSize(30, 30))

        def on_leave(event):
            if self.color_button.property("color_selected"):
                self.color_button.setIcon(QIcon())
        self.color_button = QPushButton()
        self.color_button.setFixedSize(45, 45)
        self.color_button.setCursor(self.Cursor)
        self.color_button.setStyleSheet(color_button_style)
        self.color_button.setIcon(QIcon(self.palette_svg_path))
        self.color_button.setIconSize(QSize(30, 30))
        self.color_button.setProperty("color_selected", False)
        self.color_button.clicked.connect(choose_color)
        self.color_button.enterEvent = on_enter
        self.color_button.leaveEvent = on_leave
        hbox_top.addWidget(self.color_button)
        hbox_top.addStretch(1)
        self.line_edit_color = self.return_line_edit(
            w=635, h=45,
            placeholder=self.tr(
                "Choose color or enter value (ex: #FF0000, red, rgb(255,0,0))")
        )
        hbox_top.addWidget(self.line_edit_color)
        view_layout.addWidget(input_container)
        controls_container = QWidget()
        controls_container.setFixedWidth(700)
        hbox_controls = QHBoxLayout(controls_container)
        hbox_controls.setContentsMargins(0, 0, 0, 0)
        self.Color_list = ["HEX", "RGB", "HSL", "HSV", "CMYK"]
        self.combo_box_color = self.return_combo_box(
            540, 50, Items_list=self.Color_list)
        hbox_controls.addWidget(self.combo_box_color)
        hbox_controls.addStretch(1)
        run_button = QPushButton(self.tr("Run"))
        run_button.setCursor(self.Cursor)
        run_button.setObjectName("run_button_color")
        run_button.setFont(self.Font2)
        run_button.setFixedSize(140, 50)
        run_button.setStyleSheet(STYLES["gen_btn"])
        run_button.clicked.connect(self.update_color_result)
        hbox_controls.addWidget(run_button)
        view_layout.addWidget(controls_container)
        self.result_line = self.return_black_rect(h=240)
        view_layout.addWidget(self.result_line)
        self.layout.addWidget(container_widget, 1,
                              Qt.AlignmentFlag.AlignCenter)
        self.color_widgets.append(container_widget)
        self.button_back.show()

    def _show_ascii_art_ui(self):
        self.clear_all_widgets()
        self.settings_button.hide()
        self.central_widget.setStyleSheet(APP_CONFIG["background_normal"])
        container_widget = QWidget()
        view_layout = QVBoxLayout(container_widget)
        view_layout.setContentsMargins(0, 30, 0, 0)
        view_layout.setSpacing(0)
        title = self.return_label(self.tr("ASCII Art Generator"))
        title.setStyleSheet(STYLES["title_label"])
        view_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
        view_layout.addStretch(0)
        bottom_container = QWidget()
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(1)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_edit_ascii = self.return_line_edit(
            w=700, h=45, placeholder=self.tr("Enter Text"))
        self.line_edit_ascii.returnPressed.connect(self.generate_ascii_art)
        bottom_layout.addWidget(self.line_edit_ascii)
        options_container = QWidget()
        options_container.setFixedWidth(700)
        options_layout = QHBoxLayout(options_container)
        options_layout.setSpacing(30)
        all_fonts = pyfiglet.FigletFont.getFonts()
        exotic_fonts = ['standard', 'small', 'mini', 'script', 'slant', 'italic', 'roman', 'serifcap', 'smslant', 'smscript', 'thin', '5lineoblique', 'block', 'big', 'banner', 'colossal', 'doom', 'epic', 'ogre', 'chunky', 'puffy', 'speed', 'thick', 'bigfig', 'cosmic', 'drpepper', 'eftifont', 'larry3d', 'rectangles', 'univers', 'stop', '3-d', '3d_diagonal', 'banner3-D', 'doh', 'isometric1', 'isometric2', 'isometric3', 'isometric4', 'shadow', 'dwhistled', 'rot13', 'alligator', 'alligator2', 'avatar', 'bubble', 'bulbhead', 'contessa', 'graffiti', 'hollywood', 'nancyj', 'starwars', 'sub-zero', 'swampwater',
                        'usaflag', 'weird', 'amcslash', 'caligraphy', 'catwalk', 'flowerpower', 'funky', 'ghost', 'jazmine', 'jerusalem', 'katakana', 'pawp', 'poison', 'tombstone', 'trek', 'wetletter', 'alligator3', 'danc4', 'dancingfont', 'defleppard', 'georgia11', 'graceful', 'sweet', 'digital', 'cyberlarge', 'cybermedium', 'cybersmall', 'binary', 'decimal', 'hex', 'octal', 'eftirobot', 'smkeyboard', 'morse', 'acrobatic', 'dosrebel', 'eftiwater', 'future', 'invita', 'keyboard', 'lcd', 'ntgreek', '3x5', '4max', 'bell', 'diamond', 'goofy', 'peaks', 'rounded', 'smisome1', 'stforek', 'tanja', 'twopoint', 'alphabet']
        reliable_fonts = [f for f in exotic_fonts if f in all_fonts]
        self.combo_box_ascii_font = self.return_combo_box(
            w=450, h=40, Items_list=reliable_fonts, editable=True
        )
        completer = QCompleter(reliable_fonts, self)
        self.combo_box_ascii_font.lineEdit().setPlaceholderText(self.tr("Select Font"))
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.combo_box_ascii_font.setCompleter(completer)
        options_layout.addWidget(self.combo_box_ascii_font)
        self.color_selector = self.return_combo_box(
            w=220, h=40, Items_list=['white', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'grey'],
            editable=False, read_only_text=True
        )
        options_layout.addWidget(self.color_selector)
        bottom_layout.addWidget(options_container)
        self.result_ascii = self.return_black_rect(h=340)
        bottom_layout.addWidget(self.result_ascii)
        view_layout.addWidget(bottom_container)
        view_layout.addSpacing(50)
        self.layout.addWidget(container_widget)
        self.home_button.show()

    def generate_ascii_art(self):
        text = self.line_edit_ascii.text().strip()
        if not text:
            return
        font = self.combo_box_ascii_font.currentText()
        color_name = self.color_selector.currentText()
        color_name_lower = color_name.lower()
        result = text_to_ascii_art(text, font=font)
        color_map = {
            'white': Qt.GlobalColor.white,
            'red': Qt.GlobalColor.red,
            'green': Qt.GlobalColor.green,
            'yellow': Qt.GlobalColor.yellow,
            'blue': Qt.GlobalColor.blue,
            'magenta': Qt.GlobalColor.magenta,
            'cyan': Qt.GlobalColor.cyan,
            'grey': Qt.GlobalColor.gray,
        }
        self.result_ascii.setTextColor(color_map.get(
            color_name_lower, Qt.GlobalColor.white))  
        self.result_ascii.setPlainText(result)

    def toggle_sound(self, state):
        self.settings["sound_enabled"] = bool(state)
        self.save_settings()

    def show_repl_ui(self):
        self.clear_all_widgets()
        self.settings_button.hide()
        self.central_widget.setStyleSheet("background-color: black;")
        self.home_button.raise_()
        self.layout.setContentsMargins(10, 60, 10, 10)
        self.repl_output = QTextEdit()
        self.repl_output.setReadOnly(True)
        repl_output_style = STYLES["text_edit"].replace(
            "border: 4px solid white;", "border: none;")
        self.repl_output.setStyleSheet(repl_output_style)
        repl_output_font = QFont(self.Font1)
        repl_output_font.setPointSize(self.Font1.pointSize() + 5)
        self.repl_output.setFont(repl_output_font)
        self.repl_output.append(
            self.tr("Python REPL - Press Enter to execute."))

        self.repl_input = QTextEdit()
        self.repl_input.setPlaceholderText(">>>")
        repl_input_font = QFont(self.Font1)
        repl_input_font.setPointSize(self.Font1.pointSize() + 5)
        self.repl_input.setFont(repl_input_font)
        self.repl_input.setStyleSheet(
            STYLES["line_edit_v2"] + "font-size: 17px; border-radius: 15px;")
        self.repl_input.setFixedHeight(100)

        self.repl_input.installEventFilter(self)

        self.layout.addWidget(self.repl_output)
        self.layout.addWidget(self.repl_input)
        self.home_button.show()

    def clear_all_widgets(self):
        self.delete_button()
        self.delete_tabs()
        self.delete_color_widget()
        self.delete_label()
        self._delete_menu_container()
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                layout = item.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                layout.deleteLater()


def main():
    app = QApplication(argv)
    window = Window()
    window.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
