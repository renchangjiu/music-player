import json, base64
import os

from MP3Parser import MP3
from music import Music
from play_list import PlayList


class MusicList:
    """歌单"""

    def __init__(self):
        # 歌单名
        self.__name = ""
        # 创建日期(字符串, 形如: "2018-12-12")
        self.__date = ""
        # 播放次数
        self.__play_count = 0
        # 歌单音乐
        self.__musics = []

    def get_name(self):
        return self.__name

    def size(self):
        return len(self.__musics)

    def set_name(self, name):
        self.__name = name

    def add(self, music):
        self.__musics.append(music)

    def get_play_count(self):
        return self.__play_count

    def set_play_count(self, count):
        self.__play_count = count

    def get_date(self):
        return self.__date

    def set_date(self, date_str):
        self.__date = date_str

    def get_by_name(self):
        pass

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
        ret = "MusicList name: %s, size: %d [" % (self.__name, self.size())
        for music in self.__musics:
            ret += music.__str__()
        ret += " ]"
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
    def to_disk(ml):
        """ 将MusicList中的音乐信息转成json(不包括image), 存入硬盘"""
        if ml.get_name() is None or ml.get_name() == "":
            return False
        ml = MusicList.__encode(ml)

        ret = "{"
        ret += '"name": "%s", "size": %d, "play_count": %d, "date": "%s", ' % (ml.get_name(), ml.size(), ml.get_play_count(), ml.get_date())
        ret += '"musics":['
        for i in range(ml.size()):
            music = ml.get(i)
            ret += '{"path": "%s", "file_name": "%s", "title": "%s", "artist": "%s", "album": "%s", "duration": %d},' % (
                music.get_path(), music.get_file_name(), music.get_title(), music.get_artist(), music.get_album(),
                music.get_duration())
        if ml.size() > 0:
            ret = ret[0:-1]
        ret += "]}"
        f = open(r"./resource/config/%s" % ml.get_name(), "w", encoding="utf-8")
        f.write(ret)
        f.close()
        return True

    # 将特殊字符转义( " ->  &#34;)
    @staticmethod
    def __encode(ml):
        ml.set_name(ml.get_name().replace('"', "&#34;"))
        for i in range(ml.size()):
            m = ml.get(i)
            m.set_path(m.get_path().replace('"', "&#34;"))
            m.set_title(m.get_title().replace('"', "&#34;"))
            m.set_artist(m.get_artist().replace('"', "&#34;"))
            m.set_album(m.get_album().replace('"', "&#34;"))
        return ml

    # 转义回来, 暂时无用
    @staticmethod
    def __decode(ml):
        ml.set_name(ml.get_name().replace('&#34;', '"'))
        for i in range(ml.size()):
            m = ml.get(i)
            m.set_path(m.get_path().replace('&#34;', '"'))
            m.set_title(m.get_title().replace('&#34;', '"'))
            m.set_artist(m.get_artist().replace('&#34;', '"'))
            m.set_album(m.get_album().replace('&#34;', '"'))
        return ml

    @staticmethod
    def from_disk(path):
        # 从磁盘文件中读取MusicList
        f = open(path, "r", encoding="utf-8")
        json_str = json.loads(f.read(), encoding="utf-8")

        music_list = MusicList()
        music_list.set_name(json_str["name"].replace('&#34;', '"'))
        music_list.set_play_count(json_str["play_count"])
        music_list.set_date(json_str["date"])
        m_list = json_str["musics"]
        for i in range(len(m_list)):
            m = Music()
            ms = m_list[i]
            m.set_path(str(ms["path"]).replace('&#34;', '"'))
            m.set_title(str(ms["title"]).replace('&#34;', '"'))
            m.set_artist(str(ms["artist"]).replace('&#34;', '"'))
            m.set_album(str(ms["album"]).replace('&#34;', '"'))
            m.set_duration(int(ms["duration"]))
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
    # music_list = MusicList.from_json("./resource/config/kjj.json")
    music_list = MusicList.from_disk("./resource/config/全部音乐")
    print(music_list)


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
    # test1()
    # test_4_to_json()
    # test_4_from_disk()
    # test_4_all()
    # add_all_loacl_music()
    # f = open("./resource/config/全部音乐", encoding="utf-8")
    # print(json.loads(f.read(), encoding="utf-8"))
    # f.close()
    # test_4_remove_from_disk()
    # test_4_remove()
    # test_4_contains()
    pass
