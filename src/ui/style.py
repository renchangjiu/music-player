from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidget, QSlider, QWidget, QLabel, QPushButton
from src.common.app_attribute import AppAttribute


class Style(object):

    @staticmethod
    def init_header_style(header: QWidget, btn_icon: QPushButton, btn_window_close: QPushButton,
                          btn_window_max: QPushButton,
                          btn_window_min: QPushButton, btn_set: QPushButton):
        # ------------------ header------------------ #
        qss_path = AppAttribute.res_path + "/qss/header.qss"
        qss = open(qss_path, "r", encoding="utf-8")
        header.setStyleSheet(qss.read())
        qss.close()
        btn_icon.setCursor(Qt.PointingHandCursor)
        btn_window_close.setCursor(Qt.PointingHandCursor)
        btn_window_max.setCursor(Qt.PointingHandCursor)
        btn_window_min.setCursor(Qt.PointingHandCursor)
        btn_set.setCursor(Qt.PointingHandCursor)

    @staticmethod
    def init_nav_style(navigation: QListWidget):
        # ------------------ 左边导航栏 ------------------ #
        navigation.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        navigation.setStyleSheet(
            "QListWidget{"
            "outline:0px; color:#5c5c5c; background:#f5f5f7;border-top:none;border-left:none;font-size:13px;"
            "border-right:1px solid #e1e1e2;border-bottom:1px solid #e1e1e2}"
            "QListWidget::Item{height:32px;border:0px solid gray;padding-left:19px;font-size:13px;}"
            "QListWidget::Item:hover{color:#000000;background:transparent;border:0px solid gray;}"
            "QListWidget::Item:selected{background:#e6e7ea;color:#000000;border-left: 3px solid #c62f2f;}")
        navigation.verticalScrollBar().setStyleSheet("QScrollBar{background:#fafafa; width: 8px;}"
                                                     "QScrollBar::handle{background:#e1e1e2;border-radius:4px;}"
                                                     "QScrollBar::handle:hover{background:#cfcfd1;}"
                                                     "QScrollBar::sub-line{background:transparent;}"
                                                     "QScrollBar::add-line{background:transparent;}"
                                                     "QScrollBar::add-page{background:#f5f5f7;}"
                                                     "QScrollBar::sub-page{background:#f5f5f7;}")
        navigation.setCursor(Qt.PointingHandCursor)
        # 更改右键策略
        navigation.setContextMenuPolicy(Qt.CustomContextMenu)

    @staticmethod
    def init_footer_style(slider_volume: QSlider, footer: QWidget, volume: int, btn_zoom: QPushButton, width: int,
                          height: int):
        # ------------------ footer ------------------ #
        slider_volume.setValue(volume)
        slider_volume.setCursor(Qt.PointingHandCursor)
        qss = open("./resource/qss/footer.qss", "r", encoding="utf-8")
        footer.setStyleSheet(qss.read())
        qss.close()
        btn_zoom.setGeometry(width - 18, height - 18, 14, 14)
        btn_zoom.setStyleSheet("QPushButton{border-image:url(./resource/image/缩放.png)}")
        btn_zoom.setCursor(Qt.SizeFDiagCursor)

    @staticmethod
    def init_music_card_style(music_info_widget: QWidget, btn_music_image: QPushButton, music_image_label: QLabel):
        music_info_widget.setStyleSheet(
            "QWidget#music_info_widget{background-color:#f5f5f7;border:none;border-right:1px solid #e1e1e2;}")
        music_info_widget.setCursor(Qt.PointingHandCursor)
        btn_music_image.setIconSize(QSize(44, 44))
        btn_music_image.setAutoFillBackground(True)
        music_image_label.setStyleSheet("QLabel{background-color: rgba(71, 71, 71, 150)}")
        music_image_label.setPixmap(QPixmap("./resource/image/全屏.png"))
        music_image_label.hide()
