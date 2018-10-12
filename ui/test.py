import sys, configparser
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QProcess, QEvent, QSize, QPointF
from PyQt5.QtGui import QPixmap, QBrush, QFont, QColor, QIcon, QImage, QFontMetrics, QCursor, QLinearGradient, \
    QGradient, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QAbstractItemView, QListWidgetItem, QTableWidgetItem, \
    QAction, QMenu, QLabel, QCheckBox, QFileDialog

from PyQt5 import QtCore, QtGui, QtWidgets

from search_local_music import SearchLocalMusic
from ui.choose_music_dir import Ui_Dialog


# 根据路径读取music
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
        check_box = QCheckBox(text, self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(check_box)
        return check_box

    def get_music_path(self):
        try:
            ret = []
            config_path = "./data/config.ini"
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
        config_path = "./data/config.ini"
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
            # 如果要添加的path是否不存在, 是则添加
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
        if len(change_paths) != 0:
            search_local_music = SearchLocalMusic()
            search_local_music.begin_search.connect(self.begin)
            search_local_music.end_search.connect(self.end)
            thread = threading.Thread(target=lambda: self.sub_thread(search_local_music, change_paths))
            thread.start()

    def begin(self):
        self.parent().label_search_state.setText("正在更新本地音乐列表...")

    def end(self):
        self.parent().label_search_state.setText("更新完成")
        self.local_musics_change.emit()
        print("发出信号")

    def sub_thread(self, search_local_music, change_paths):
        paths = []
        for path in change_paths:
            if path[1] == "checked":
                paths.append(path[0])
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


def main():
    app = QtWidgets.QApplication(sys.argv)
    my_window = ChooseMusicDirPage()
    my_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
