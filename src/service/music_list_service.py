import time

from src.dao.music_list_dao import MusicListDao
from src.entity.music_list import MusicList


class MusicListService:
    def __init__(self) -> None:
        super().__init__()
        self.music_list_dao = MusicListDao()

    def get_all_music_list(self) -> tuple:
        """获取所有歌单"""
        music_lists = self.music_list_dao.select_list()
        return tuple(music_lists)

    def get_music_list_by_id(self, _id: int) -> MusicList:
        """根据ID获取歌单"""
        return self.music_list_dao.select_by_id(_id)

    def logic_delete(self, _id):
        """逻辑删除该歌单"""
        self.music_list_dao.logic_delete(_id)

    def insert(self, music_list: MusicList):
        """新增歌单, 只需要name属性"""
        music_list.set_created(int(time.time()))
        self.music_list_dao.insert(music_list)


if __name__ == "__main__":
    service = MusicListService()
    # music_lists = service.get_all_music_list()
    # for music_list in music_lists:
    #     print(music_list)

    # print(service.get_music_list_by_id(1))

    # music_list = MusicList()
    # music_list.set_name("歌单55555")
    # service.insert(music_list)
