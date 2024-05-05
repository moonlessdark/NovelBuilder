import sys

from PySide6 import QtWidgets

from DeskFunc.connect import MainFunc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication对象
    m = MainFunc()  # 创建一个MainWin对象
    m.show()  # 显示窗口
    sys.exit(app.exec())  # 执行QApplication的exec_()方法，开始事件循环
