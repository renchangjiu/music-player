from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QProcess, QEvent, QSize, QPointF
from PyQt5.QtGui import QPixmap, QBrush, QFont, QColor, QIcon, QImage, QFontMetrics, QCursor, QLinearGradient, \
    QGradient, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QAbstractItemView, QListWidgetItem, QTableWidgetItem, \
    QAction, QMenu, QLabel

from PyQt5 import QtCore, QtGui, QtWidgets
import util


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(580, 633)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(580, 0))
        Form.setMaximumSize(QtCore.QSize(580, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        Form.setFont(font)
        Form.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 7, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")
        self.play_list = QtWidgets.QWidget()
        self.play_list.setObjectName("play_list")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.play_list)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(self.play_list)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.play_list)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.tabWidget.addTab(self.play_list, "")
        self.history = QtWidgets.QWidget()
        self.history.setObjectName("history")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.history)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget_2 = QtWidgets.QWidget(self.history)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.gridLayout_3.addWidget(self.widget_2, 0, 0, 1, 1)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.history)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.history, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "共45首"))
        self.pushButton.setText(_translate("Form", "收藏全部"))
        self.pushButton_2.setText(_translate("Form", "清空"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.play_list), _translate("Form", "播放列表"))
        self.label_2.setText(_translate("Form", "共100首"))
        self.pushButton_3.setText(_translate("Form", "清空"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.history), _translate("Form", "历史记录"))


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

    def paintEvent(self, QPaintEvent):
        # 画出边框线
        paint = QPainter()
        paint.begin(self)
        pen = QPen()
        pen.setColor(QColor("#c3c3c4"))
        paint.setPen(pen)
        paint.drawLine(0, 0, self.width(), 0)
        paint.drawLine(0, 0, 0, self.tabWidget.tabBar().height())
