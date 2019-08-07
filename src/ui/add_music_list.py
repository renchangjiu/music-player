# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\13595\PycharmProjects\hello\qt\example\music_remake\ui\add_music_list.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QIcon


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(270, 200))
        Dialog.setMaximumSize(QtCore.QSize(270, 200))
        Dialog.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.confirm = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirm.sizePolicy().hasHeightForWidth())
        self.confirm.setSizePolicy(sizePolicy)
        self.confirm.setObjectName("confirm")
        self.horizontalLayout.addWidget(self.confirm)
        self.cancel = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(228, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(228, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cancel.setText(_translate("Dialog", "取消"))
        self.confirm.setText(_translate("Dialog", "创建"))
        self.label.setText(_translate("Dialog", "新建歌单"))


class AddMusicListDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setModal(False)
        # animation = QPropertyAnimation(self)
        # animation.setDuration(100000)
        # animation.setStartValue(0)
        # animation.setEndValue(1)
        # animation.start()/

        self.setStyleSheet("QDialog{border:2px solid #c8c8c9; border-radius:5px}")
        self.label.setStyleSheet("color:333333;font-size:20px")
        self.lineEdit.setStyleSheet("border:2px solid #e1e1e2")
        self.lineEdit.setPlaceholderText("请输入歌单标题")

        self.cancel.setStyleSheet(
            "QPushButton{width:80px; height:28px;border: 1px solid #e1e1e2;background-color:#ffffff;border-radius:5px}" +
            "QPushButton:hover{background-color:#f5f5f7}")
        self.confirm.setStyleSheet(
            "QPushButton{width:80px; height:28px;color:#b5d3ea;border: 1px solid #e1e1e2;background-color:#96c0e1;border-radius:5px}")
        self.cancel.setCursor(QtCore.Qt.PointingHandCursor)
        self.confirm.setEnabled(False)
        self.lineEdit.textChanged.connect(self.make_confirm_enable)

    def make_confirm_enable(self):
        text = self.lineEdit.text()
        if len(text.strip()) != 0:
            self.confirm.setEnabled(True)
            self.confirm.setStyleSheet(
                "QPushButton{width:80px; height:28px;color:#ffffff;border: 1px solid #e1e1e2;background-color:#0c73c2;border-radius:5px}" +
                "QPushButton:hover{background-color:#1167a8}")
        else:
            self.confirm.setEnabled(False)
            self.confirm.setStyleSheet(
                "QPushButton{width:80px; height:28px;color:#b5d3ea;border: 1px solid #e1e1e2;background-color:#96c0e1;border-radius:5px}")
