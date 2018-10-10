import os
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, Qt, QThread, QUrl, QTimer

from music import Music


class PlayList(QObject):
    """播放列表
        根据path & from 来判断是否是来自同一歌单同一首音乐
    """

    # Music is current-music
    current_music_change = QtCore.pyqtSignal(Music)
    # current_index_change = QtCore.pyqtSignal
    test_sig = QtCore.pyqtSignal(str)

    # 单曲循环
    current_item_in_loop_mode = 1
    # 列表循环
    loop_mode = 2
    # 随机播放
    random_mode = 3
    # 顺序播放(列表播放完则停止)
    sequential_mode = 4

    def __init__(self):
        super().__init__()
        self.__musics = list()
        self.play_mode = 2
        self.__current_index = -1

    def set_play_mode(self, PlayList_mode):
        self.play_mode = PlayList_mode

    def get_play_mode(self):
        return self.play_mode

    def add_music(self, music):
        self.__musics.append(music)

    def insert_music(self, index, music):
        self.__musics.insert(index, music)

    def get_music_count(self):
        return len(self.__musics)

    def size(self):
        return len(self.__musics)

    def get_current_index(self):
        return self.__current_index

    def get(self, index):
        return self.__musics[index]

    def remove(self, music):
        index = self.index_of(music)
        # print("index ", index)
        if index != -1:
            self.__musics.pop(index)
            if index <= self.__current_index:
                self.__current_index -= 1

    def remove_2(self, index):
        self.__musics.pop(index)
        if index < self.__current_index:
            self.__current_index -= 1

    def contains(self, path):
        for music in self.__musics:
            if music.get_path() == path:
                return True
        return False

    def index_of(self, music):
        for i in range(self.size()):
            m = self.get(i)
            if self.is_same_music(m, music):
                return i
        return -1

    # 来自于同歌单且path相同的music将被判断为 相同的music
    def is_same_music(self, one=Music(), another=Music()):
        if type(one) == type(another):
            if one.get_path() == another.get_path() and one.get_from().get_name() == another.get_from().get_name():
                return True
        return False

    def set_current_index(self, index):
        if self.size() > 0:
            self.__current_index = index
            self.current_music_change.emit(self.get_current_music())

    def get_current_music(self):
        if self.size() > 0:
            return self.__musics[self.__current_index]

    def get_music(self, index):
        return self.__musics[index]

    def next(self):
        if self.get_play_mode() == self.loop_mode:
            # 如果索引是play_list 的最后一项, 则置索引为0
            if self.__current_index == self.get_music_count() - 1:
                self.__current_index = 0
            else:
                self.__current_index += 1
            self.current_music_change.emit(self.get_current_music())

    def previous(self):
        if self.get_play_mode() == self.loop_mode:
            # 如果索引是play_list 的第一项, 则置索引为length-1(即最后一项)
            if self.__current_index == 0:
                self.__current_index = self.get_music_count() - 1
            else:
                self.__current_index -= 1
            self.current_music_change.emit(self.get_current_music())

    def __str__(self):
        if len(self.__musics) != 0:
            ret = "PlayerList %d [" % self.get_music_count()
            for i in range(len(self.__musics)):
                ret += "\t"
                ret += self.__musics[i].get_path()
                ret += ",\t\t"
                ret += self.__musics[i].get_title()
                ret += "\n"
            ret += "]"
            return ret
        else:
            return "PlayerList[None]"
