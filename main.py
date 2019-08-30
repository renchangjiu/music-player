import re, os, sys
import threading
import winreg

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QProcess, QEvent, QSize, QModelIndex, QObject
from PyQt5.QtGui import QPixmap, QFont, QIcon, QImage, QFontMetrics, QCursor, QCloseEvent, QMouseEvent, QMovie, \
    QPaintEvent
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QListWidgetItem, QTableWidgetItem, \
    QAction, QMenu, QLabel, QWidgetAction, QHBoxLayout, QTextEdit

from src.service.check_program import CheckProgram
from src.neteaseCloudMusicApi.api import NeteaseCloudMusicApi
from src.service.LRCParser import LRC
from src.service.MP3Parser import MP3
from src.service.global_variable import GlobalVar
from src.service.main_widget import Ui_Form
from src.entity.music_list import MusicList
from src.service.music_list_service import MusicListService
from src.service.music_service import MusicService
from src.ui import add_music_list
from src.ui.choose_music_dir import ChooseMusicDirPage
from src.ui.play_list_page import PlayListPage
from src.service import util
from src.service.search_local_music import SearchLocalMusic

from src.ui.toast import Toast


# TODO 滚动歌词: verticalScrollBar.setValue()
# TODO 如果要播放的文件不存在:  0. 右键播放, 1. 正在的播放的文件被删除, 4. 双击歌单列表, 但目标文件已被删除,
#  5. 双击播放列表, ..., 6. 要删除已被删除的文件
# TODO table widget 列宽可调节
# TODO UI细节调整
# todo 歌单图片
# TODO 重构 & 拆分入口文件

class MainWindow(QWidget, Ui_Form):
    # 播放状态
    stopped_state = 0  # 该状态已被废弃
    playing_state = 1
    paused_state = 2

    def __init__(self):
        QWidget.__init__(self)
        Ui_Form.__init__(self)

        self.music_list_service = MusicListService()
        self.music_service = MusicService()

        # 播放信息
        self.process = None
        # 音量
        self.volume = 50
        # 音乐时长
        self.duration = -1
        # 播放状态
        self.state = self.paused_state
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

        self.setupUi(self)

        self.init_menu()
        self.init_data()
        self.init_table_widget_ui()
        self.init_ui()
        self.init_shortcut()
        self.init_connect()
        self.min = self.scrollArea.verticalScrollBar().minimum()

        # 重新搜索本地音乐
        self.research_local_music()

    def research_local_music(self):
        search_local_music = SearchLocalMusic()
        search_local_music.begin_search.connect(self.begin_search)
        search_local_music.end_search.connect(self.end_search)
        thread = threading.Thread(target=lambda: self.sub_thread(search_local_music))
        thread.start()

    def begin_search(self):
        print("搜索开始")
        self.label_search_gif = QLabel(self.navigation)
        movie = QMovie("./resource/image/1.gif")
        self.label_search_gif.setMovie(movie)
        self.label_search_gif.setGeometry(160, 9, 16, 16)
        self.label_search_gif.show()
        movie.start()
        movie.setSpeed(90)
        self.label_search_state.setText("正在更新本地音乐列表...")

    def end_search(self):
        print("搜索结束")
        self.label_search_gif.hide()
        self.label_search_state.setText("更新完成")

    def sub_thread(self, search_local_music):
        paths = ChooseMusicDirPage.get_music_path()
        temp = []
        for path in paths:
            if path[1] == "checked" and os.path.exists(path[0]):
                temp.append(path[0])
        search_local_music.search_in_path(temp)

    def init_data(self):
        self.navigation.setIconSize(QSize(18, 18))
        font = QFont()
        font.setPixelSize(13)
        local_item = QListWidgetItem(self.navigation)
        local_item.setData(Qt.UserRole, self.music_list_service.get_local_music())
        local_item.setIcon(QIcon("./resource/image/本地音乐.png"))
        local_item.setText("本地音乐")
        local_item.setFont(font)

        self.navigation.addItem(local_item)

        item1 = QListWidgetItem()
        item1.setText("创建的歌单")
        item1.setFlags(Qt.NoItemFlags)
        self.navigation.addItem(item1)

        all_music_list = self.music_list_service.get_all_music_list()
        music_list_icon = QIcon("./resource/image/歌单.png")
        for music_list in all_music_list:
            item = QListWidgetItem()
            item.setIcon(music_list_icon)
            item.setFont(font)
            item.setText(music_list.get_name())
            item.setData(Qt.UserRole, music_list)
            self.navigation.addItem(item)

        # 启动时默认选中第一个歌单
        self.navigation.setCurrentRow(0)
        cur_id = self.navigation.currentItem().data(Qt.UserRole).get_id()

        self.update_music_list(cur_id)

        self.stackedWidget_2.setCurrentWidget(self.music_list_detail)
        self.musics.setColumnCount(5)
        # 将歌单中的歌曲列表加载到 table widget
        if self.cur_play_list is None:
            self.cur_play_list = self.music_list_service.to_play_list(self.cur_music_list)
            self.cur_play_list.set_current_index(0)
            self.cur_play_list.current_music_change.connect(self.on_cur_play_list_change)
        self.show_musics_data()

    def init_table_widget_ui(self):
        # --------------------- 1. 歌单音乐列表UI --------------------- #
        self.musics.setHorizontalHeaderLabels(["", "音乐标题", "歌手", "专辑", "时长"])
        self.musics.setColumnCount(5)
        self.musics.setStyleSheet("QTableWidget{border:none;background:#fafafa;}" +
                                  "QTableWidget::item::selected{background:#e3e3e5}")
        # 设置表头
        self.musics.horizontalHeader().setStyleSheet(
            """QHeaderView::section{background:#fafafa;border:none;border-right:1px solid #e1e1e2;height:30px;}
            QHeaderView::section:hover{background:#ebeced;border:none}
            QHeaderView{color:#666666; border-top:1px solid #c62f2f;}
            """)

        # --------------------- 2. 本地音乐页面UI--------------------- #
        self.tb_local_music.setColumnCount(6)
        self.tb_local_music.setHorizontalHeaderLabels(["", "音乐标题", "歌手", "专辑", "时长", "大小"])
        self.tb_local_music.setStyleSheet("QTableWidget{border:none}" +
                                          "QTableWidget::item::selected{background:#e3e3e5}")
        # 设置表头
        self.tb_local_music.horizontalHeader().setStyleSheet(
            """QHeaderView::section{background:#fafafa;border:none;border-right:1px solid #e1e1e2;height:30px;}
            QHeaderView::section:hover{background:#eceeed;border:none;}
            QHeaderView{color:#666666; border-top:1px solid #e1e1e2;}
            """)

    # 当点击navigation时, 显示对应页面
    def on_nav_clicked(self, list_item: QListWidgetItem):
        data = list_item.data(Qt.UserRole)
        if data is None:
            return

        if data.get_id() == 0:
            self.show_local_music_page()
        else:
            cur_id = data.get_id()
            self.update_music_list(cur_id)
            self.stackedWidget_2.setCurrentWidget(self.music_list_detail)
            self.set_musics_layout()
            # 加载歌单中的歌曲列表
            self.show_musics_data()
            self.musics.setCurrentCell(0, 0)

    # 将歌单中的歌曲列表加载到 table widget(需先设置行列数)
    def show_musics_data(self):
        self.music_list_name.setText(self.cur_music_list.get_name())
        self.music_list_date.setText("%s创建" % self.cur_music_list.get_created())
        self.music_count.setText("<p>歌曲数</p><p style='text-align: right'>%d</p>" % self.cur_music_list.size())
        self.music_list_play_count.setText(
            "<p>播放数</p><p style='text-align: right'>%d</p>" % self.cur_music_list.get_play_count())

        self.musics.clearContents()
        self.musics.setRowCount(self.cur_music_list.size())
        musics__ = self.cur_music_list
        for i in range(musics__.size()):
            music = musics__.get(i)
            item = QTableWidgetItem()
            item.setData(Qt.UserRole, music)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setText(str(i + 1) + " ")
            self.musics.setItem(i, 0, item)
            item = QTableWidgetItem(str(music.get_title()))
            item.setToolTip(music.get_title())
            self.musics.setItem(i, 1, item)
            item = QTableWidgetItem(str(music.get_artist()))
            item.setToolTip(music.get_artist())
            self.musics.setItem(i, 2, item)
            item = QTableWidgetItem(str(music.get_album()))
            item.setToolTip(music.get_album())
            self.musics.setItem(i, 3, item)
            item = QTableWidgetItem(str(util.format_time(music.get_duration())))
            item.setToolTip(str(util.format_time(music.get_duration())))
            self.musics.setItem(i, 4, item)
        # 若当前播放的音乐属于该歌单, 则为其设置喇叭图标
        self.set_icon_item()

    # 展示本地音乐页面的表格数据
    def show_local_music_page_data(self):
        self.label_2.setText("%d首音乐" % self.cur_whole_music_list.size())
        self.tb_local_music.clearContents()
        self.tb_local_music.setRowCount(self.cur_music_list.size())
        self.set_tb_local_music_layout()
        for i in range(self.cur_music_list.size()):
            music = self.cur_music_list.get(i)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setText(str(i + 1) + " ")
            self.tb_local_music.setItem(i, 0, item)
            item = QTableWidgetItem(music.get_title())
            item.setToolTip(str(music.get_title()))
            self.tb_local_music.setItem(i, 1, item)
            item = QTableWidgetItem(music.get_artist())
            item.setToolTip(str(music.get_artist()))
            self.tb_local_music.setItem(i, 2, item)
            item = QTableWidgetItem(music.get_album())
            item.setToolTip(str(music.get_album()))
            self.tb_local_music.setItem(i, 3, item)
            item = QTableWidgetItem(str(util.format_time(music.get_duration())))
            item.setToolTip(str(util.format_time(music.get_duration())))
            self.tb_local_music.setItem(i, 4, item)
            item = QTableWidgetItem(str(music.get_size()))
            item.setToolTip(str(music.get_size()))
            self.tb_local_music.setItem(i, 5, item)
        self.set_icon_item()

    # 若当前播放的音乐属于该歌单, 则为其设置喇叭图标
    def set_icon_item(self):
        if self.cur_play_list is not None:
            if self.cur_play_list.get_current_music() is not None:
                # 找到当前播放的音乐在该歌单中的索引
                playing_row = self.music_list_service.index_of(self.cur_play_list.get_current_music(),
                                                               self.cur_music_list)
                if playing_row != -1:
                    icon_label = QLabel()
                    # 播放状态或暂停状态显示两种图标
                    if self.state == self.playing_state:
                        icon_label.setPixmap(QPixmap("./resource/image/musics_play.png"))
                    else:
                        icon_label.setPixmap(QPixmap("./resource/image/musics_pause.png"))
                    icon_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    # 区分歌单页面和本地音乐页面
                    if self.stackedWidget_2.currentWidget() == self.music_list_detail:
                        self.musics.item(playing_row, 0).setText("")
                        self.musics.setCellWidget(playing_row, 0, icon_label)
                    elif self.stackedWidget_2.currentWidget() == self.local_music_page:
                        self.tb_local_music.item(playing_row, 0).setText("")
                        self.tb_local_music.setCellWidget(playing_row, 0, icon_label)

    def show_local_music_page(self):
        self.stackedWidget_2.setCurrentWidget(self.local_music_page)
        self.cur_music_list = self.music_list_service.get_local_music()
        self.cur_whole_music_list = self.music_list_service.get_local_music()
        self.show_local_music_page_data()

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

    # 当存放音乐列表的表格被双击
    def on_tb_double_clicked(self, model_index: QModelIndex):
        self.state = self.playing_state
        index = model_index.row()
        # 把当前歌单的全部音乐加入到播放列表
        self.cur_play_list = self.music_list_service.to_play_list(self.cur_whole_music_list)
        self.cur_play_list.current_music_change.connect(self.on_cur_play_list_change)
        # 找到被双击的音乐在 cur_whole_music_list 中的索引
        self.cur_play_list.set_current_index(index)
        self.label_play_count.setText(str(self.cur_play_list.size()))
        self.stop_current()
        self.play()
        self.musics.selectRow(index)

        if self.is_mute:
            self.process.write(b"mute 1\n")
        self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                     "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
        # 读取音乐名片
        self.show_music_info()

    # 显示左下音乐名片相关信息
    def show_music_info(self):
        if self.cur_play_list.size() > 0:
            if self.music_info_widget.isHidden():
                self.music_info_widget.show()
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
        else:
            self.music_info_widget.hide()

    def init_button(self):
        self.label_play_count.setText(str(self.cur_play_list.size()))
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
        self.navigation.customContextMenuRequested.connect(self.on_nav_right_click)  # 右键菜单
        self.btn_zoom.installEventFilter(self)
        self.btn_music_image.installEventFilter(self)
        self.music_image_label.installEventFilter(self)
        self.btn_music_image.clicked.connect(self.change_to_play_page)
        self.btn_add_music_list.clicked.connect(self.show_add_music_list_page)
        self.add_music_list_dialog.cancel.clicked.connect(self.cancel_to_add_music_list)
        self.add_music_list_dialog.confirm.clicked.connect(self.confirm_to_add_music_list)

        # footer & play
        # self.slider.installEventFilter(self)
        self.timer.timeout.connect(self.get_info)
        # 歌词滚动
        # self.label_lyric.installEventFilter(self)
        self.btn_mute.clicked.connect(self.set_mute)
        self.btn_next.clicked.connect(self.next_music)
        self.btn_start.clicked.connect(self.play_pause)
        self.btn_previous.clicked.connect(self.previous_music)
        self.btn_play_list.clicked.connect(self.show_play_list)
        self.slider_volume.valueChanged.connect(self.set_volume)
        self.slider_progress.sliderReleased.connect(self.seek_music)
        self.cur_play_list.current_music_change.connect(self.on_cur_play_list_change)

        # musics
        self.music_list_search.textChanged.connect(self.on_search)
        self.musics.doubleClicked.connect(self.on_tb_double_clicked)
        self.musics.customContextMenuRequested.connect(self.on_musics_right_click)

        # 全屏播放页面
        self.btn_return.clicked.connect(lambda: self.main_stacked_widget.setCurrentWidget(self.main_page))

        # 本地音乐页面
        self.le_search_local_music.textChanged.connect(self.on_search)
        self.btn_choose_dir.clicked.connect(self.show_choose_music_dir_page)
        self.tb_local_music.doubleClicked.connect(self.on_tb_double_clicked)
        self.tb_local_music.customContextMenuRequested.connect(self.on_tb_local_music_right_click)  # 右键菜单

        # 播放列表页面
        self.play_list_page.pushButton_2.clicked.connect(self.on_clear_clicked)

    # 当点击了播放列表页的清空按钮
    def on_clear_clicked(self):
        self.cur_play_list.clear()
        self.play_list_page.show_data(self.cur_play_list)
        self.music_info_widget.hide()
        self.stop_current()
        self.label_play_count.setText("0")
        self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/播放.png)}" +
                                     "QPushButton:hover{border-image:url(./resource/image/播放2.png)}")

    def init_shortcut(self):
        pause_play_act = QAction(self)
        pause_play_act.setShortcut(Qt.Key_Space)
        self.addAction(pause_play_act)
        pause_play_act.triggered.connect(self.play_pause)

    def eventFilter(self, object: QObject, event: QEvent):
        if event.type() == QEvent.MouseButtonPress:
            if not self.play_list_page.isHidden():
                self.play_list_page.hide()
        # 1. 如果主窗口被激活, 关闭子窗口
        if event.type() == QEvent.WindowActivate:
            if not self.play_list_page.isHidden():
                self.play_list_page.hide()
            if not self.add_music_list_dialog.isHidden():
                self.add_music_list_dialog.hide()

        # 2. 如果左下缩放按钮被鼠标左键拖动, 则缩放窗口
        if object == self.btn_zoom and event.type() == QEvent.MouseMove and event.buttons() == Qt.LeftButton:
            global_x = event.globalX()
            global_y = event.globalY()
            window_global_x = self.x()
            window_global_y = self.y()
            width = global_x - window_global_x
            heigth = global_y - window_global_y
            self.setGeometry(window_global_x, window_global_y, width, heigth)
        if object == self.header and type(event) == QMouseEvent and event.buttons() == Qt.LeftButton:
            # 如果标题栏被双击
            if event.type() == QEvent.MouseButtonDblClick:
                self.show_maximized_normal()
            # 记录拖动标题栏的位置
            elif event.type() == QEvent.MouseButtonPress:
                self.point = event.globalPos() - self.frameGeometry().topLeft()
            # 如果标题栏被拖动
            elif event.type() == QEvent.MouseMove:
                # print(self.frameGeometry().y())
                # if self.frameGeometry().y() <= 0:
                #     self.show_maximized_normal()
                if self.windowState() == Qt.WindowNoState:
                    self.move(event.globalPos() - self.point)
        # 3. 当鼠标移动到music_image时显示遮罩层
        if object == self.btn_music_image:
            if event.type() == QEvent.Enter:
                self.music_image_label.setGeometry(self.btn_music_image.geometry())
                self.music_image_label.show()
        if object == self.music_image_label:
            if event.type() == QEvent.Leave:
                self.music_image_label.hide()
            if event.type() == QEvent.MouseButtonPress:
                self.change_to_play_page()
        # 4.
        if object == self.label_lyric:
            if event.type() == QEvent.Wheel:
                self.is_wheeling = True
            else:
                self.is_wheeling = False
            # print("eventfilter: " + str(self.is_wheeling))
        return super().eventFilter(object, event)

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

        # api = NeteaseCloudMusicApi()
        # lyric = api.match_lyric(self.cur_play_list.get_current_music())
        # self.label_lyric.setText(lyric)
        # min = self.scrollArea.verticalScrollBar().minimum()
        # max = self.scrollArea.verticalScrollBar().maximum()
        # print(min)
        # print(max)

        # print(self.scrollArea.verticalScrollBar().value())
        # self.scrollArea.verticalScrollBar().setValue(560)
        # print("scrollArea.height: " + str(self.scrollArea.height()))
        # print("scrollArea.maximum: " + str(self.scrollArea.verticalScrollBar().maximum()))
        # self.scrollArea.verticalScrollBar().setSliderPosition(585)
        # print(self.scrollArea.verticalScrollBar().sliderPosition())
        # print("value: " + str(self.scrollArea.verticalScrollBar().value()))
        pass

    def paintEvent(self, event: QPaintEvent):
        self.btn_zoom.setGeometry(self.width() - 18, self.height() - 18, 14, 14)
        self.set_tb_local_music_layout()
        if self.cur_music_list is not None:
            self.set_musics_layout()

    def init_ui(self):
        self.setWindowIconText("qaq")
        self.setWindowIcon(QIcon("./resource/image/app-icon.png"))
        # font = QFont("Consolas", 10, 50)
        # self.musics.setFont(font)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.main_stacked_widget.setCurrentWidget(self.main_page)
        self.stackedWidget_2.setCurrentWidget(self.music_list_detail)
        # ------------------ header------------------ #
        qss_header = open("./resource/qss/header.qss", "r", encoding="utf-8")
        self.header.setStyleSheet(qss_header.read())
        qss_header.close()

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
        # self.music_list_date.setText("%s创建" % self.cur_music_list.get_creatd())
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
        self.navigation.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.navigation.setStyleSheet(
            "QListWidget{outline:0px; color:#5c5c5c; background:#f5f5f7;border-top:none;border-left:none;font-size:13px;"
            "border-right:1px solid #e1e1e2;border-bottom:1px solid #e1e1e2}"
            "QListWidget::Item{height:32px;border:0px solid gray;padding-left:19px;font-size:13px;}"
            "QListWidget::Item:hover{color:#000000;background:transparent;border:0px solid gray;}"
            "QListWidget::Item:selected{background:#e6e7ea;color:#000000;border-left: 3px solid #c62f2f;}")
        self.navigation.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa; width: 8px;}"
                                                          "QScrollBar::handle{background:#e1e1e2;border-radius:4px;}"
                                                          "QScrollBar::handle:hover{background:#cfcfd1;}"
                                                          "QScrollBar::sub-line{background:transparent;}"
                                                          "QScrollBar::add-line{background:transparent;}"
                                                          "QScrollBar::add-page{background:#f5f5f7;}"
                                                          "QScrollBar::sub-page{background:#f5f5f7;}")
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
        self.music_info_widget.setStyleSheet(
            "QWidget#music_info_widget{background-color:#f5f5f7;border:none;border-right:1px solid #e1e1e2;}")
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
        qss_foot = open("./resource/qss/footer.qss", "r", encoding="utf-8")
        self.footer.setStyleSheet(qss_foot.read())
        qss_foot.close()

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
        s = "<p>111阿斯蒂芬</p><br/><p>222发个好豆腐干</p><br/><p>333地方活佛济公</p><br/><p>444打成供东方红</p><br/><p>555宽高画更健康换个</p><br/>" \
            # "<p>666地方规划局和</p><br/><p>777飞规划局规划局</p><br/><p>88积分换个房管局8</p><br/><p>9</p><br/><p>10</p><br/><p>11</p><br/>" \
        # "<p>12</p><p>13</p><p>14</p><p>15</p>" \
        # "<p>16</p><p>17</p><p>18</p>" \
        # "<p>19</p><p>20</p><p>21</p><p>22</p><p>23</p><p>24</p><p>25</p><p style='color:white'>26</p><p>27</p>" \
        # "<p>28</p><p>29</p><p>30</p><p>31</p><p>32</p><p>33</p><p>34</p><p>35</p><p>36</p><p>37</p><p>&nbsp;</p><p>38</p><p>&nbsp;</p><p>壊すわ</p>"\
        # "<p>666地方规划局和</p><br/><p>777飞规划局规划局</p><br/><p>88积分换个房管局8</p><br/><p>9</p><br/><p>10</p><br/><p>11</p><br/>" \
        # "<p>12</p><p>13</p><p>14</p><p>15</p>" \
        # "<p>16</p><p>17</p><p>18</p>" \
        # "<p>19</p><p>20</p><p>21</p><p>22</p><p>23</p><p>24</p><p>25</p><p style='color:white'>26</p><p>27</p>" \
        # "<p>28</p><p>29</p><p>30</p><p>31</p><p>32</p><p>33</p><p>34</p><p>35</p><p>36</p><p>37</p><p>&nbsp;</p><p>38</p><p>&nbsp;</p><p>壊すわ</p>"\
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>" \
        # "<p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p><p>asdfghjkl</p><p>asdgdsg</p><p>asdgsdgsdg</p>"
        # min 总是0
        min = self.scrollArea.verticalScrollBar().minimum()
        _max = self.scrollArea.verticalScrollBar().maximum()
        print(min)
        print(self.scrollArea.verticalScrollBar().maximum())
        self.label_lyric.setText(s)

        # 右下播放列表页面
        self.play_list_page = PlayListPage(self)
        # 本地音乐页面
        self.widget.setStyleSheet("QWidget#widget{background-color:#fafafa;border:none;}")
        self.btn_choose_dir.setFlat(True)
        self.btn_choose_dir.setStyleSheet("QPushButton#btn_choose_dir{background:none;color:#0a63a8;border:none;}")
        self.btn_choose_dir.setCursor(Qt.PointingHandCursor)
        # 搜索框
        self.le_search_local_music.setStyleSheet(
            "QLineEdit#le_search_local_music{border:none;border-radius:10px;padding:2px 4px; background-color:#ffffff;" +
            "color:#000000;selection-color:yellow;selection-background-color: blue;}")
        self.le_search_local_music.setPlaceholderText("搜索本地音乐")
        self.search_act_2 = QAction(self)
        self.search_act_2.setIcon(QIcon("./resource/image/搜索3.png"))
        self.le_search_local_music.addAction(self.search_act_2, QLineEdit.TrailingPosition)
        self.init_button()

    def init_menu(self):
        # 1. 导航栏右键菜单
        self.nav_menu = QMenu()

        # 2. 在音乐列表上右键的菜单
        self.musics_menu = QMenu()

        # 3. 鼠标移到收藏到歌单时的二级菜单
        self.collect_menu = QMenu()

        # 4. 本地音乐右键菜单
        self.lm_menu = QMenu()

        qss = "QMenu{background-color:#fafafc;border:1px solid #c8c8c8;font-size:13px;width:214px;}" \
              "QMenu::item {height:36px;padding-left:44px;padding-right:60px;}" \
              "QMenu::item:selected {background-color:#ededef;}" \
              "QMenu::separator{background-color:#ededef;height:1px}"
        self.nav_menu.setStyleSheet(qss)
        self.musics_menu.setStyleSheet(qss)
        self.collect_menu.setStyleSheet(qss)
        self.lm_menu.setStyleSheet(qss)

    def show_play_list(self):
        if self.play_list_page.isHidden():
            self.play_list_page.show()
            self.play_list_page.show_data(self.cur_play_list)
        else:
            self.play_list_page.hide()

    def show_add_music_list_page(self):
        self.add_music_list_dialog.lineEdit.clear()
        self.add_music_list_dialog.setGeometry(QCursor.pos().x() + 30, QCursor.pos().y(), 270, 200)
        self.add_music_list_dialog.show()
        self.add_music_list_dialog.lineEdit.setFocus()

    def confirm_to_add_music_list(self):
        """ 新增歌单 """
        text = self.add_music_list_dialog.lineEdit.text()
        if len(text.strip()) > 0:
            ml = MusicList()
            ml.set_name(text)
            self.music_list_service.insert(ml)
            self.navigation.clear()
            self.init_data()
            self.add_music_list_dialog.hide()

    def cancel_to_add_music_list(self):
        self.add_music_list_dialog.hide()

    # 显示nav右键菜单
    def on_nav_right_click(self, pos):
        item = self.navigation.itemAt(pos)
        data = item.data(Qt.UserRole)
        if type(data) == MusicList and data.get_id() != 0 and data.get_name() != "本地音乐":
            self.nav_menu.clear()
            act1 = self.create_widget_action("./resource/image/nav-播放.png", "播放(Enter)")
            act2 = self.create_widget_action("./resource/image/导出.png", "导出歌单")
            act3 = self.create_widget_action("./resource/image/编辑.png", "编辑歌单信息(E)")
            act4 = self.create_widget_action("./resource/image/删除.png", "删除歌单(Delete)")
            act4.triggered.connect(lambda: self.del_music_list(data))

            self.nav_menu.addAction(act1)
            self.nav_menu.addAction(act2)
            self.nav_menu.addSeparator()
            self.nav_menu.addAction(act3)
            self.nav_menu.addAction(act4)
            self.nav_menu.exec(QCursor.pos())

    def create_widget_action(self, icon, text, data=None):
        act = QWidgetAction(self)
        act.setText(text)
        if data is not None:
            act.setData(data)
        widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(13, -1, -1, 11)
        layout.setSpacing(13)
        lb_icon = QLabel(widget)
        lb_icon.resize(18, 18)
        lb_text = QLabel(text, widget)
        if icon != "":
            lb_icon.setPixmap(QPixmap(icon))
        widget.setStyleSheet("QWidget:hover{background:#ededef}")
        layout.addWidget(lb_icon)
        layout.addWidget(lb_text)
        layout.addStretch()
        widget.setLayout(layout)
        act.setDefaultWidget(widget)
        return act

    def on_musics_right_click(self, pos):
        self.musics_menu.clear()
        act1 = self.create_widget_action("./resource/image/nav-播放.png", "播放(Enter)")
        act2 = self.create_widget_action("./resource/image/nav-下一首播放.png", "下一首播放(Enter)")
        act3 = QAction("收藏到歌单(Ctrl+S)", self)
        act4 = self.create_widget_action("./resource/image/打开文件.png", "打开文件所在目录")
        act5 = self.create_widget_action("./resource/image/删除.png", "从歌单中删除(Delete)")

        self.musics_menu.addAction(act1)
        self.musics_menu.addAction(act2)
        self.musics_menu.addAction(act3)
        # 获取被选中的行, 包括列
        items = self.musics.selectedItems()
        # 去重, 获取被选中的行号
        rows = set()
        for item in items:
            rows.add(item.row())
        # 被选中的音乐
        musics = []
        for row in rows:
            music = self.cur_music_list.get(row)
            musics.append(music)

        # 设置子菜单归属于act3
        self.create_collect_menu(musics)
        act3.setMenu(self.collect_menu)
        self.musics_menu.addMenu(self.collect_menu)
        # 只选中了一行
        if len(rows) == 1:
            self.musics_menu.addSeparator()
            self.musics_menu.addAction(act4)
        else:
            self.musics_menu.addSeparator()
        self.musics_menu.addAction(act5)
        act1.triggered.connect(lambda: self.on_act_play(musics))
        act2.triggered.connect(lambda: self.on_act_next_play(musics))
        act4.triggered.connect(lambda: self.on_act_open_file(musics))
        act5.triggered.connect(lambda: self.on_act_del(musics))
        self.musics_menu.exec(QCursor.pos())

    # 选中歌单列表的音乐, 点击 "播放"
    def on_act_play(self, musics: list):
        # 1. 若选中的音乐已在播放列表中, 则移除已存在的, 然后重新加入
        # 2. 选中的音乐依次在current index后加入播放列表
        # 3. 播放第一个选中的音乐
        for music in musics:
            self.cur_play_list.remove(music)
        cur_index = self.cur_play_list.get_current_index()
        for music in musics:
            cur_index += 1
            self.cur_play_list.insert_music(cur_index, music)

        self.label_play_count.setText(str(self.cur_play_list.size()))
        self.cur_play_list.set_current_index(self.cur_play_list.get_current_index() + 1)
        self.stop_current()
        if not os.path.exists(self.cur_play_list.get_current_music().get_path()):
            self.next_music()
            return
        self.play()
        self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/暂停.png)}" +
                                     "QPushButton:hover{border-image:url(./resource/image/暂停2.png)}")
        if self.is_mute:
            self.process.write(b"mute 1\n")
        self.state = self.playing_state
        self.show_music_info()

    # 选中歌单列表的音乐, 点击 "下一首播放"
    def on_act_next_play(self, musics: list):
        # 1. 若选中的音乐已在播放列表中, 则移除已存在的, 然后重新加入
        # 2. 选中的音乐依次在current index后加入播放列表
        for music in musics:
            self.cur_play_list.remove(music)
        cur_index = self.cur_play_list.get_current_index()
        for music in musics:
            cur_index += 1
            self.cur_play_list.insert_music(cur_index, music)

        self.label_play_count.setText(str(self.cur_play_list.size()))

    def create_collect_menu(self, musics: list):
        self.collect_menu.clear()
        act0 = self.create_widget_action("./resource/image/添加歌单.png", "创建新歌单")
        self.collect_menu.addAction(act0)
        self.collect_menu.addSeparator()
        all_music_list = self.music_list_service.get_all_music_list()
        for music_list in all_music_list:
            act = self.create_widget_action("./resource/image/歌单.png", music_list.get_name(), music_list)
            self.collect_menu.addAction(act)
            act.triggered.connect(lambda: self.on_acts_choose(musics))

    def on_acts_choose(self, musics: list):
        # 1. 在目标歌单的末尾加入; 2. 已存在的音乐则不加入(根据path判断)
        sender = self.sender()
        # data 是被选择的歌单, 但是该歌单不包含所属音乐
        data = sender.data()
        target_music_list = self.music_list_service.get_music_list_by_id_include_music(data.get_id())
        is_all_in = True
        need_insert_musics = []
        for music in musics:
            if not self.music_list_service.contains(music.get_path(), target_music_list):
                is_all_in = False
                music.set_mlid(target_music_list.get_id())
                need_insert_musics.append(music)
        self.music_service.batch_insert(need_insert_musics)
        if not is_all_in:
            Toast.show_(self, "已收藏到歌单", True, 2000)
        else:
            Toast.show_(self, "歌曲已存在!", False, 2000)

    # 选中歌单列表的音乐, 点击 "打开文件所在目录"
    def on_act_open_file(self, musics: list):
        if len(musics) == 1:
            music = musics[0]
            command = "explorer /select, \"%s\"" % music.get_path().replace("/", "\\")
            os.system(command)

    # 选中歌单列表的音乐, 点击 "从歌单中删除"
    def on_act_del(self, musics: list):
        self.music_service.batch_delete(musics)
        self.update_music_list()
        self.show_musics_data()
        # 清除已选择的项
        self.musics.clearSelection()

    def on_act_del_from_disk(self, musics: list):
        """ 从硬盘上删除本地音乐 """
        # 1.从歌单删除(本地音乐)
        # 2.从播放列表中删除(如果有的话)
        # 3.从硬盘删除
        self.music_service.batch_delete(musics)
        for music in musics:
            os.remove(music.get_path())
            self.cur_play_list.remove(music)
        self.update_music_list()
        self.label_play_count.setText(str(self.cur_play_list.size()))
        self.show_local_music_page_data()
        # 清除已选择的项
        self.tb_local_music.clearSelection()

    # 本地音乐页面表格被右击
    def on_tb_local_music_right_click(self, pos):
        self.lm_menu.clear()
        act1 = self.create_widget_action("./resource/image/nav-播放.png", "播放(Enter)")
        act2 = self.create_widget_action("./resource/image/nav-下一首播放.png", "下一首播放(Enter)")
        act3 = QAction("收藏到歌单(Ctrl+S)", self)
        act4 = self.create_widget_action("./resource/image/打开文件.png", "打开文件所在目录")
        act5 = self.create_widget_action("./resource/image/删除.png", "从本地磁盘删除")

        self.lm_menu.addAction(act1)
        self.lm_menu.addAction(act2)
        self.lm_menu.addAction(act3)

        # 获取被选中的行, 包括列
        items = self.tb_local_music.selectedItems()
        # 被选中的行号
        rows = set()
        for item in items:
            rows.add(item.row())
        musics = []
        for row in rows:
            music = self.cur_music_list.get(row)
            musics.append(music)
        # 设置子菜单归属于act3
        self.create_collect_menu(musics)
        act3.setMenu(self.collect_menu)
        self.lm_menu.addMenu(self.collect_menu)

        # 只选中了一行
        if len(rows) == 1:
            self.lm_menu.addSeparator()
            self.lm_menu.addAction(act4)
        else:
            self.lm_menu.addSeparator()
        self.lm_menu.addAction(act5)
        act1.triggered.connect(lambda: self.on_act_play(musics))
        act2.triggered.connect(lambda: self.on_act_next_play(musics))
        act4.triggered.connect(lambda: self.on_act_open_file(musics))
        act5.triggered.connect(lambda: self.on_act_del_from_disk(musics))
        self.lm_menu.exec(QCursor.pos())

    def del_music_list(self, music_list: MusicList):
        """ 删除歌单 """
        self.music_list_service.logic_delete(music_list.get_id())
        self.navigation.clear()
        self.init_data()

    def on_search(self, text: str):
        text = text.strip()
        if len(text) != 0:
            self.cur_music_list = self.cur_whole_music_list.search(text)
        else:
            self.cur_music_list = self.cur_whole_music_list.copy()
        # 显示当前页面显示两个不同的表格
        if self.stackedWidget_2.currentWidget() == self.music_list_detail:
            self.show_musics_data()
        elif self.stackedWidget_2.currentWidget() == self.local_music_page:
            self.show_local_music_page_data()

    def on_cur_play_list_change(self, music):
        if self.stackedWidget_2.currentWidget() == self.music_list_detail:
            self.show_musics_data()
        elif self.stackedWidget_2.currentWidget() == self.local_music_page:
            self.show_local_music_page_data()
        # 同步更新播放列表页的数据
        if self.cur_play_list is not None:
            self.play_list_page.show_data(self.cur_play_list)

    def show_choose_music_dir_page(self):
        self.choose_music_dir_page = ChooseMusicDirPage(self)
        self.choose_music_dir_page.local_musics_change.connect(self.reload_local_musics)
        self.choose_music_dir_page.exec()

    # 当改变了本地音乐的搜索路径, 重新读取本地音乐文件
    def reload_local_musics(self):
        self.cur_music_list = self.music_list_service.get_local_music()
        self.cur_whole_music_list = self.music_list_service.get_local_music()
        self.show_local_music_page_data()

    def play_pause(self):
        if self.cur_play_list is not None and self.cur_play_list.size() > 0:
            if self.state == self.playing_state:
                self.process.write(b"pause\n")
                self.btn_start.setStyleSheet("QPushButton{border-image:url(./resource/image/播放.png)}" +
                                             "QPushButton:hover{border-image:url(./resource/image/播放2.png)}")
                self.state = self.paused_state
                self.set_icon_item()
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
                self.set_icon_item()

    # 设置音量
    def set_volume(self, value: int):
        if self.process is not None:
            self.process.write(b"volume %d 50\n" % value)
            self.volume = value
        else:
            self.volume = value

    def get_elided_text(self, font: QFont, _str: str, max_width: int):
        fm = QFontMetrics(font)
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
                self.lrc_scroll(lrc, time)
                if self.duration != -1:
                    slider_position = int(float(p) / self.duration * 100)
                    if not self.slider_progress.isSliderDown():
                        self.slider_progress.setValue(slider_position)
            # 一曲放完
            if output.find("Exiting... (End of file)") != -1:
                print("当前歌曲播放完毕, 即将播放下一曲")
                self.info_reset()
                self.stop_current()
                self.cur_play_list.next()
                self.music_list_service.play_count_incr(self.cur_music_list.get_id())
                self.update_music_list()
                self.music_list_play_count.setText(
                    "<p>播放数</p><p style='text-align: right'>%d</p>" % self.cur_music_list.get_play_count())
                self.show_music_info()
                self.play()
                if self.is_mute:
                    self.process.write(b"mute 1\n")

    def lrc_scroll(self, lrc, time):
        # print(self.scrollArea.height())
        # print(self.scrollArea.verticalScrollBar().maximum())
        # pos = (line - 15) * 31 + 489/2
        # ret = lrc.show(time)
        # cur_line = ret[0]
        # print("%d %d" % (ret[0], ret[1]))
        # pos = (ret[0] - 15) * 31 + self.scrollArea.height() / 2
        # pos = ret[1] * 34 + (ret[0] - 15 - ret[1]) * 31 + self.scrollArea.height() / 2
        # print(str(ret[1]) + " " + str(pos))
        # print(self.is_wheeling)
        # if not self.is_wheeling:
        #     self.scrollArea.verticalScrollBar().setSliderPosition(pos)
        # self.label_lyric.setText(ret[2])
        # self.label_lyric.ver
        self.scrollArea.verticalScrollBar().setValue(self.min)
        self.min += 1
        print(self.scrollArea.verticalScrollBar().maximum())
        pass

    def error_output(self):
        while self.process.canReadLine():
            output = str(self.process.readLine())
            print("!" * 10 + " \nHere is the error output")
            print(output)
            print("!" * 10 + "error output end")

    def previous_music(self):
        if self.cur_play_list is not None and self.cur_play_list.size() > 0:
            self.info_reset()
            self.stop_current()
            self.cur_play_list.previous()
            # 若上一首歌曲已不存在, 则尝试播放上上一首
            if not os.path.exists(self.cur_play_list.get_current_music().get_path()):
                Toast.show_(self, "该歌曲已不存在(%s)" % self.cur_play_list.get_current_music().get_path(), False, 3000)
                print(self.cur_play_list.get_current_music().get_path() + "\t不存在")
                self.previous_music()
                return
            self.show_music_info()
            if self.state == self.playing_state:
                self.play()
                if self.is_mute:
                    self.process.write(b"mute 1\n")

    def next_music(self):
        if self.cur_play_list is not None and self.cur_play_list.size() > 0:
            self.info_reset()
            self.stop_current()
            self.cur_play_list.next()
            # 若下一首歌曲已不存在, 则尝试播放下下一首
            if not os.path.exists(self.cur_play_list.get_current_music().get_path()):
                Toast.show_(self, "该歌曲已不存在(%s)" % self.cur_play_list.get_current_music().get_path(), False, 3000)
                print(self.cur_play_list.get_current_music().get_path() + "\t不存在")
                self.next_music()
                return
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

    def update_music_list(self, _mlid=None):
        """ 当歌单内音乐增加或被删除后, 需要更新相关变量 """
        if _mlid is not None:
            self.cur_music_list = self.music_list_service.get_music_list_by_id_include_music(_mlid)
            self.cur_whole_music_list = self.music_list_service.get_music_list_by_id_include_music(_mlid)
        else:
            self.cur_music_list = self.music_list_service.get_music_list_by_id_include_music(
                self.cur_music_list.get_id())
            self.cur_whole_music_list = self.music_list_service.get_music_list_by_id_include_music(
                self.cur_music_list.get_id())

    def closeEvent(self, event: QCloseEvent):
        self.stop_current()


def main():
    # init_install()
    CheckProgram.check_program()
    app = QtWidgets.QApplication(sys.argv)
    # qss = open("./resource/qss/main.qss", "r", encoding="utf-8")
    # read = qss.read()
    # app.setStyleSheet(read)
    my_window = MainWindow()
    my_window.show()
    sys.exit(app.exec_())


# 1184
if __name__ == "__main__":
    main()
    # init_install()
