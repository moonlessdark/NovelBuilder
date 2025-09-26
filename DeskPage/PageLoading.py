import os.path

from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtCore import QPropertyAnimation, Property, QTimer, QEasingCurve, Qt
from PySide6.QtGui import QColor, QPainter


class TransparentLoadingView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.anim = None
        self.svg_item = None
        self._angle = None
        self.setWindowTitle("Transparent Loading")

        # self.resize(780, 590)

        # 设置透明窗口属性
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # 创建透明场景
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor(0, 0, 0, 0))
        self.setScene(self.scene)

        # 延迟加载确保渲染完成
        QTimer.singleShot(100, self.init_animation)
        # self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform)
        # 如果FullViewportUpdate性能不够理想，可以尝试以下替代方案
        # self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        # 或者
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)

    def init_animation(self):
        # 加载SVG并设置居中

        _loading_file_path = "./_internal/Resources/Images/loading.svg"
        if not os.path.exists(_loading_file_path):
            _loading_file_path = "./Resources/Images/loading.svg"
        self.svg_item = QGraphicsSvgItem(_loading_file_path)
        rect = self.svg_item.boundingRect()
        self.svg_item.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.scene.addItem(self.svg_item)
        self.centerOn(self.svg_item)

        # 动画配置
        self._angle = 0
        self.anim = QPropertyAnimation(self, b"angle")
        self.anim.setDuration(2000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(360)
        self.anim.setKeyValueAt(0.3, 120)  # 前120°快转
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.setLoopCount(-1)
        QTimer.singleShot(50, self.anim.start)

    @Property(float)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.svg_item.setRotation(value)
        # 强制刷新视口以避免残影
        self.viewport().update()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")  # 确保透明效果生效
    window = TransparentLoadingView()
    window.show()
    app.exec()
