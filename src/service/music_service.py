from src.dao.music_dao import MusicDao
from src.entity.music import Music


class MusicService:
    def __init__(self) -> None:
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

    def has_same_music(self, music: Music) -> bool:
        """根据歌单ID和path判断 该歌单内是否已经有同一首歌曲"""
        musics = self.music_dao.select_by_selective(music)
        return len(musics) != 0


if __name__ == "__main__":
    service = MusicService()
    music = Music()
    music.set_mlid(10)
    music.set_path("/path/a.mp3")
    ret = service.has_same_music(music)
    print(ret)
