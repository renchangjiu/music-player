import json, os
from datetime import datetime

from src.service import global_variable as glo_var
from src.service.MP3Parser import MP3
from src.entity.music import Music
from src.service.play_list import PlayList


class MusicList:
    """歌单"""

    def __init__(self):
        # 歌单id
        self.__id = -1
        # 歌单名
        self.__name = ""
        # 创建日期(字符串, 形如: "2018-12-12")
        self.__created = ""
        # 播放次数
        self.__play_count = 0
        # 所属歌单音乐
        self.__musics = []

    def get_id(self):
        return self.__id

    def set_id(self, _id):
        self.__id = _id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def size(self):
        return len(self.__musics)

    def add(self, music):
        self.__musics.append(music)

    def get_play_count(self):
        return self.__play_count

    def set_play_count(self, count):
        self.__play_count = count

    def get_created(self):
        return self.__created

    def set_created(self, date_str):
        self.__created = date_str

    def get(self, index):
        return self.__musics[index]

    def remove(self, music):
        """ 通过文件路径删除music"""
        for m in self.__musics:
            if m.get_path() == music.get_path():
                # print(music)
                self.__musics.remove(m)
                return True
        return False

    def contains(self, path):
        for music in self.__musics:
            if music.get_path() == path:
                return True
        return False

    def index_of(self, music):
        for i in range(self.size()):
            m = self.get(i)
            if m.get_path() == music.get_path():
                return i
        return -1

    def __str__(self):
        ret = "MusicList [\n\tid: %s\n\tname: %s,\n\tplay_count: %d\n\tcreted: %s\n\tsize: %d" % (
            self.__id, self.__name, self.__play_count, self.__created, self.size())
        ret += "\n\tmusic:[\n"
        for music in self.__musics:
            ret += music.__str__()
        ret += "\t]\n]"
        return ret

    # music_list to play_list
    @staticmethod
    def to_play_list(ml):
        play_list = PlayList()
        for i in range(ml.size()):
            music = ml.get(i)
            play_list.add_music(music)
        return play_list

    @staticmethod
    def to_disk(ml, path=""):
        """ 将MusicList中的音乐信息转成json(不包括image), 存入硬盘"""
        if ml.get_name() is None or ml.get_name() == "":
            return False
        ml = MusicList.__encode(ml)

        # 如果是创建歌单
        if ml.get_created() == "" or ml.get_created() is None:
            date = datetime.now().strftime("%F")
            ml.set_created(date)
        ret = "{"
        ret += '"name": "%s", "size": %d, "play_count": %d, "date": "%s", ' % (
            ml.get_name(), ml.size(), ml.get_play_count(), ml.get_created())
        ret += '"musics":['
        for i in range(ml.size()):
            music = ml.get(i)
            ret += '{"path": "%s", "file_name": "%s", "title": "%s", "artist": "%s", "album": "%s", "duration": %d, "size": "%s"},' % (
                music.get_path(), music.get_file_name(), music.get_title(), music.get_artist(), music.get_album(),
                music.get_duration(), music.get_size())
        if ml.size() > 0:
            ret = ret[0:-1]
        ret += "]}"

        if path == "":
            f = open(r"%s%s" % (glo_var.music_list_path, ml.get_name()), "w", encoding="utf-8")
        else:
            f = open(r"%s%s" % (path, ml.get_name()), "w", encoding="utf-8")
        f.write(ret)
        f.close()
        return True

    # 将特殊字符转义( " ->  &#34; \ -> &#92;)
    @staticmethod
    def __encode(ml):
        ml.set_name(ml.get_name().replace('"', "&#34;").replace('\\', "&#92;"))
        for i in range(ml.size()):
            m = ml.get(i)
            m.set_path(m.get_path().replace('"', "&#34;").replace('\\', "&#92;"))
            m.set_title(m.get_title().replace('"', "&#34;").replace('\\', "&#92;"))
            m.set_artist(m.get_artist().replace('"', "&#34;").replace('\\', "&#92;"))
            m.set_album(m.get_album().replace('"', "&#34;").replace('\\', "&#92;"))
        return ml


    @staticmethod
    def from_disk(path):
        # 从磁盘文件中读取MusicList
        f = open(path, "r", encoding="utf-8")
        json_str = json.loads(f.read(), encoding="utf-8")
        music_list = MusicList()
        music_list.set_name(json_str["name"].replace('&#34;', '"'))
        music_list.set_play_count(json_str["play_count"])
        music_list.set_created(json_str["date"])
        m_list = json_str["musics"]
        for i in range(len(m_list)):
            m = Music()
            ms = m_list[i]
            m.set_path(str(ms["path"]).replace('&#34;', '"').replace('&#92;', "\\"))
            m.set_title(str(ms["title"]).replace('&#34;', '"').replace('&#92;', "\\"))
            m.set_artist(str(ms["artist"]).replace('&#34;', '"').replace('&#92;', "\\"))
            m.set_album(str(ms["album"]).replace('&#34;', '"').replace('&#92;', "\\"))
            m.set_duration(int(ms["duration"]))
            # 兼容旧版本歌单
            if "size" in ms:
                m.set_size(str(ms["size"]))
            m.set_from(music_list)
            music_list.add(m)
        return music_list

    @staticmethod
    def remove_from_disk(path):
        return os.remove(path)

    # 根据title, artist, album搜索, 返回符合条件的MusicList
    # 当删除ret后, 需对原MusicList做刷新
    def search(self, keyword):
        keyword = keyword.lower()
        ret = MusicList()
        ret.set_name(self.__name)
        ret.set_play_count(self.__play_count)
        for m in self.__musics:
            title = m.get_title().lower()
            artist = m.get_artist().lower()
            album = m.get_album().lower()
            if title.find(keyword) != -1 or artist.find(keyword) != -1 or album.find(keyword) != -1:
                ret.add(m)
        return ret

    # copy该歌单的全部内容到新歌单
    def copy(self):
        ret = MusicList()
        ret.set_name(self.__name)
        ret.set_play_count(self.__play_count)
        ret.set_created(self.__created)
        for m in self.__musics:
            ret.add(m)
        return ret


#######################################################################################################################

def test_4_to_disk():
    m1 = Music()
    m1.set_path("D:/13595/Music/ClariS - blossom.mp3")
    m1.set_title("blossom")
    m1.set_artist("ClariS")
    m1.set_album("unknown")
    m1.set_duration(231)

    music_list = MusicList()
    music_list.set_name("kjj")
    # music_list.add_music(m1)
    MusicList.to_disk(music_list)


def test_4_from_disk():
    # print(music_list)
    pass


def add_all_loacl_music():
    path = r"D:/13595/Music/"
    flies = os.listdir(path)
    music_list = MusicList()
    music_list.set_name("全部音乐_bak")
    music_list.set_play_count(100)
    for file in flies:
        if file.endswith("mp3") or file.endswith("MP3"):
            mp3 = MP3(path + file)
            music = Music()
            music.set_title(mp3.title)
            music.set_artist(mp3.artist)
            music.set_album(mp3.album)
            music.set_duration(mp3.duration)
            music.set_path(path + file)
            music.set_image(mp3.image)
            music_list.add(music)

            # print(mp3.title)
            # print(mp3.ret)
    MusicList.to_disk(music_list)


if __name__ == "__main__":
    pass
