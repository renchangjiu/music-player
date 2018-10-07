import re, os, sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QProcess, QEvent, QSize, QPointF
from PyQt5.QtGui import QPixmap, QBrush, QFont, QColor, QIcon, QImage, QFontMetrics, QCursor, QLinearGradient, \
    QGradient, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QAbstractItemView, QListWidgetItem, QTableWidgetItem, \
    QAction, QMenu, QLabel

from main_widget import Ui_Form
from ui.play_list_page import Ui_Form
import util


class PlayListPage(QWidget, Ui_Form):
    def __init__(self, parent):
        QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.setParent(parent)

        self.__init_ui()
        self.__init_table_widget_ui()
        self.__set_table_widget_width()

    def __init_ui(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.tabWidget.setCurrentWidget(self.play_list)
        # self.setStyleSheet('border:1px solid red')

        self.tabWidget.tabBar().setCursor(Qt.PointingHandCursor)
        self.tabWidget.setStyleSheet("QTabWidget{border:10px solid red;}")
        self.tabWidget.setStyleSheet("QTabWidget::pane{border-top: 1px solid #e1e1e2;}" +
                                     "QTabWidget::tab-bar{alignment:center;height:46px;}" +
                                     "QTabBar::tab:!selected{height:38px;background-color:#7c7d86; color: #ffffff;}" +
                                     "QTabBar::tab:selected:hover{height:38px;background:#f5f5f7;}"
                                     )

        self.widget.setStyleSheet(
            "background:#f9f9f9;border:none;border-bottom:1px solid #efefef;border-left:1px solid #c3c3c4;")
        self.label.setStyleSheet("border:none")
        self.label_2.setStyleSheet("border:none")
        self.widget_2.setStyleSheet(
            "background:#f9f9f9;border:none;border-bottom:1px solid #efefef;border-left:1px solid #c3c3c4;")

        # self.setGeometry(self.parent().width() - 580, 150, 580,
        #                  self.parent().height() - 150 - 48)

    def __init_table_widget_ui(self):
        self.tableWidget.setColumnCount(5)
        # 隐藏默认行号
        self.tableWidget.verticalHeader().setHidden(True)
        self.tableWidget.horizontalHeader().setHidden(True)
        # 按住Ctrl or shift选择
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # 解决表头塌陷
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        # 设置整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(False)  # 设置不显示格子线
        self.tableWidget.setFocusPolicy(Qt.NoFocus)  # 去除选中虚线框
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置垂直滚动条样式
        self.tableWidget.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa; width: 10px;}"
                                                           "QScrollBar::handle{background:#e1e1e2; border:2px solid transparent; border-radius:5px;}"
                                                           "QScrollBar::handle:hover{background:#cfcfd1;}"
                                                           "QScrollBar::sub-line{background:transparent;}"
                                                           "QScrollBar::add-line{background:transparent;}")
        self.tableWidget.setStyleSheet("QTableWidget{border:none;border-left:1px solid #c0c0c1}" +
                                       "QTableWidget::item::selected{background:#e3e3e5}")
        # 隐藏横向滚动条
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 更改右键策略
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)

    def __set_table_widget_width(self):
        self.tableWidget.setColumnWidth(0, self.width() * 0.03)
        self.tableWidget.setColumnWidth(1, self.width() * 0.63)
        self.tableWidget.setColumnWidth(2, self.width() * 0.17)
        self.tableWidget.setColumnWidth(3, self.width() * 0.05)
        self.tableWidget.setColumnWidth(4, self.width() * 0.12)

    def show_data(self, play_list):
        self.setGeometry(self.parent().width() - 580, 150, 580,
                         self.parent().height() - 150 - 48)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(play_list.size())
        self.label.setText("共%d首" % play_list.size())
        icon = QIcon("./resource/image/链接.png")
        for i in range(play_list.size()):
            music = play_list.get(i)
            icon_item = QTableWidgetItem()
            icon_item.setIcon(icon)
            self.tableWidget.setItem(i, 0, QTableWidgetItem("\t"))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(music.get_title())))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(music.get_artist())))
            self.tableWidget.setItem(i, 3, icon_item)
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(util.format_time(music.get_duration()))))

        # 为当前音乐设置喇叭图标
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("./resource/image/musics_play.png"))
        icon_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableWidget.setCellWidget(play_list.get_current_index(), 0, icon_label)

        # 隔行变色
        b1 = QBrush(QColor("#fafafa"))
        b2 = QBrush(QColor("#f5f5f7"))
        for i in range(self.tableWidget.rowCount()):
            if i % 2 == 0:
                for j in range(self.tableWidget.columnCount()):
                    if self.tableWidget.item(i, j) is not None:
                        self.tableWidget.item(i, j).setBackground(b1)
            else:
                for j in range(self.tableWidget.columnCount()):
                    if self.tableWidget.item(i, j) is not None:
                        self.tableWidget.item(i, j).setBackground(b2)

        print(self.tabWidget.tabBar().height())

    def paintEvent(self, QPaintEvent):
        # 画出边框线
        paint = QPainter()
        paint.begin(self)
        pen = QPen()
        pen.setColor(QColor("#c3c3c4"))
        paint.setPen(pen)
        paint.drawLine(0, 0, self.width(), 0)
        paint.drawLine(0, 0, 0, self.tabWidget.tabBar().height())


"""QString tabWidgetStyle1 =  "QTabWidget::pane {border-top: 2px solid #c2c7cb;}\
        QTabWidget::tab-bar {left:5px}\
        QTabBar::tab {background: blue;border:2px solid #c4c4c3;border-bottom-color:#c2c7cb;border-top-left-radius:4px;border-top-right-radius:4px;min-width:8px;padding:2px;}\
        QTabBar::tab:!selected{margin-top:20px}";/*选中的标签高20px ,commented by zhaoyulong,2016.9.10*/
 
QString tabWidgetStyle2 = "QTabWidget::pane{border-top:1px solid gray;border-bottom:2px solid black;}\
        QTabWidget::tab-bar {left:5px}\
        QTabBar::tab:!selected{width:40px;height:20px;background:rgb(240,240,240);font:20px}\
        QTabBar::tab:selected{width:40px;height:20px;background:rgb(240,240,240);color:blue;font:20px;border-bottom:2px solid blue }\
"""
