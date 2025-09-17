from PySide6 import QtWidgets


class QInformation(QtWidgets.QMessageBox):

    def __init__(self, information_str: str):
        super().__init__()

        self.setFixedSize(700, 200)
        self.setWindowTitle("信息提示")
        # 显示的内容
        self.setText(information_str)
        # 显示的图标
        self.setIcon(self.Icon.Information)
        self.setStandardButtons(self.StandardButton.Ok | self.StandardButton.Cancel)
        # 设置默认按钮，会被默认打开或突出显示
        self.setDefaultButton(self.StandardButton.Ok)

        # 将消息框弹出，返回用户的选择
        ret = self.exec()

        if ret == self.StandardButton.Ok:
            pass
        else:
            pass
