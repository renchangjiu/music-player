import math

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QProcess, QEvent, QSize, QPointF
from PyQt5.QtGui import QPixmap, QBrush, QFont, QColor, QIcon, QImage, QFontMetrics, QCursor, QLinearGradient, \
    QGradient, QPainter, QPen, QPalette
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QAbstractItemView, QListWidgetItem, QTableWidgetItem, \
    QAction, QMenu, QLabel, QTableWidget, QHeaderView


# 重载QTableWidget, 实现隔行变色 & 鼠标滑过变色
class TableWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setObjectName("tablewidget")
        self.init_ui()
        # 上一行行号
        self.previous_row = -1
        # 上一行颜色, 透明颜色
        self.previous_row_color = QColor(0x00, 0xff, 0x00, 0x00)

        self.cellEntered.connect(self.cell_entered)
        # self.horizontalHeader().sectionResized.connect(self.on_resize_section)
        self.pre_size = None
        self.pre_width = -1

        self.resize_flag = True

    def on_resize_section(self, row, old_width, new_width):
        print(row, " ", old_width, " ", new_width)
        for i in range(self.columnCount()):
            pass
            # print(self.columnWidth(i))
        # if new_width < 50:
        #     self.setColumnWidth(row, 50)

    def resizeEventQQ(self, QResizeEvent_):
        if self.resize_flag:
            self.setColumnWidth(0, self.width() * 0.06)
            self.setColumnWidth(1, self.width() * 0.35)
            self.setColumnWidth(2, self.width() * 0.24)
            self.setColumnWidth(3, self.width() * 0.23)
            self.setColumnWidth(4, self.width() * 0.12)
        self.resize_flag = False

        column_width_sum = 0
        for i in range(self.columnCount()):
            column_width_sum += self.columnWidth(i)
        # print(column_width_sum, "  ", self.width())
        # if self.pre_size is not None:
        #     for i in range(self.columnCount()):
        #         print(self.columnWidth(i))
        #         # print("pre: ", self.pre_size.width())
        #         # print("cur: ", self.width())
        #         if self.width() - column_width_sum >= 5:
        #             self.setColumnWidth(i, round(self.columnWidth(i) / column_width_sum * self.width()))
        # else:
        #     self.pre_size = QSize(self.width(), self.height())
        # print("*" * 10)
        # # print("之前宽度总和: ", sum, "old-width: ", self.width())
        self.pre_size = QSize(self.width(), self.height())
        if self.width() - self.pre_width >= 20:
            pass
        else:
            pass

        super().resizeEvent(QResizeEvent_)

    def leaveEvent(self, QEvent_):
        # 还原上一行颜色
        item = self.item(self.previous_row, 0)
        if item is not None:
            self.set_row_color(self.previous_row, self.previous_row_color)
        super().leaveEvent(QEvent_)

    def cell_entered(self, row, column):
        # 还原上一行颜色
        item = self.item(self.previous_row, 0)
        if item is not None:
            self.set_row_color(self.previous_row, self.previous_row_color)

        # 设置当前行颜色
        item = self.item(row, column)
        if item is not None:
            self.set_row_color(row, QColor("#ebeced"))  # TODO 颜色先写死
        self.previous_row = row

    # 可能会有bug
    def set_row_color(self, row, color):
        brush = QBrush(color)
        for column in range(self.columnCount()):
            item = self.item(row, column)
            if item is not None:
                item.setBackground(brush)
            # else:
            #     item_widget = self.cellWidget(row, column)
            #     if item_widget is not None:
            #         item_widget.setStyleSheet(
            #             "background-color:rgba(%d,%d,%d,%d);" % (color.red(), color.green(), color.blue(), color.alpha()))

    def init_ui(self):
        # self.horizontalHeader().setStretchLastSection(True)
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 隐藏默认行号
        self.verticalHeader().setHidden(True)
        # 按住Ctrl or shift选择
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 解决表头塌陷
        self.horizontalHeader().setHighlightSections(False)
        # 设置整行选中
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setShowGrid(False)  # 设置不显示格子线
        self.setFocusPolicy(Qt.NoFocus)  # 去除选中虚线框
        self.setMouseTracking(True)

        # 设置垂直滚动条样式
        self.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa; width: 8px;}"
                                               "QScrollBar::handle{background:#e1e1e2; border-radius:4px;}"
                                               "QScrollBar::handle:hover{background:#cfcfd1;}"
                                               "QScrollBar::sub-line{none;}"
                                               "QScrollBar::add-line{background:transparent;}")

        # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 更改右键策略
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # 隔行变色
        p = self.palette()
        p.setColor(QPalette.Base, QColor("#fafafa"))
        p.setColor(QPalette.AlternateBase, QColor("#f5f5f7"))
        self.setPalette(p)
        self.setAlternatingRowColors(True)
