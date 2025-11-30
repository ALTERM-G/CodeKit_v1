import sys
import os
from PyQt6.QtWidgets import QApplication
from app.ui.main_window import Window
from app import load_translations

def get_base_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
    base_path = get_base_path()
    window = Window(base_path=base_path)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()