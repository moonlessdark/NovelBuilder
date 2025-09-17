import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QMovie, Qt


class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Loading')
        # self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # 创建QLabel用于显示GIF
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 加载GIF文件并设置到QLabel
        movie = QMovie(r"/Users/luojun/ProjectDev/NovelBuilder/Resources/loading.gif")
        self.label.setMovie(movie)
        movie.start()

        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoadingWindow()
    ex.show()
    sys.exit(app.exec())