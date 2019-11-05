# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\13595\PycharmProjects\music-player\ui\choose_music_dir.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import os
import configparser
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QFileDialog

from src.service.search_local_music import SearchLocalMusic
from src.common.app_attribute import AppAttribute
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(302, 357)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(302, 357))
        Dialog.setMaximumSize(QtCore.QSize(302, 357))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.header = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setMinimumSize(QtCore.QSize(302, 51))
        self.header.setMaximumSize(QtCore.QSize(302, 51))
        self.header.setObjectName("header")
        self.gridLayout = QtWidgets.QGridLayout(self.header)
        self.gridLayout.setContentsMargins(20, -1, 13, -1)
        self.gridLayout.setHorizontalSpacing(13)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.header)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.btn_close = QtWidgets.QPushButton(self.header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMinimumSize(QtCore.QSize(14, 13))
        self.btn_close.setMaximumSize(QtCore.QSize(14, 13))
        self.btn_close.setText("")
        self.btn_close.setObjectName("btn_close")
        self.gridLayout.addWidget(self.btn_close, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.header, 0, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 280, 181))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(20, -1, 20, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.footer = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy)
        self.footer.setMinimumSize(QtCore.QSize(0, 62))
        self.footer.setMaximumSize(QtCore.QSize(199999, 62))
        self.footer.setObjectName("footer")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout.setContentsMargins(63, -1, 63, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_confirm = QtWidgets.QPushButton(self.footer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_confirm.sizePolicy().hasHeightForWidth())
        self.btn_confirm.setSizePolicy(sizePolicy)
        self.btn_confirm.setMinimumSize(QtCore.QSize(80, 30))
        self.btn_confirm.setMaximumSize(QtCore.QSize(80, 30))
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout.addWidget(self.btn_confirm)
        self.btn_add = QtWidgets.QPushButton(self.footer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setMinimumSize(QtCore.QSize(80, 30))
        self.btn_add.setMaximumSize(QtCore.QSize(80, 30))
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.gridLayout_2.addWidget(self.footer, 3, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 61))
        self.label_2.setMaximumSize(QtCore.QSize(19991, 61))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "选择本地音乐文件夹"))
        self.btn_confirm.setText(_translate("Dialog", "确认"))
        self.btn_add.setText(_translate("Dialog", "添加文件夹"))
        self.label_2.setText(_translate("Dialog", " 将自动扫描您勾选的目录, 文件增删实时同步"))


class ChooseMusicDirPage(QtWidgets.QDialog, Ui_Dialog):
    local_musics_change = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setParent(parent)
        self.setupUi(self)
        # 记录下修改path之前的path, 以便在修改之后判断是否需要重新搜索音乐
        self.pre_paths = []
        self.init_ui()
        self.init_data()
        self.init_connect()

    def init_connect(self):
        self.btn_close.clicked.connect(self.close)
        self.btn_add.clicked.connect(self.show_dialog)
        self.btn_confirm.clicked.connect(self.on_confirm)

    def add_checkbox(self, text):
        # 特殊字符, 把一个 &, 替换成两个 &&, 以正常显示一个&
        # error, 上述方法会导致bug
        # check_box = QCheckBox(text.replace("&", "&&"), self.scrollAreaWidgetContents)
        check_box = QCheckBox(text, self.scrollAreaWidgetContents)
        check_box.setToolTip(text)
        self.verticalLayout.addWidget(check_box, alignment=Qt.AlignTop)
        return check_box

    @staticmethod
    def get_music_path():
        try:
            ret = []
            config_path = AppAttribute.data_path + "/config.ini"
            config = configparser.ConfigParser()
            config.read(config_path, "utf-8")
            # d:/path1/*checked?d:/path2/path2/*checked?d:/path3/path3/path3/unchecked?
            path_str = config.get("music-path", "path")
            paths = path_str.split("?")
            for path in paths:
                split = path.split("*")
                if len(split) == 2:
                    temp = (split[0], split[1])
                    ret.append(temp)
            return ret
        except configparser.NoSectionError as e1:
            pass
        except configparser.NoOptionError as e2:
            pass

    def write_music_path(self, paths):
        path_str = ""
        for path in paths:
            path_str = path_str + path[0] + "*" + path[1] + "?"
        config_path = AppAttribute.data_path + "/config.ini"
        config = configparser.ConfigParser()
        config.read(config_path, "utf-8")
        config.set("music-path", "path", path_str)
        config.write(open(config_path, "w"))

    def init_data(self):
        paths = self.get_music_path()
        for path in paths:
            checkbox = self.add_checkbox(path[0])
            self.pre_paths.append(path)
            if path[1] == "checked":
                checkbox.setCheckState(Qt.Checked)

    def show_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "选择添加目录", r"C:/", QFileDialog.ShowDirsOnly)
        if path.strip() != "":
            # 要添加的path是否不存在, 是则添加
            if self.in_paths(path) == "":
                checkbox = self.add_checkbox(path)
                checkbox.setCheckState(Qt.Checked)

    # 判断要添加的path是否已经存在, 已存在则返回其check状态("checked" or "unchecked"), 否则返回""
    def in_paths(self, path):
        for p in self.pre_paths:
            if path == p[0]:
                return p[1]
        return ""

    def on_confirm(self):
        ret = []
        count = self.verticalLayout.layout().count()
        for i in range(count):
            at = self.verticalLayout.layout().itemAt(i)
            if at != 0:
                checkbox = at.widget()
                temp = [checkbox.text()]
                if checkbox.checkState() == Qt.Checked:
                    temp.append("checked")
                elif checkbox.checkState() == Qt.Unchecked:
                    temp.append("unchecked")
                ret.append(temp)
        self.write_music_path(ret)
        self.compare_two_path(ret)
        # 重新为previous path 赋值
        self.pre_paths.clear()
        for path in ret:
            self.pre_paths.append(path)
        self.close()

    # 比较path修改前后的变化(多一个 or 少一个)
    def compare_two_path(self, cur_paths):
        change_paths = []
        # 因为已添加的目录不可被删除, 所以previous-paths总是current-paths的子集
        for path in cur_paths:
            pre_state = self.in_paths(path[0])
            # 如果该path 已存在,
            if pre_state != "":
                # 如果state不同, 则返回当前state
                if path[1] != pre_state:
                    change_paths.append(path)
            # 不存在, 根据其是否被check, 判断
            else:
                if path[1] == "checked":
                    change_paths.append(path)
        # 如果path有变化, 则重新搜索新的path
        if len(change_paths) != 0:
            # print(cur_paths)
            search_local_music = SearchLocalMusic()
            search_local_music.begin_search.connect(self.begin)
            search_local_music.end_search.connect(self.end)
            thread = threading.Thread(target=lambda: self.sub_thread(search_local_music, cur_paths))
            thread.start()

    # 比较path修改前后的变化(多一个 or 少一个)
    def compare_two_path_可被优化的(self, cur_paths):
        change_paths = []
        # 因为已添加的目录不可被删除, 所以previous-paths总是current-paths的子集
        for path in cur_paths:
            pre_state = self.in_paths(path[0])
            # 如果该path 已存在,
            if pre_state != "":
                # 如果state不同, 则返回当前state
                if path[1] != pre_state:
                    change_paths.append(path)
            # 不存在, 根据其是否被check, 判断
            else:
                if path[1] == "checked":
                    change_paths.append(path)
        print(change_paths)
        if len(change_paths) != 0:
            search_local_music = SearchLocalMusic()
            search_local_music.begin_search.connect(self.begin)
            search_local_music.end_search.connect(self.end)
            thread = threading.Thread(target=lambda: self.sub_thread(search_local_music, change_paths))
            thread.start()

    def begin(self):
        self.parent().begin_search()
        self.parent().label_search_state.setText("正在更新本地音乐列表...")

    def end(self):
        self.parent().end_search()
        self.parent().label_search_state.setText("更新完成")
        # 发出信号, 通知父窗口更新本地音乐
        self.local_musics_change.emit()

    def sub_thread(self, search_local_music, change_paths):
        paths = []
        for path in change_paths:
            if path[1] == "checked" and os.path.exists(path[0]):
                paths.append(path[0])
        print(paths)
        search_local_music.search_in_path(paths)

    def init_ui(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setModal(True)
        self.setWindowModality(Qt.WindowModal)
        self.setGeometry((self.parent().width() - self.width()) / 2, (self.parent().height() - self.height()) / 2, 0, 0)
        # scrollArea -> scrollAreaWidgetContents -> verticalLayout
        self.setStyleSheet("background:#fafafa;border-right:1px solid #c8c8c8;")
        self.header.setStyleSheet(
            "QWidget#header{border:1px solid #c8c8c8;border-bottom:1px solid #e1e1e2;background:#fafafa;}")
        self.label_2.setStyleSheet("border-left:1px solid #c8c8c8;border-right:1px solid #c8c8c8;")
        self.scrollArea.setStyleSheet(
            "QScrollArea#scrollArea{border:none;border-left:1px solid #c8c8c8;}")
        self.scrollAreaWidgetContents.setStyleSheet("{font-size:16px;}")
        self.label.setStyleSheet("border:none")
        self.scrollAreaWidgetContents.setStyleSheet(
            "QWidget{border:none;}"
            "QCheckBox::indicator::unchecked{image:url(./resource/image/checkbox-unchecked.png);}" +
            "QCheckBox::indicator::checked{image:url(./resource/image/checkbox-checked.png);}")

        self.scrollArea.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa; width:8px;border:none;}"
                                                          "QScrollBar::handle{border:none;background:#e1e1e2; border-radius:4px;}"
                                                          "QScrollBar::handle:hover{background:#cfcfd1;}"
                                                          "QScrollBar::sub-line{none;}"
                                                          "QScrollBar::add-line{background:transparent;}")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.footer.setStyleSheet(
            "QWidget#footer{border:1px solid #c8c8c8;border-top:1px solid #e1e1e2;background:#f5f5f7;}")

        self.btn_close.setStyleSheet("QPushButton{border-image:url(./resource/image/choose-music-dir-page-关闭.png)}")
        self.btn_confirm.setStyleSheet(
            "QPushButton{width:80px; height:28px;color:#ffffff;border: 1px solid #e1e1e2;background-color:#0c73c2;border-radius:5px}" +
            "QPushButton:hover{background-color:#1167a8}")
        self.btn_add.setStyleSheet(
            "QPushButton{width:80px; height:28px;border: 1px solid #e1e1e2;background-color:#ffffff;border-radius:5px}" +
            "QPushButton:hover{background-color:#f5f5f7}")
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_confirm.setCursor(Qt.PointingHandCursor)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.header.setCursor(Qt.SizeAllCursor)
