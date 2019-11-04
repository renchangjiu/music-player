import os
from src.common.app_attribute import AppAttribute
from src.dao.music_dao import MusicDao
from src.entity.music import Music
from src.service import util
from src.service.MP3Parser import MP3


class MusicService:
    def __init__(self) -> None:
        self.music_dao = MusicDao()

    @staticmethod
    def gen_music_by_path(path: str, mid: int):
        """
        根据path获得其时长及作者等信息, 生成 Music 对象
        :param path: 文件实际路径
        :param mid: 所属歌单ID
        :return: Music
        """
        m = Music()
        mp3 = MP3(path)
        m.set_mlid(mid)
        m.set_path(path)
        m.set_size(util.format_size(os.path.getsize(path)))
        m.set_title(mp3.title)
        m.set_artist(mp3.artist)
        m.set_album(mp3.album)
        m.set_duration(mp3.duration)
        return m

    def get_musics_by_mid(self, mid: int) -> tuple:
        """
        查询该歌单所属的所有歌曲
        :param mid: 歌单id
        """
        musics = self.music_dao.select_by_mlid(mid)
        return tuple(musics)

    def get_music_by_id(self, _id: int) -> Music:
        """根据ID获取歌曲"""
        return self.music_dao.select_by_id(_id)

    def has_same_music(self, music_: Music) -> bool:
        """根据歌单ID和path判断 该歌单内是否已经有同一首歌曲"""
        musics = self.music_dao.select_by_selective(music_)
        return len(musics) != 0

    def insert(self, music_: Music):
        self.music_dao.insert(music_)

    def batch_insert(self, musics: list):
        self.music_dao.batch_insert(musics)

    def delete(self, _id: int):
        """
        删除该歌曲, 即把该歌曲从所属歌单里删除, 硬盘里的文件不会被删除
        :param _id: 歌曲ID
        """
        self.music_dao.delete(_id)

    def batch_delete(self, ids: list):
        """
        根据ID列表批量删除歌曲, 即把该歌曲从所属歌单里删除, 硬盘里的文件不会被删除
        :param ids: 歌曲ID列表
        """
        self.music_dao.batch_delete(ids)

    def delete_by_mid(self, mid: int):
        """ 根据歌单ID删除 """
        self.music_dao.delete_by_mlid(mid)


if __name__ == "__main__":
    service = MusicService()
    music = Music()
    music.set_mlid(10)
    music.set_path("/path/a.mp3")
    ret = service.has_same_music(music)
    print(ret)
