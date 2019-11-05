import time

from src.dao.music_dao import MusicDao
from src.dao.music_list_dao import MusicListDao
from src.entity.music import Music
from src.entity.music_list import MusicList
from src.service.play_list import PlayList


class MusicListService:
    def __init__(self) -> None:
        super().__init__()
        self.music_list_dao = MusicListDao()
        self.music_dao = MusicDao()

    @staticmethod
    def copy(source: MusicList) -> MusicList:
        """ 将源歌单的所有属性复制到一个新对象"""
        ret = MusicList()
        ret.name = source.name
        ret.play_count = source.play_count
        ret.created = source.created
        ret.musics = source.musics[0:len(source.musics)]
        return ret

    @staticmethod
    def search(music_list: MusicList, keyword: str) -> MusicList:
        """ 根据title, artist, album搜索, 返回搜索结果集 """
        keyword = keyword.lower()
        ret = MusicList()
        ret.name = music_list.name
        ret.play_count = music_list.play_count
        ret.musics = []
        for m in music_list.musics:
            title = m.title.lower()
            artist = m.artist.lower()
            album = m.album.lower()
            if title.find(keyword) != -1 or artist.find(keyword) != -1 or album.find(keyword) != -1:
                ret.musics.append(m)
        return ret

    def get_all_music_list(self) -> tuple:
        """获取所有歌单"""
        music_lists = self.music_list_dao.select_list()
        return tuple(music_lists)

    def get_local_music(self) -> MusicList:
        """获取本地音乐歌单, 同时查出该歌单下的所属音乐"""
        music_list = self.music_list_dao.select_by_id(MusicList.default_id)
        musics = self.music_dao.list_by_mid(music_list.id)
        music_list.musics = musics
        return music_list

    def get_music_list_by_id(self, _id: int) -> MusicList:
        """根据ID获取歌单信息"""
        return self.music_list_dao.select_by_id(_id)

    def get_by_id(self, id_: int) -> MusicList:
        """ 根据ID获取歌单信息, 同时获取该歌单的所属音乐 """
        music_list = self.music_list_dao.select_by_id(id_)
        musics = self.music_dao.list_by_mid(id_)
        music_list.musics = musics
        return music_list

    def logic_delete(self, _id: int):
        """逻辑删除该歌单"""
        self.music_list_dao.logic_delete(_id)

    def play_count_incr(self, _id: int):
        """ 使该歌单的播放数+1 """
        self.music_list_dao.play_count_incr(_id)

    def insert(self, name: str):
        """新增歌单, 只需要name属性"""
        ml = MusicList()
        ml.name = name
        ml.created = int(time.time())
        self.music_list_dao.insert(ml)

    def to_play_list(self, music_list: MusicList) -> PlayList:
        """ 把MusicList 转成 PlayList """
        play_list = PlayList()
        play_list.set_musics(music_list.musics)
        return play_list


if __name__ == "__main__":
    pass
