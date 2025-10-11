from PySide6.QtWidgets import (
    QApplication, QListWidget, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, Slot


class ListWidgetWithMenu(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 初始化菜单
        self.context_menu = QMenu()
        self.delete_action = self.context_menu.addAction("Delete")
        self.clear_action = self.context_menu.addAction("Clear All")
        self.delete_action.triggered.connect(self.delete_selected)
        self.clear_action.triggered.connect(self.clear_all)

    @Slot()
    def delete_selected(self):
        if items := self.selectedItems():
            if QMessageBox.StandardButton.Yes == QMessageBox.question(
                    self, "Confirm",
                    f"Delete {len(items)} items?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ):
                for item in items:
                    self.takeItem(self.row(item))

    @Slot()
    def clear_all(self):
        if QMessageBox.StandardButton.Yes == QMessageBox.question(
                self, "Confirm",
                "Clear all items?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ):
            self.clear()

    @Slot()
    def show_context_menu(self, pos):
        self.context_menu.exec(self.mapToGlobal(pos))