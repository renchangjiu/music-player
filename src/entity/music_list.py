from src.entity.music import Music


class MusicList:
    """歌单"""

    def __init__(self):
        # 歌单id
        self.__id = -1
        # 歌单名
        self.__name = ""
        # 创建日期(秒级时间戳)
        self.__created = -1
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

    def is_empty(self) -> bool:
        return len(self.__musics) == 0

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

    def get_musics(self):
        return self.__musics

    def set_musics(self, musics):
        self.__musics = musics

    def get(self, index) -> Music:
        return self.__musics[index]

    def __str__(self):
        ret = "MusicList [\n\tid: %s\n\tname: %s,\n\tplay_count: %d\n\tcreted: %s\n\tsize: %d" % (
            self.__id, self.__name, self.__play_count, self.__created, self.size())
        ret += "\n\tmusic:[\n"
        for music in self.__musics:
            ret += music.__str__()
        ret += "\t]\n]"
        return ret

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


if __name__ == "__main__":
    pass
