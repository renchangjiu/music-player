from src.dao.music_dao import MusicDao
from src.entity.music import Music


class MusicService:
    def __init__(self):
        super.__init__()
        self.music_dao = MusicDao()

    def get_musics_by_mlid(self, music_list_id: int) -> tuple:
        """
        查询该歌单所属的所有歌曲
        :param music_list_id: int
        """
        musics = self.music_dao.select_by_mlid(music_list_id)
        return tuple(musics)

    def get_music_by_id(self, _id: int) -> Music:
        """根据ID获取歌曲"""
        return self.music_dao.select_by_id(_id)