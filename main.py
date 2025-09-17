from PySide6 import QtWidgets

from DeskConnect.connect import ConnectFunc


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication对象
    m = ConnectFunc()  # 创建一个MainWin对象
    m.show()  # 显示窗口
    sys.exit(app.exec())
