import sys
from PySide6.QtWidgets import QApplication, QTableView, QStyledItemDelegate, QStyleOptionViewItem, QAbstractItemView, \
    QStyledItemDelegate, QStyleOptionViewItem, QWidget, QVBoxLayout, QTableView, QHeaderView
from PySide6.QtCore import Qt, QRect, QSize, QModelIndex, QAbstractTableModel, QSortFilterProxyModel


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data  # 数据存储，例如 [[row1col1, row1col2], [row2col1, row2col2], ...]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        if not self._data:
            return 0
        return max(len(row) for row in self._data)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            if col < len(self._data[row]):
                return self._data[row][col]
        return None


# 使用 QSortFilterProxyModel 来虚拟化数据
class VirtualTableModel(QSortFilterProxyModel):
    def __init__(self, sourceModel):
        super().__init__()
        self.setSourceModel(sourceModel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = [["Row 1", "Row 1 Col 2", "Row 1 Col 3"], ["Row 2", "Row 2 Col 2", "Row 2 Col 3", "Row 2 Col 4"], ["Row 3", "Row 3 Col 2"]]
    model = CustomTableModel(data)
    view = QTableView()
    view.show()
    view.setModel(model)

    # 可选：设置固定行高

    sys.exit(app.exec())