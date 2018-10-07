import re, os, sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QProcess, QEvent, QSize, QPointF
from PyQt5.QtGui import QPixmap, QBrush, QFont, QColor, QIcon, QImage, QFontMetrics, QCursor, QLinearGradient, \
    QGradient, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QAbstractItemView, QListWidgetItem, QTableWidgetItem, \
    QAction, QMenu, QLabel

from LRCParser import LRC
from MP3Parser import MP3
from main_widget import Ui_Form
from music_list import MusicList
from ui import add_music_list
import util
import ui.test
from search_local_music import SearchLocalMusic
from menu import Menu

# TODO 本地音乐(未完成:)
# TODO 自动滚动到当前播放音乐所在行: verticalScrollBar.setValue()
# TODO 歌单音乐列表的右键菜单 (未完成: UI)
# TODO ACTION 移入移出(1.重载类, 2. 判断鼠标位置)
# TODO UI细节调整
# todo 本地音乐或可与歌单音乐代码合并
# todo 歌单图片 & 显示播放数
# TODO 优化代码
from ui.toast import Toast


class MyWindow(QWidget, Ui_Form):
    # 播放状态
    stopped_state = 0
    playing_state = 1
    paused_state = 2

    def __init__(self):
        QWidget.__init__(self)
        Ui_Form.__init__(self)

        # 播放信息
        self.process = None
        # 音量
        self.volume = 50
        # 音乐时长
        self.duration = -1
        # 播放状态
        self.state = self.stopped_state
        # 播放位置
        self.percent_pos = -0.1
        self.is_mute = False

        # 全屏播放界面的歌词label是否正在被滚动
        self.is_wheeling = False
        self.timer = QTimer(self)
        # 启动定时器, 每隔0.1s 使mplayer输出时间信息(duration & position)
        self.timer.start(100)

        # 当前歌单的音乐列表, 初始化时加载歌单中所有音乐, 搜索时会清空音乐并加载搜索结果
        self.cur_music_list = None
        # 包含当前歌单的全部音乐, 只用于搜索使用的库
        self.cur_whole_music_list = None
        # 当前播放列表
        self.cur_play_list = None

        # 本地音乐(也是歌单)
        self.cur_local_music_list = None
        self.cur_whole_local_music_list = None

        self.setupUi(self)
        self.init_data()
        self.init_table_widget_ui()
        self.init_ui()
        self.init_button()
        self.init_shortcut()
        self.init_connect()

    def init_data(self):
        font = QFont()
        font.setPixelSize(13)
        local_item = QListWidgetItem(self.navigation)
        local_item.setIcon(QIcon("./resource/image/本地音乐.png"))
        local_item.setText("本地音乐")
        local_item.setFont(font)
        self.navigation.addItem(local_item)

        item1 = QListWidgetItem()
        item1.setText("创建的歌单")
        item1.setFlags(Qt.NoItemFlags)
        self.navigation.addItem(item1)

        path = "./resource/config/"
        music_lists = os.listdir(path)
        music_list_icon = QIcon("./resource/image/歌单.png")
        for music_list in music_lists:
            item = QListWidgetItem()
            item.setIcon(music_list_icon)
            item.setFont(font)
            item.setText(music_list)
            self.navigation.addItem(item)

        # 启动时默认选中第一个歌单
        self.navigation.setCurrentRow(2)
        text = self.navigation.currentItem().text()
        self.cur_music_list = MusicList.from_disk(path + text)
        self.cur_whole_music_list = MusicList.from_disk(path + text)
        self.stackedWidget_2.setCurrentWidget(self.music_list_detail)
        self.musics.setColumnCount(5)
        # 将歌单中的歌曲列表加载到 table widget
        self.show_musics_data()
        self.cur_play_list = MusicList.to_play_list(self.cur_music_list)
        self.cur_play_list.set_current_index(0)
        self.cur_play_list.current_music_change.connect(self.on_cur_play_list_change)

    def init_table_widget_ui(self):
        # --------------------- 1. 歌单音乐列表UI --------------------- #
        # 隐藏默认行号
        self.musics.verticalHeader().setHidden(True)
        # 按住Ctrl or shift选择
        self.musics.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.musics.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.musics.setHorizontalHeaderLabels(["", "音乐标题", "歌手", "专辑", "时长"])
        self.musics.setColumnCount(5)
        self.musics.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # 解决表头塌陷
        self.musics.horizontalHeader().setHighlightSections(False)
        # 设置整行选中
        self.musics.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.musics.setShowGrid(False)  # 设置不显示格子线
        self.musics.setFocusPolicy(Qt.NoFocus)  # 去除选中虚线框
        self.musics.setMouseTracking(True)
        # 设置垂直滚动条样式
        self.musics.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa; width: 10px;}"
                                                      "QScrollBar::handle{background:#e1e1e2; border:2px solid transparent; border-radius:5px;}"
                                                      "QScrollBar::handle:hover{background:#cfcfd1;}"
                                                      "QScrollBar::sub-line{background:transparent;}"
                                                      "QScrollBar::add-line{background:transparent;}")
        self.musics.setStyleSheet("QTableWidget{border:none}" +
                                  "QTableWidget::item::selected{background:#e3e3e5}")
        # 设置表头
        self.musics.horizontalHeader().setStyleSheet(
            """QHeaderView::section{background:#fafafa;border:none;border-right:1px solid #e1e1e2}
            QHeaderView::section:hover{background:#ebeced;border:none}
            QHeaderView{color:#666666; border-top:1px solid #c62f2f;}
            """)

        # 隐藏横向滚动条
        self.musics.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 更改右键策略
        self.musics.setContextMenuPolicy(Qt.CustomContextMenu)

        # --------------------- 2. 本地音乐页面UI--------------------- #
        self.tb_local_music.verticalHeader().setHidden(True)
        self.tb_local_music.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tb_local_music.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tb_local_music.setColumnCount(6)
        self.tb_local_music.setHorizontalHeaderLabels(["", "音乐标题", "歌手", "专辑", "时长", "大小"])
        self.tb_local_music.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tb_local_music.horizontalHeader().setHighlightSections(False)
        self.tb_local_music.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_local_music.setShowGrid(False)  # 设置不显示格子线
        self.tb_local_music.setFocusPolicy(Qt.NoFocus)  # 去除选中虚线框
        self.tb_local_music.setMouseTracking(True)
        self.tb_local_music.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa; width: 10px;}"
                                                              "QScrollBar::handle{background:#e1e1e2; border:2px solid transparent; border-radius:5px;}"
                                                              "QScrollBar::handle:hover{background:#cfcfd1;}"
                                                              "QScrollBar::sub-line{background:transparent;}"
                                                              "QScrollBar::add-line{background:transparent;}")
        self.tb_local_music.setStyleSheet("QTableWidget{border:none}" +
                                          "QTableWidget::item::selected{background:#e3e3e5}")
        # 设置表头
        self.tb_local_music.horizontalHeader().setStyleSheet(
            """QHeaderView::section{background:#fafafa;border:none;border-right:1px solid #e1e1e2}
            QHeaderView::section:hover{background:#ebeced;border:none}
            QHeaderView{color:#666666; border-top:1px solid #c62f2f;}
            """)
        self.tb_local_music.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tb_local_music.setContextMenuPolicy(Qt.CustomContextMenu)

    # 当点击navigation时, 显示对应页面
    def on_nav_clicked(self, QListWidgetItem_):
        text = QListWidgetItem_.text()
        if text == "本地音乐":
            self.show_local_music_page()
            return
        if text == "创建的歌单":
            return
        self.stackedWidget_2.setCurrentWidget(self.music_list_detail)
        path = "./resource/config/"
        music_list_path = path + text
        self.cur_music_list = MusicList.from_disk(music_list_path)
        self.cur_whole_music_list = MusicList.from_disk(music_list_path)
        # 在 tableWidget中显示歌曲列表
        self.set_musics_layout()
        # 加载歌单中的歌曲列表
        self.show_musics_data()
        self.show_icon_item()
        self.musics.setCurrentCell(0, 0)

    # 将歌单中的歌曲列表加载到 table widget
    # 需先设置列数
    def show_musics_data(self):
        self.music_list_name.setText(self.cur_music_list.get_name())
        self.music_list_date.setText("%s创建" % self.cur_music_list.get_date())
        self.music_count.setText("<p>歌曲数</p><p style='text-align: right'>%d</p>" % self.cur_music_list.size())
        self.music_list_play_count.setText(
            "<p>播放数</p><p style='text-align: right'>%d</p>" % self.cur_music_list.get_play_count())

        self.musics.clearContents()
        self.musics.setRowCount(self.cur_music_list.size())
        musics__ = self.cur_music_list
        for i in range(musics__.size()):
            music = musics__.get(i)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setText(str(i + 1) + " ")
            self.musics.setItem(i, 0, item)
            self.musics.setItem(i, 1, QTableWidgetItem(str(music.get_title())))
            self.musics.setItem(i, 2, QTableWidgetItem(str(music.get_artist())))
            self.musics.setItem(i, 3, QTableWidgetItem(str(music.get_album())))
            self.musics.setItem(i, 4, QTableWidgetItem(str(util.format_time(music.get_duration()))))
        self.interlaced_discoloration()

    # 隔行变色(注: 需要先把数据填充到表格)
    def interlaced_discoloration(self):
        b1 = QBrush(QColor("#fafafa"))
        b2 = QBrush(QColor("#f5f5f7"))
        # 对歌单音乐列表
        if self.stackedWidget_2.currentWidget() == self.music_list_detail:
            for i in range(self.musics.rowCount()):
                if i % 2 == 0:
                    for j in range(self.musics.columnCount()):
                        if self.musics.item(i, j) is not None:
                            self.musics.item(i, j).setBackground(b1)
                else:
                    for j in range(self.musics.columnCount()):
                        if self.musics.item(i, j) is not None:
                            self.musics.item(i, j).setBackground(b2)
        elif self.stackedWidget_2.currentWidget() == self.local_music_page:
            for i in range(self.tb_local_music.rowCount()):
                if i % 2 == 0:
                    for j in range(self.tb_local_music.columnCount()):
                        if self.tb_local_music.item(i, j) is not None:
                            self.tb_local_music.item(i, j).setBackground(b1)
                else:
                    for j in range(self.tb_local_music.columnCount()):
                        if self.tb_local_music.item(i, j) is not None:
                            self.tb_local_music.item(i, j).setBackground(b2)

    def show_local_music_page(self):
        self.stackedWidget_2.setCurrentWidget(self.local_music_page)
        self.cur_local_music_list = SearchLocalMusic.get_exist_result()
        self.cur_whole_local_music_list = SearchLocalMusic.get_exist_result()
        self.show_local_music_page_data()
        # 隔行变色
        self.interlaced_discoloration()

    def show_local_music_page_data(self):
        self.label_2.setText("%d首音乐" % self.cur_whole_local_music_list.size())
        self.tb_local_music.clearContents()
        self.tb_local_music.setRowCount(self.cur_local_music_list.size())
        self.set_tb_local_music_layout()
        for i in range(self.cur_local_music_list.size()):
            music = self.cur_local_music_list.get(i)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setText(str(i + 1) + " ")
            self.tb_local_music.setItem(i, 0, item)
            self.tb_local_music.setItem(i, 1, QTableWidgetItem(str(music.get_title())))
            self.tb_local_music.setItem(i, 2, QTableWidgetItem(str(music.get_artist())))
            self.tb_local_music.setItem(i, 3, QTableWidgetItem(str(music.get_album())))
            self.tb_local_music.setItem(i, 4, QTableWidgetItem(str(util.format_time(music.get_duration()))))
            self.tb_local_music.setItem(i, 5, QTableWidgetItem(str(music.get_size())))

    def set_musics_layout(self):
        self.musics.setColumnWidth(0, self.musics.width() * 0.06)
        self.musics.setColumnWidth(1, self.musics.width() * 0.35)
        self.musics.setColumnWidth(2, self.musics.width() * 0.24)
        self.musics.setColumnWidth(3, self.musics.width() * 0.23)
        self.musics.setColumnWidth(4, self.musics.width() * 0.12)

    def set_tb_local_music_layout(self):
        self.tb_local_music.setColumnWidth(0, self.tb_local_music.width() * 0.05)
        self.tb_local_music.setColumnWidth(1, self.tb_local_music.width() * 0.37)
        self.tb_local_music.setColumnWidth(2, self.tb_local_music.width() * 0.22)
        self.tb_local_music.setColumnWidth(3, self.tb_local_music.width() * 0.22)
        self.tb_local_music.setColumnWidth(4, self.tb_local_music.width() * 0.07)
        self.tb_local_music.setColumnWidth(5, self.tb_local_music.width() * 0.07)

    # musics_play
    def on_musics_double_clicked(self, QModelIndex_):
        index = QModelIndex_.row()
        # 把当前歌单的全部音乐加入到播放列表
        self.cur_play_list = MusicList.to_play_list(self.cur_whole_music_list)
        self.cur_play_list.current_music_change.connect(self.on_cur_play_list_change)
        # 找到被双击的音乐在 cur_whole_music_list 中的索引
        music_index = self.cur_whole_music_list.index_of(self.cur_music_list.get(index))
        # print(music_index)
        self.cur_play_list.set_current_index(music_index)
        self.label_play_count.setText(str(self.cur_play_list.get_music_count()))
        self.stop_current()
        self.play()
        self.musics.selectRow(index)

        if self.is_mute:
            self.process.write(b"mute 1\n")
        self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                     "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
        # 读取音乐名片
        self.show_music_info()
        self.state = self.playing_state

    # 显示左下音乐名片相关信息
    def show_music_info(self):
        if self.cur_play_list.get_music_count() > 0:
            music = self.cur_play_list.get_current_music()
            image_data = MP3(music.get_path()).image
            if image_data == b"":
                image = QPixmap("./resource/image/default_music_image.png")
            else:
                image = QPixmap.fromImage(QImage.fromData(image_data))
            max_width = 110
            title = music.get_title()
            artist = music.get_artist()
            self.btn_music_image.setIcon(QIcon(image))

            self.label_music_title.setText(self.get_elided_text(self.label_music_title.font(), title, max_width))
            self.label_music_artist.setText(self.get_elided_text(self.label_music_artist.font(), artist, max_width))

    def init_button(self):
        self.btn_previous.setStyleSheet("QPushButton{border-image:url(./resource/image/上一首.png)}" +
                                        "QPushButton:hover{border-image:url(./resource/image/上一首2.png)}")

        self.btn_next.setStyleSheet("QPushButton{border-image:url(./resource/image/下一首.png)}" +
                                    "QPushButton:hover{border-image:url(./resource/image/下一首2.png)}")

        self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/播放.png)}" +
                                     "QPushButton:hover{border-image:url(./resource/image/播放2.png)}")

        self.btn_mute.setStyleSheet("QPushButton{border-image:url(./resource/image/喇叭.png)}" +
                                    "QPushButton:hover{border-image:url(./resource/image/喇叭2.png)}")

        self.btn_play_mode.setStyleSheet("QPushButton{border-image:url(./resource/image/顺序播放.png)}" +
                                         "QPushButton:hover{border-image:url(./resource/image/顺序播放2.png)}")

        self.btn_desktop_lyric.setStyleSheet("QPushButton{border-image:url(./resource/image/歌词.png)}" +
                                             "QPushButton:hover{border-image:url(./resource/image/歌词2.png)}")

        self.btn_play_list.setStyleSheet("QPushButton{border-image:url(./resource/image/播放列表.png)}" +
                                         "QPushButton:hover{border-image:url(./resource/image/播放列表2.png)}")

        self.label_play_count.setText(str(self.cur_play_list.get_music_count()))
        self.label_play_count.setStyleSheet("QLabel{color: #333333; background-color: #e1e1e2;border-width:1;" +
                                            "border-color:#e1e1e2; border-style: solid; border-radius: 7px;}")

        self.btn_previous.setCursor(Qt.PointingHandCursor)
        self.btn_next.setCursor(Qt.PointingHandCursor)
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_mute.setCursor(Qt.PointingHandCursor)
        self.btn_play_mode.setCursor(Qt.PointingHandCursor)
        self.btn_play_list.setCursor(Qt.PointingHandCursor)
        self.btn_desktop_lyric.setCursor(Qt.PointingHandCursor)

    def init_connect(self):
        self.installEventFilter(self)
        # header
        self.header.installEventFilter(self)
        self.btn_window_close.clicked.connect(self.close)
        self.btn_window_min.clicked.connect(self.showMinimized)
        self.btn_window_max.clicked.connect(self.show_maximized_normal)
        self.btn_icon.clicked.connect(lambda: self.main_stacked_widget.setCurrentWidget(self.main_page))

        # nav
        self.navigation.itemClicked.connect(self.on_nav_clicked)
        self.btn_zoom.installEventFilter(self)
        self.btn_music_image.installEventFilter(self)
        self.music_image_label.installEventFilter(self)
        self.btn_music_image.clicked.connect(self.change_to_play_page)
        self.btn_add_music_list.clicked.connect(self.show_add_music_list_page)
        self.navigation.customContextMenuRequested.connect(self.on_nav_right_click)  # 右键菜单
        self.add_music_list_dialog.cancel.clicked.connect(self.cancel_to_add_music_list)
        self.add_music_list_dialog.confirm.clicked.connect(self.confirm_to_add_music_list)

        # footer & play
        # self.slider.installEventFilter(self)
        self.timer.timeout.connect(self.get_info)
        self.label_lyric.installEventFilter(self)
        self.btn_mute.clicked.connect(self.set_mute)
        self.btn_next.clicked.connect(self.next_music)
        self.btn_start.clicked.connect(self.play_pause)
        self.btn_previous.clicked.connect(self.previous_music)
        self.btn_play_list.clicked.connect(self.show_play_list)
        self.slider_volume.valueChanged.connect(self.set_volume)
        self.slider_progress.sliderReleased.connect(self.seek_music)
        self.cur_play_list.current_music_change.connect(self.on_cur_play_list_change)

        # musics
        self.musics.cellEntered.connect(self.ch_hover_color)
        self.music_list_search.textChanged.connect(self.on_search)
        self.musics.doubleClicked.connect(self.on_musics_double_clicked)
        self.musics.customContextMenuRequested.connect(self.on_musics_right_click)

        # 全屏播放页面
        self.btn_return.clicked.connect(lambda: self.main_stacked_widget.setCurrentWidget(self.main_page))

        # 本地音乐页面
        self.le_search_local_music.textChanged.connect(self.on_search)
        self.tb_local_music.cellEntered.connect(self.on_table_cell_entered)
        self.tb_local_music.customContextMenuRequested.connect(self.on_tb_local_music_right_click)  # 右键菜单

    def init_shortcut(self):
        pause_play_act = QAction(self)
        pause_play_act.setShortcut(Qt.Key_Space)
        self.addAction(pause_play_act)
        pause_play_act.triggered.connect(self.play_pause)

    # 歌单音乐的鼠标滑过变色
    def ch_hover_color(self, row):
        # 先重设全部背景色
        self.interlaced_discoloration()
        # 再设置当前行的颜色
        brush = QBrush(QColor("#ebeced"))
        for i in range(5):
            self.musics.item(row, i).setBackground(brush)

    # 本地音乐的鼠标滑过变色
    def on_table_cell_entered(self, row):
        # 先重设全部背景色
        self.interlaced_discoloration()
        # 再设置当前行的颜色
        brush = QBrush(QColor("#ebeced"))
        for i in range(5):
            self.tb_local_music.item(row, i).setBackground(brush)

    def eventFilter(self, _QObject, _QEvent):
        if _QEvent.type() == QEvent.MouseButtonPress:
            if not self.play_list_page.isHidden():
                self.play_list_page.hide()
        # 1. 如果主窗口被激活, 关闭子窗口
        if _QEvent.type() == QEvent.WindowActivate:
            if not self.play_list_page.isHidden():
                self.play_list_page.hide()
            if not self.add_music_list_dialog.isHidden():
                self.add_music_list_dialog.hide()

        # 2. 如果左下缩放按钮被拖动
        if _QObject == self.btn_zoom:
            if _QEvent.type() == QEvent.MouseMove:
                if _QEvent.buttons() == Qt.LeftButton:
                    global_x = _QEvent.globalX()
                    global_y = _QEvent.globalY()
                    window_global_x = self.x()
                    window_global_y = self.y()
                    width = global_x - window_global_x
                    heigth = global_y - window_global_y
                    self.setGeometry(window_global_x, window_global_y, width, heigth)
        elif _QObject == self.header:
            # 如果标题栏被双击
            if _QEvent.type() == QEvent.MouseButtonDblClick:
                if _QEvent.buttons() == Qt.LeftButton:
                    self.show_maximized_normal()
            # 记录拖动标题栏的位置
            elif _QEvent.type() == QEvent.MouseButtonPress:
                if _QEvent.buttons() == Qt.LeftButton:
                    self.point = _QEvent.globalPos() - self.frameGeometry().topLeft()
            # 如果标题栏被拖动
            elif _QEvent.type() == QEvent.MouseMove:
                if _QEvent.buttons() == Qt.LeftButton:
                    # print(self.windowState() == Qt.WindowMaximized)
                    if self.windowState() == Qt.WindowNoState:
                        self.move(_QEvent.globalPos() - self.point)
        # 3. 当鼠标移动到music_image时显示遮罩层
        if _QObject == self.btn_music_image:
            if _QEvent.type() == QEvent.Enter:
                self.music_image_label.setGeometry(self.btn_music_image.geometry())
                self.music_image_label.show()
        if _QObject == self.music_image_label:
            if _QEvent.type() == QEvent.Leave:
                self.music_image_label.hide()
            if _QEvent.type() == QEvent.MouseButtonPress:
                self.change_to_play_page()
        # 4.
        if _QObject == self.label_lyric:
            if _QEvent.type() == QEvent.Wheel:
                self.is_wheeling = True
            else:
                self.is_wheeling = False
            # print("eventfilter: " + str(self.is_wheeling))
        return super().eventFilter(_QObject, _QEvent)

    def show_maximized_normal(self):
        state = self.windowState()
        if state == Qt.WindowNoState:
            self.setWindowState(Qt.WindowMaximized)
            self.btn_window_max.setStyleSheet("QPushButton{border-image:url(./resource/image/恢复最大化.png)}" +
                                              "QPushButton:hover{border-image:url(./resource/image/恢复最大化2.png)}")
        else:
            self.setWindowState(Qt.WindowNoState)
            self.btn_window_max.setStyleSheet("QPushButton{border-image:url(./resource/image/最大化.png)}" +
                                              "QPushButton:hover{border-image:url(./resource/image/最大化2.png)}")

    # 使播放的相关信息复位
    def info_reset(self):
        self.label_pos.setText("00:00")
        self.label_duration.setText("00:00")
        self.slider_progress.setValue(0)

    def change_to_play_page(self):
        self.main_stacked_widget.setCurrentWidget(self.play_page)
        # print(self.scrollArea.verticalScrollBar().value())
        # self.scrollArea.verticalScrollBar().setValue(560)
        print("scrollArea.height: " + str(self.scrollArea.height()))
        print("scrollArea.maximum: " + str(self.scrollArea.verticalScrollBar().maximum()))
        self.scrollArea.verticalScrollBar().setSliderPosition(585)
        print(self.scrollArea.verticalScrollBar().sliderPosition())
        # print("value: " + str(self.scrollArea.verticalScrollBar().value()))

    def paintEvent(self, _QPaintEvent):
        self.btn_zoom.setGeometry(self.width() - 18, self.height() - 18, 14, 14)
        self.set_tb_local_music_layout()
        if self.cur_music_list is not None:
            self.set_musics_layout()

    def init_ui(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.main_stacked_widget.setCurrentWidget(self.main_page)
        self.stackedWidget_2.setCurrentWidget(self.music_list_detail)
        # ------------------ header------------------ #
        self.header.setStyleSheet("background-color:#c62f2f")
        self.btn_icon.setStyleSheet("QPushButton{border-image:url(./resource/image/icon.png)}")
        self.btn_window_close.setStyleSheet("QPushButton{border-image:url(./resource/image/关闭.png)}" +
                                            "QPushButton:hover{border-image:url(./resource/image/关闭2.png)}")
        self.btn_window_max.setStyleSheet("QPushButton{border-image:url(./resource/image/最大化.png)}" +
                                          "QPushButton:hover{border-image:url(./resource/image/最大化2.png)}")
        self.btn_window_min.setStyleSheet("QPushButton{border-image:url(./resource/image/最小化.png)}" +
                                          "QPushButton:hover{border-image:url(./resource/image/最小化2.png)}")
        self.btn_set.setStyleSheet("QPushButton{border-image:url(./resource/image/设置.png)}" +
                                   "QPushButton:hover{border-image:url(./resource/image/设置2.png)}")
        self.btn_icon.setCursor(Qt.PointingHandCursor)
        self.btn_window_close.setCursor(Qt.PointingHandCursor)
        self.btn_window_max.setCursor(Qt.PointingHandCursor)
        self.btn_window_min.setCursor(Qt.PointingHandCursor)
        self.btn_set.setCursor(Qt.PointingHandCursor)

        # TODO 输入文字后, 前景色变亮
        self.le_search.setPlaceholderText("搜索音乐")
        self.le_search.setStyleSheet("border:none;border-radius:10px;padding:2px 4px; background-color:#a82828;" +
                                     "color:#cccccc;selection-color:yellow;selection-background-color: blue;")
        self.search_act = QAction(self)
        self.search_act.setIcon(QIcon("./resource/image/搜索3.png"))
        self.le_search.addAction(self.search_act, QLineEdit.TrailingPosition)

        # ------------------ 右上歌单相关信息------------------ #
        mln_font = QFont()
        mln_font.setPointSize(20)
        self.music_list_name.setFont(mln_font)
        # self.music_list_name.setText(self.cur_music_list.get_name())
        # self.music_list_date.setText("%s创建" % self.cur_music_list.get_date())
        self.music_count.setStyleSheet("color:#999999")
        self.music_list_play_count.setStyleSheet("color:#999999")
        # self.line.setStyleSheet("background-color:#999999;border:10px")
        self.music_list_image.setPixmap(QPixmap("./resource/image/music_list/rikka.png"))
        self.widget_2.setStyleSheet("background-color:#fafafa;border:none")
        self.label_4.setStyleSheet("QLabel{background-color:#c62f2f; color:white;border:1px solid red}")
        # 歌单音乐列表上方搜索框
        self.music_list_search.setStyleSheet(
            "border:none;border-radius:10px;padding:2px 4px; background-color:#ffffff;" +
            "color:#cccccc;selection-color:yellow;selection-background-color: blue;")
        self.music_list_search.setPlaceholderText("搜索歌单音乐")
        self.search_act = QAction(self)
        self.search_act.setIcon(QIcon("./resource/image/搜索3.png"))
        self.music_list_search.addAction(self.search_act, QLineEdit.TrailingPosition)
        self.main_stacked_widget.setStyleSheet("border-bottom: 1px solid #E1E1E2")

        # ------------------ 左边导航栏 ------------------ #
        self.navigation.setStyleSheet(
            "QListWidget{outline:0px; color:#5c5c5c; background:#f5f5f7;border-top:none;border-left:none; "
            "border-right:1px solid #e1e1e2;border-bottom:1px solid #e1e1e2}"
            "QListWidget::Item{height:32px;border:0px solid gray;padding-left:15;}"
            "QListWidget::Item:hover{color:#000000;background:transparent;border:0px solid gray;}"
            "QListWidget::Item:selected{color:#000000;border:0px solid gray;}"
            "QListWidget::Item:selected:active{background:#e6e7ea;color:#000000;border-left: 3px solid #c62f2f;}")
        self.navigation.setCursor(Qt.PointingHandCursor)
        self.slider_progress.setCursor(Qt.PointingHandCursor)
        # 更改右键策略
        self.navigation.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建歌单按钮
        self.btn_add_music_list = QPushButton(self.navigation)
        self.btn_add_music_list.setCursor(Qt.PointingHandCursor)
        self.btn_add_music_list.setStyleSheet("QPushButton{border-image:url(./resource/image/添加.png)}" +
                                              "QPushButton:hover{border-image:url(./resource/image/添加2.png)}")
        self.btn_add_music_list.setGeometry(160, 39, 18, 18)

        # 点击创建歌单按钮弹出窗口
        self.add_music_list_dialog = add_music_list.AddMusicListDialog()
        # 右下窗口缩放按钮
        self.btn_zoom = QPushButton(self)
        self.btn_zoom.setGeometry(self.width() - 18, self.height() - 18, 14, 14)
        self.btn_zoom.setStyleSheet("QPushButton{border-image:url(./resource/image/缩放.png)}")
        self.btn_zoom.setCursor(Qt.SizeFDiagCursor)

        # ------------------ 左下音乐名片模块 ------------------ #
        self.music_info_widget.setStyleSheet("background-color:#f5f5f7;border:none")
        self.music_info_widget.setCursor(Qt.PointingHandCursor)
        self.btn_music_image.setIconSize(QSize(44, 44))
        self.btn_music_image.setAutoFillBackground(True)
        self.music_image_label = QLabel(self.music_info_widget)
        self.music_image_label.setStyleSheet("QLabel{background-color: rgba(71, 71, 71, 150)}")
        self.music_image_label.setPixmap(QPixmap("./resource/image/全屏.png"))
        self.music_image_label.hide()
        self.show_music_info()

        # ------------------ footer ------------------ #
        self.slider_volume.setValue(self.volume)
        self.slider_volume.setCursor(Qt.PointingHandCursor)
        self.footer.setStyleSheet(
            "QWidget{background-color:#f6f6f8; border:none;outline:0px;border-top:1px solid #e1e1e2}")
        self.slider_progress.setStyleSheet("QSlider::groove:horizontal{border:0px;height:4px;}"
                                           "QSlider::sub-page:horizontal{background:#e83c3c;}"
                                           "QSlider::add-page:horizontal{background:#c2c2c4;} "
                                           "QSlider::handle:horizontal{background:white;width:10px;border:#51b5fb 10px;border-radius:5px;margin:-3px 0px -3px 0px;}"
                                           "QSlider{border:none}")
        self.slider_volume.setStyleSheet("QSlider::groove:horizontal{border:0px;height:4px;}"
                                         "QSlider::sub-page:horizontal{background:#e83c3c;}"
                                         "QSlider::add-page:horizontal{background:#e6e6e8;} "
                                         "QSlider::handle:horizontal{background:white;width:10px;border:#51b5fb 10px;border-radius:5px;margin:-3px 0px -3px 0px;}"
                                         "QSlider{border:none}")

        # ------------------ 全屏播放窗口 ------------------ #
        self.play_page.setStyleSheet("border-image:url(./resource/image/渐变背景.png) repeated;border:none; ")
        self.label_title.setStyleSheet("border-image:none")
        self.label_album.setStyleSheet("border-image:none")
        self.label_artist.setStyleSheet("border-image:none")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa;width:10px;border:none}"
                                                          "QScrollBar::handle{background-color:#e1e1e2; border:none;}"
                                                          "QScrollBar::handle:hover{background:#adb0b4;}"
                                                          "QScrollBar::sub-line{background-color:#e1e1e2;}"
                                                          "QScrollBar::add-line{background-color:#e1e1e2}"
                                                          "QScrollBar::add-page{background-color:#ebebe9;}"
                                                          "QScrollBar::sub-page{background-color:#ebebe9;}")
        self.btn_return.setStyleSheet(
            "QPushButton{border-image:url(./resource/image/取消全屏.png);border-radius:5px;border-color:#dadadb}" +
            "QPushButton:hover{border-image:url(./resource/image/取消全屏2.png)}")
        self.btn_return.setCursor(Qt.PointingHandCursor)
        # max: 0
        s = "<p>1</p><p>2</p><p>3</p><p>4</p><p>5</p><p>6</p><p>7</p><p>8</p><p>9</p><p>10</p><p>11</p>" \
            "<p>12</p><p>13</p><p>14</p><p>15</p>" \
            "<p>16</p><p>17</p><p>18</p>" \
            "<p>19</p><p>20</p><p>21</p><p>22</p><p>23</p><p>24</p><p>25</p><p style='color:white'>26</p><p>27</p>" \
            "<p>28</p><p>29</p><p>30</p><p>31</p><p>32</p><p>33</p><p>34</p><p>35</p><p>36</p><p>37</p><p>&nbsp;</p><p>38</p><p>&nbsp;</p><p>壊すわ</p>"
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>"
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>"

        self.label_lyric.setText(s)

        # 右下播放列表页面
        self.play_list_page = ui.test.PlayListPage(self)

        # 本地音乐页面
        self.widget.setStyleSheet("QWidget#widget{background-color:#fafafa;border:none;}")
        self.btn_choose_dir.setFlat(True)
        self.btn_choose_dir.setStyleSheet("background:none;color:#0a63a8")
        # 搜索框
        self.le_search_local_music.setStyleSheet(
            "QLineEdit#le_search_local_music{border:none;border-radius:10px;padding:2px 4px; background-color:#ffffff;" +
            "color:#000000;selection-color:yellow;selection-background-color: blue;}")
        self.le_search_local_music.setPlaceholderText("搜索本地音乐")
        self.search_act_2 = QAction(self)
        self.search_act_2.setIcon(QIcon("./resource/image/搜索3.png"))
        self.le_search_local_music.addAction(self.search_act_2, QLineEdit.TrailingPosition)

    def show_play_list(self):
        self.play_list_page.show()
        self.play_list_page.show_data(self.cur_play_list)

    def show_add_music_list_page(self):
        self.add_music_list_dialog.lineEdit.clear()
        self.add_music_list_dialog.setGeometry(QCursor.pos().x() + 30, QCursor.pos().y(), 270, 200)
        self.add_music_list_dialog.show()
        self.add_music_list_dialog.lineEdit.setFocus()

    def confirm_to_add_music_list(self):
        text = self.add_music_list_dialog.lineEdit.text()
        if len(text) > 0:
            ml = MusicList()
            ml.set_name(text)
            MusicList.to_disk(ml)
            self.navigation.clear()
            self.init_data()
            self.add_music_list_dialog.hide()

    def cancel_to_add_music_list(self):
        self.add_music_list_dialog.hide()

    # 显示nav右键菜单
    def on_nav_right_click(self, pos):
        item = self.navigation.itemAt(pos)
        if item is not None and item.text() != "创建的歌单":
            self.menu = QMenu()
            act1 = QAction("播放(Enter)", self)
            act1.setIcon(QIcon("./resource/image/nav-播放.png"))

            act2 = QAction("删除歌单(Delete)", self)
            act2.setIcon(QIcon("./resource/image/nav-删除.png"))
            act2.triggered.connect(lambda: self.del_music_list(item.text()))
            self.menu.addAction(act1)
            self.menu.addSeparator()
            self.menu.addAction(act2)
            self.menu.exec(QCursor.pos())

    def on_musics_right_click(self, pos):
        self.musics_menu = Menu()
        act1 = QAction("播放(Enter)", self)
        # act1.setIcon(QIcon("./resource/image/nav-播放.png"))

        act2 = QAction("下一首播放", self)
        # act2.setIcon(QIcon("./resource/image/nav-删除.png"))
        act3 = QAction("收藏到歌单(Ctrl+S)", self)
        act4 = QAction("打开文件所在目录", self)
        act5 = QAction("从歌单中删除(Delete)", self)

        # 获取被选中的行, 包括列
        items = self.musics.selectedItems()
        # 被选中的行号
        rows = set()
        for item in items:
            rows.add(item.row())
        self.musics_menu.addAction(act1)
        self.musics_menu.addAction(act2)
        self.musics_menu.addAction(act3)
        # 只选中了一行
        if len(rows) == 1:
            self.musics_menu.addSeparator()
            self.musics_menu.addAction(act4)
        else:
            self.musics_menu.addSeparator()
        self.musics_menu.addAction(act5)
        act1.triggered.connect(lambda: self.on_act1_play(rows))
        act2.triggered.connect(lambda: self.on_act2_next_play(rows))
        # todo hover
        act3.hovered.connect(lambda: self.on_act3_collect(rows))
        act4.triggered.connect(lambda: self.on_act4_open_file(rows))
        act5.triggered.connect(lambda: self.on_act5_del(rows))
        self.musics_menu.exec(QCursor.pos())

    # 选中歌单列表的音乐, 点击 "播放"
    def on_act1_play(self, rows):
        # 1. 选中的音乐依次在current index后加入播放列表
        # 2. 若选中的音乐已在播放列表中, 则移除已存在的, 然后重新加入
        # 3. 播放第一个选中的音乐
        for row in rows:
            # todo 移除播放列表的同歌单的同歌曲(by path & from)
            music = self.cur_music_list.get(row)
            # print(music)
            self.cur_play_list.remove(music)
        cur_index = self.cur_play_list.get_current_index()
        for row in rows:
            music = self.cur_music_list.get(row)
            cur_index += 1
            self.cur_play_list.insert_music(cur_index, music)
        self.label_play_count.setText(str(self.cur_play_list.get_music_count()))
        self.cur_play_list.set_current_index(self.cur_play_list.get_current_index() + 1)
        self.stop_current()
        self.play()
        self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                     "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
        if self.is_mute:
            self.process.write(b"mute 1\n")
        self.state = self.playing_state
        self.show_music_info()

    # 选中歌单列表的音乐, 点击 "下一首播放"
    def on_act2_next_play(self, rows):
        # 1. 选中的音乐依次在current index后加入播放列表
        # 2. 若选中的音乐已在播放列表中, 则移除已存, 然后重新加入
        for row in rows:
            music = self.cur_music_list.get(row)
            self.cur_play_list.remove(music)
        cur_index = self.cur_play_list.get_current_index()
        for row in rows:
            music = self.cur_music_list.get(row)
            cur_index += 1
            self.cur_play_list.insert_music(cur_index, music)
        self.label_play_count.setText(str(self.cur_play_list.get_music_count()))

    def on_act3_collect(self, rows):
        self.collect_menu = QMenu()
        act0 = QAction("创建新歌单", self)
        # act1.setIcon(QIcon("./resource/image/nav-播放.png"))
        self.collect_menu.addAction(act0)
        self.collect_menu.addSeparator()
        music_lists = util.get_music_lists()
        for music_list in music_lists:
            act = QAction(music_list.get_name(), self.collect_menu)
            self.collect_menu.addAction(act)
            act.triggered.connect(lambda: self.on_acts_choose(rows))

        self.collect_menu.exec(QCursor.pos())

    # 选中歌单列表的音乐, 点击 "打开文件所在目录"
    def on_act4_open_file(self, rows):
        if len(rows) == 1:
            music = self.cur_music_list.get(rows.pop())
            command = "explorer /select, %s" % music.get_path().replace("/", "\\")
            os.system(command)

    # 选中歌单列表的音乐, 点击 "从歌单中删除"
    def on_act5_del(self, rows):
        dels = []
        for row in rows:
            music = self.cur_music_list.get(row)
            dels.append(music)
        for del_music in dels:
            self.cur_music_list.remove(del_music)
        MusicList.to_disk(self.cur_music_list)
        self.show_musics_data()
        # 清除已选择的项
        self.musics.clearSelection()

    def on_acts_choose(self, rows):
        # 1. 在目标歌单的末尾加入; 2. 已存在的音乐则不加入(根据path判断)
        sender = self.sender()
        music_list_name = sender.text()
        target_music_list = MusicList.from_disk("./resource/config/%s" % music_list_name)
        is_all_in = True
        for row in rows:
            if self.stackedWidget_2.currentWidget() == self.music_list_detail:
                music = self.cur_music_list.get(row)
            elif self.stackedWidget_2.currentWidget() == self.local_music_page:
                music = self.cur_local_music_list.get(row)
            if not target_music_list.contains(music.get_path()):
                is_all_in = False
                target_music_list.add(music)
        if not is_all_in:
            Toast.show_(self, "已收藏到歌单", True, 2000)
        else:
            Toast.show_(self, "歌曲已存在!", False, 2000)
        MusicList.to_disk(target_music_list)

    def on_tb_local_music_right_click(self, pos):
        self.lm_menu = QMenu()
        act1 = QAction("播放(Enter)", self.lm_menu)
        # act1.setIcon(QIcon("./resource/image/nav-播放.png"))

        act2 = QAction("下一首播放", self.lm_menu)
        # act2.setIcon(QIcon("./resource/image/nav-删除.png"))
        act3 = QAction("收藏到歌单(Ctrl+S)", self.lm_menu)
        act4 = QAction("打开文件所在目录", self.lm_menu)
        act5 = QAction("从本地磁盘删除)", self.lm_menu)

        # 获取被选中的行, 包括列
        items = self.tb_local_music.selectedItems()
        # 被选中的行号
        rows = set()
        for item in items:
            rows.add(item.row())
        self.lm_menu.addAction(act1)
        self.lm_menu.addAction(act2)
        self.lm_menu.addAction(act3)
        # 只选中了一行
        if len(rows) == 1:
            self.lm_menu.addSeparator()
            self.lm_menu.addAction(act4)
        else:
            self.lm_menu.addSeparator()
        self.lm_menu.addAction(act5)
        act1.triggered.connect(lambda: self.on_lm_act1_play(rows))
        act2.triggered.connect(lambda: self.on_lm_act2_next_play(rows))
        # todo hover
        act3.hovered.connect(lambda: self.on_lm_act3_collect(rows))
        act4.triggered.connect(lambda: self.on_lm_act4_open_file(rows))
        act5.triggered.connect(lambda: self.on_lm_act5_del(rows))
        self.lm_menu.exec(QCursor.pos())

    def on_lm_act1_play(self, rows):
        # 1. 选中的音乐依次在current index后加入播放列表
        # 2. 播放第一个选中的音乐
        # print(rows)
        cur_index = self.cur_play_list.get_current_index()
        # print(self.cur_play_list)
        for row in rows:
            music = self.cur_local_music_list.get(row)
            # print(music)
            cur_index += 1
            self.cur_play_list.insert_music(cur_index, music)
        # print(self.cur_play_list)
        self.label_play_count.setText(str(self.cur_play_list.get_music_count()))
        self.cur_play_list.set_current_index(self.cur_play_list.get_current_index() + 1)
        self.stop_current()
        self.play()
        self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                     "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
        if self.is_mute:
            self.process.write(b"mute 1\n")
        self.state = self.playing_state
        self.show_music_info()

    def on_lm_act2_next_play(self, rows):
        # 1. 选中的音乐依次在current index后加入播放列表
        cur_index = self.cur_play_list.get_current_index()
        for row in rows:
            music = self.cur_local_music_list.get(row)
            cur_index += 1
            self.cur_play_list.insert_music(cur_index, music)
        self.label_play_count.setText(str(self.cur_play_list.get_music_count()))

    def on_lm_act3_collect(self, rows):
        self.collect_menu = QMenu()
        act0 = QAction("创建新歌单", self)
        # act1.setIcon(QIcon("./resource/image/nav-播放.png"))
        self.collect_menu.addAction(act0)
        self.collect_menu.addSeparator()
        music_lists = util.get_music_lists()
        for music_list in music_lists:
            act = QAction(music_list.get_name(), self.collect_menu)
            self.collect_menu.addAction(act)
            act.triggered.connect(lambda: self.on_acts_choose(rows))

        self.collect_menu.exec(QCursor.pos())

    def on_lm_act4_open_file(self, rows):
        if len(rows) == 1:
            music = self.cur_local_music_list.get(rows.pop())
            command = "explorer /select, %s" % music.get_path().replace("/", "\\")
            os.system(command)

    def on_lm_act5_del(self, rows):
        if 1 == 0:
            for row in rows:
                music = self.cur_local_music_list.get(row)
                os.remove(music.get_path())
            self.show_local_music_page_data()
            # 清除已选择的项
            self.tb_local_music.clearSelection()

    def del_music_list(self, music_list_name):
        path = "./resource/config/%s" % music_list_name
        MusicList.remove_from_disk(path)
        self.navigation.clear()
        self.init_data()

    def on_search(self, text):
        text = text.strip()
        if self.stackedWidget_2.currentWidget() == self.music_list_detail:
            if len(text) != 0:
                self.cur_music_list = self.cur_whole_music_list.search(text)
            else:
                path = "./resource/config/"
                text = self.navigation.currentItem().text()
                self.cur_music_list = MusicList.from_disk(path + text)
            # self.show_musics_data()
            self.show_icon_item()
        elif self.stackedWidget_2.currentWidget() == self.local_music_page:
            if len(text) != 0:
                self.cur_local_music_list = self.cur_whole_local_music_list.search(text)
            else:
                self.cur_local_music_list = SearchLocalMusic.get_exist_result()
            self.show_local_music_page_data()

    # 为musics(tablewidget)的某一行显示喇叭图片
    def show_icon_item(self):
        if self.stackedWidget_2.currentWidget() == self.music_list_detail:
            # 总是要设置数据
            self.show_musics_data()
            # print("equal   ",
            #       self.cur_play_list.get_current_music().get_from().get_name() == self.cur_music_list.get_name())
            # print(self.cur_play_list.get_current_music())
            if self.cur_play_list.get_current_music() is not None:
                if self.cur_play_list.get_current_music().get_from().get_name() == self.cur_music_list.get_name():
                    playing_row = self.cur_music_list.index_of(self.cur_play_list.get_current_music())
                    if playing_row != -1:
                        # 先把之前的喇叭恢复成数字(目前无法确定上一首音乐的位置, 只能重新全部设置数据)
                        # self.show_musics_data()
                        # 再设置喇叭图标
                        self.musics.item(playing_row, 0).setText("")
                        icon_label = QLabel()
                        icon_label.setPixmap(QPixmap("./resource/image/musics_play.png"))
                        icon_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.musics.setCellWidget(playing_row, 0, icon_label)
        elif self.stackedWidget_2.currentWidget() == self.local_music_page:
            # todo 本地音乐页面的喇叭图标
            pass
            # self.show_local_music_page_data()
        if self.cur_play_list is not None:
            self.play_list_page.show_data(self.cur_play_list)

    def on_cur_play_list_change(self, music):
        self.show_icon_item()

    def play_pause(self):
        if self.cur_play_list is not None:
            if self.state == self.stopped_state:
                self.play()
                self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                             "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
                if self.is_mute:
                    self.process.write(b"mute 1\n")
                self.state = self.playing_state
            elif self.state == self.playing_state:
                self.process.write(b"pause\n")
                self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/播放.png)}" +
                                             "QPushButton:hover{border-image:url(./resource/image/播放2.png)}")
                self.state = self.paused_state
            elif self.state == self.paused_state:
                if self.process is None:
                    self.play()
                    self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                                 "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
                    if self.is_mute:
                        self.process.write(b"mute 1\n")
                    self.state = self.playing_state
                else:
                    self.process.write(b"pause\n")
                    self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                                 "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
                    # 如果进度条被拖动
                    if self.percent_pos != -0.1:
                        pos = int(self.percent_pos * self.duration)
                        self.process.write(b"seek %d 2\n" % pos)
                        self.percent_pos = -0.1
                    self.state = self.playing_state

    # 设置音量
    def set_volume(self, value):
        if self.process is not None:
            self.process.write(b"volume %d 50\n" % value)
            self.volume = value
        else:
            self.volume = value

    def get_elided_text(self, _QFont, _str, max_width):
        fm = QFontMetrics(_QFont)
        # 计算字符串宽度
        w = fm.width(_str)
        # 当字符串宽度大于最大宽度时进行转换
        if w < max_width:
            return _str
        else:
            return self.sub(_str, max_width, fm)

    def sub(self, s, max_width, fm):
        w = fm.width(s)
        if w < max_width:
            return s + "..."
        else:
            return self.sub(s[0:-1], max_width, fm)

    def stop_current(self):
        if self.process is not None:
            self.process.kill()
            self.process = None

    def get_info(self):
        if self.process is not None:
            if self.state == self.playing_state:
                self.process.write(b"get_time_length\n")
                self.process.write(b"get_time_pos\n")

    # 抽取出来的播放方法, 注意: 对播放状态的调整应由自己控制
    def play(self):
        music = self.cur_play_list.get_current_music()
        self.process = QProcess(self)
        command = "./lib/mplayer.exe -slave -quiet -volume %d \"%s\"" % (self.volume, music.get_path())
        self.process.start(command)
        # 连接信号
        self.process.readyReadStandardOutput.connect(self.show_play_info)
        self.process.readyReadStandardError.connect(self.error_output)

    def show_play_info(self):
        duration_regex = "ANS_LENGTH=(.*?)\\\\r"
        duration_pattern = re.compile(duration_regex)
        position_regex = "ANS_TIME_POSITION=(.*?)\\\\r"
        position_pattern = re.compile(position_regex)
        # 歌词
        lrc = LRC("./resource/周杰伦 - 星晴.lrc")

        while self.process.canReadLine():
            output = str(self.process.readLine())
            # print(output)
            duration_match = duration_pattern.search(output)
            position_match = position_pattern.search(output)
            # 处理时长
            if duration_match is not None:
                d = duration_match.group(1)
                self.duration = float(d)
                format_duration = util.format_time(d)
                self.label_duration.setText(format_duration)
            # 处理播放位置
            if position_match is not None:
                p = position_match.group(1)
                position = util.format_time(p)
                self.label_pos.setText(position)

                time = int(float(p) * 1000)
                # print(time)
                # self.label_lyric.setText(lrc.show(time))
                self.lrc_scroll(lrc, time)
                if self.duration != -1:
                    slider_position = int(float(p) / self.duration * 100)
                    if not self.slider_progress.isSliderDown():
                        self.slider_progress.setValue(slider_position)
            # 一曲放完
            if output.find("Exiting... (End of file)") != -1:
                print("一曲完毕, 播放下一曲")
                self.info_reset()
                self.stop_current()
                self.cur_play_list.next()
                self.show_music_info()
                self.play()
                if self.is_mute:
                    self.process.write(b"mute 1\n")

    def lrc_scroll(self, lrc, time):
        # print(self.scrollArea.height())
        # print(self.scrollArea.verticalScrollBar().maximum())
        # pos = (line - 15) * 31 + 489/2
        ret = lrc.show(time)
        cur_line = ret[0]
        # print("%d %d" % (ret[0], ret[1]))
        # pos = (ret[0] - 15) * 31 + self.scrollArea.height() / 2
        pos = ret[1] * 34 + (ret[0] - 15 - ret[1]) * 31 + self.scrollArea.height() / 2
        # print(str(ret[1]) + " " + str(pos))
        # print(self.is_wheeling)
        if not self.is_wheeling:
            self.scrollArea.verticalScrollBar().setSliderPosition(pos)
        self.label_lyric.setText(ret[2])

    def error_output(self):
        while self.process.canReadLine():
            output = str(self.process.readLine())
            print("!" * 10 + " \nHere is the error output")
            print(output)
            print("!" * 10 + "error output end")

    def previous_music(self):
        if self.cur_play_list is not None:
            self.info_reset()
            self.stop_current()
            self.cur_play_list.previous()
            self.show_music_info()
            if self.state == self.playing_state:
                self.play()
                if self.is_mute:
                    self.process.write(b"mute 1\n")

    def next_music(self):
        if self.cur_play_list is not None:
            self.info_reset()
            self.stop_current()
            self.cur_play_list.next()
            self.show_music_info()
            if self.state == self.playing_state:
                self.play()
                if self.is_mute:
                    self.process.write(b"mute 1\n")

    # 定位到音乐的指定绝对位置, 秒
    def seek_music(self):
        value = self.slider_progress.value()
        if self.state == self.playing_state:
            pos = value / 100 * self.duration
            self.process.write(b"seek %d 2\n" % pos)
        elif self.state == self.paused_state:
            self.percent_pos = value / 100

    def set_mute(self):
        if self.is_mute:
            if self.state == self.playing_state:
                self.process.write(b"mute 0\n")
            self.is_mute = False
            self.btn_mute.setStyleSheet("QPushButton{border-image:url(./resource/image/喇叭.png)}" +
                                        "QPushButton:hover{border-image:url(./resource/image/喇叭2.png)}")
        else:
            if self.state == self.playing_state:
                self.process.write(b"mute 1\n")
            self.btn_mute.setStyleSheet("QPushButton{border-image:url(./resource/image/取消静音.png)}" +
                                        "QPushButton:hover{border-image:url(./resource/image/取消静音2.png)}")
            self.is_mute = True

    def closeEvent(self, QCloseEvent):
        self.stop_current()


def main():
    app = QtWidgets.QApplication(sys.argv)
    # qss = open("./resource/qss/main.qss", "r", encoding="utf-8")
    # read = qss.read()
    # app.setStyleSheet(read)
    my_window = MyWindow()
    my_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
