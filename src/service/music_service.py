import os
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
        m.mid = mid
        m.path = path
        m.size = util.format_size(os.path.getsize(path))
        m.title = mp3.title
        m.artist = mp3.artist
        m.album = mp3.album
        m.duration = mp3.duration
        return m

    def list_(self, m: Music) -> tuple:
        return tuple(self.music_dao.list_(m))

    def list_by_mid(self, mid: int) -> tuple:
        """
        查询该歌单所属的所有歌曲
        :param mid: 歌单id
        """
        musics = self.music_dao.list_by_mid(mid)
        return tuple(musics)

    def get_by_id(self, _id: int) -> Music:
        """根据ID获取歌曲"""
        return self.music_dao.select_by_id(_id)

    def contains(self, mid: str, path: str) -> bool:
        """根据歌单ID和path判断该歌单内是否已经有相同的歌曲"""
        music = Music()
        music.mid = mid
        music.path = path
        musics = self.music_dao.list_(music)
        return len(musics) != 0

    def insert(self, music_: Music):
        self.music_dao.insert(music_)

    def batch_insert(self, musics: list):
        """ 重复数据不会被插入(重复指 path 及 mid 相同) """
        total_list = self.list_(Music())
        data = []
        for music in musics:
            flag = True
            for m in total_list:
                if music.path == m.path and music.mid == m.mid:
                    flag = False
                    break
            if flag:
                data.append(music)
        self.music_dao.batch_insert(data)

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
        self.music_dao.delete_by_mid(mid)

    def index_of(self, id_: int, mid: int) -> int:
        """ 判断某歌曲是否属于某歌单, 是则返回该歌曲在该歌单中的索引, 否则返回-1 """
        music = self.get_by_id(id_)
        if music.mid != mid:
            return -1
        musics = self.list_by_mid(mid)
        for i in range(len(musics)):
            m = musics[i]
            if m.id == music.id:
                return i
        return -1


if __name__ == "__main__":
    pass
