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

    def get_all_music_list(self) -> tuple:
        """获取所有歌单"""
        music_lists = self.music_list_dao.select_list()
        return tuple(music_lists)

    def get_local_music(self) -> MusicList:
        """获取本地音乐歌单, 同时查出该歌单下的所属音乐"""
        music_list = self.music_list_dao.select_local_music()
        musics = self.music_dao.select_by_mlid(music_list.get_id())
        music_list.set_musics(musics)
        return music_list

    def get_music_list_by_id(self, _id: int) -> MusicList:
        """根据ID获取歌单信息"""
        return self.music_list_dao.select_by_id(_id)

    def get_music_list_by_id_include_music(self, _id: int) -> MusicList:
        """根据ID获取歌单信息, 同时获取该歌单的所属音乐"""
        music_list = self.music_list_dao.select_by_id(_id)
        musics = self.music_dao.select_by_mlid(_id)
        music_list.set_musics(musics)
        return music_list

    def logic_delete(self, _id):
        """逻辑删除该歌单"""
        self.music_list_dao.logic_delete(_id)

    def insert(self, music_list: MusicList):
        """新增歌单, 只需要name属性"""
        music_list.set_created(int(time.time()))
        self.music_list_dao.insert(music_list)

    def to_play_list(self, music_list: MusicList) -> PlayList:
        """ 把MusicList 转成 PlayList """
        play_list = PlayList()
        play_list.set_musics(music_list.get_musics())
        return play_list

    def contains(self, path: str, music_list: MusicList) -> bool:
        """ 根据歌单ID和path判断 该歌单内是否已经有同一首歌曲"""
        # musics = self.music_dao.select_by_selective(music)
        # return self.index_of(music, music_list) != -1
        for i in range(music_list.size()):
            music = music_list.get(i)
            if path == music.get_path():
                return True
        return False
    # return len(musics) != 0

    def index_of(self, music: Music, music_list: MusicList):
        """ 判断某歌曲是否属于某歌单, 是则返回该歌曲在该歌单中的索引, 否则返回-1 """
        if music.get_mlid() != music_list.get_id():
            return -1
        for i in range(music_list.size()):
            m = music_list.get(i)
            if m.get_id() == music.get_id():
                return i
        return -1


if __name__ == "__main__":
    service = MusicListService()
    # music_lists = service.get_all_music_list()
    # for music_list in music_lists:
    #     print(music_list)

    # print(service.get_music_list_by_id(1))

    # music_list = MusicList()
    # music_list.set_name("歌单55555")
    # service.insert(music_list)
