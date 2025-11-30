from PyQt6.QtWidgets import QSlider, QKeySequenceEdit
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QStyle, QStyleOptionSlider

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

class CustomKeySequenceEdit(QKeySequenceEdit):
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.clear()
            self.clearFocus()
            event.accept()
        else:
            super().keyPressEvent(event)