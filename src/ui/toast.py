import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFontMetrics
from PyQt5.QtWidgets import QApplication, QWidget, QDialog


class Toast(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(24, 25, 24, 25)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lb_icon = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_icon.sizePolicy().hasHeightForWidth())
        self.lb_icon.setSizePolicy(sizePolicy)
        self.lb_icon.setMinimumSize(QtCore.QSize(31, 31))
        self.lb_icon.setMaximumSize(QtCore.QSize(31, 31))
        self.lb_icon.setObjectName("lb_icon")
        self.horizontalLayout.addWidget(self.lb_icon)
        self.lb_tip = QtWidgets.QLabel(self)
        self.lb_tip.setObjectName("lb_tip")
        self.horizontalLayout.addWidget(self.lb_tip)

        self.setObjectName("window")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet(
            "QWidget#window{background-color:rgba(118,118,118,225); border-left:1px solid #b5b5b6; border-right:1px solid #b5b5b6;}" \
            "QLabel#lb_tip{color:#e5e5e6;font-size:20px;font-family:宋体}")

    @staticmethod
    def show_(parent, text, correct, time=2000):
        toast = Toast()
        toast.setParent(parent)
        text = str(text)
        toast.lb_tip.setText(text)
        toast.fm = QFontMetrics(toast.lb_tip.font())
        width = toast.fm.width(text) + 24 + 31 + 16 + 24
        height = 80
        toast.setGeometry((parent.width() - width) / 2, (parent.height() - height) / 2, width, height)

        if correct:
            toast.lb_icon.setPixmap(QPixmap("./resource/image/正确.png"))
        else:
            toast.lb_icon.setPixmap(QPixmap("./resource/image/错误.png"))

        toast.timer = QTimer()
        toast.timer.singleShot(time, Qt.PreciseTimer, toast.close)

        toast.show()


