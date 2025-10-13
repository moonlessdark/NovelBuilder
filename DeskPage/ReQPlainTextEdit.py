from PySide6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PySide6.QtGui import QFont, QWheelEvent
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class ZoomableTextEdit(QPlainTextEdit):
    MIN_FONT_SIZE = 8
    MAX_FONT_SIZE = 72
    ZOOM_STEP = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self._base_font = QFont("Consolas", 12)
        self.setFont(self._base_font)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            font = self.font()
            current_size = font.pointSize()

            if delta > 0:  # 放大
                new_size = min(current_size + self.ZOOM_STEP, self.MAX_FONT_SIZE)
            else:  # 缩小
                new_size = max(current_size - self.ZOOM_STEP, self.MIN_FONT_SIZE)

            if new_size != current_size:
                font.setPointSize(new_size)
                self.setFont(font)

            event.accept()
        else:
            super().wheelEvent(event)