import sqlite3

from src.entity.music import Music
from src.common.app_attribute import AppAttribute


class MusicDao:
    def __init__(self):
        self.database = AppAttribute.db_path + "/data.db"
        self.conn = sqlite3.connect(self.database)

    def select_by_mlid(self, music_list_id: int) -> list:
        """
        查询该歌单所属的所有歌曲
        :param music_list_id:
        :return:
        """
        sql = "select * from t_music where mlid = ?"
        musics = []
        cursor = self.conn.cursor()
        cursor.execute(sql, (music_list_id,))
        ret = cursor.fetchall()
        cursor.close()
        for row in ret:
            music = self.__row_2_music(row)
            musics.append(music)
        return musics

    def select_by_id(self, _id: int) -> Music:
        sql = "select * from t_music where id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (_id,))
        ret = cursor.fetchall()[0]
        cursor.close()
        music = self.__row_2_music(ret)
        return music

    def select_by_selective(self, music: Music) -> list:
        sql = "select * from t_music where 1 = 1"
        if music.get_mlid() != None and music.get_mlid() != "":
            sql = sql + " and mlid = '" + str(music.get_mlid()) + "'"
        if music.get_path() != None and music.get_path() != "":
            sql = sql + " and path = '" + music.get_path() + "'"
        musics = []
        cursor = self.conn.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()
        for row in ret:
            music = self.__row_2_music(row)
            musics.append(music)
        return musics

    def insert(self, music: Music):
        sql = "insert into t_music values (null, ?, ?, ?, ?, ?, ?, ?)"
        self.conn.execute(sql, self.__music_2_row(music))
        self.conn.commit()

    def batch_insert(self, musics: list):
        """ 批量插入 """
        sql = "insert into t_music values (null, ?, ?, ?, ?, ?, ?, ?)"
        for music in musics:
            self.conn.execute(sql, self.__music_2_row(music))
        self.conn.commit()

    def delete(self, _id: int):
        """
        删除该歌曲, 即把该歌曲从所属歌单里删除
        :param _id: 歌曲ID
        """
        sql = "delete from t_music where id = ?"
        self.conn.execute(sql, (_id,))
        self.conn.commit()

    def batch_delete(self, _ids: list):
        """ 批量删除 """
        sql = "delete from t_music where id = ?"
        for _id in _ids:
            self.conn.execute(sql, (_id,))
        self.conn.commit()

    def delete_by_mlid(self, mlid: int):
        """ 根据歌单ID删除 """
        sql = "delete from t_music where mlid = ?"
        self.conn.execute(sql, (mlid,))
        self.conn.commit()

    def __music_2_row(self, music: Music) -> tuple:
        return (
            music.get_mlid(), music.get_path(), music.get_size(), music.get_title(),
            music.get_artist(), music.get_album(), music.get_duration())

    def __row_2_music(self, row: tuple):
        """
        把表中查询到的一行数据封装成一个Music对象
        :param row: 一行数据
        :return: Music
        """
        music = Music()
        music.set_id(row[0])
        music.set_mlid(row[1])
        music.set_path(row[2])
        music.set_size(row[3])
        music.set_title(row[4])
        music.set_artist(row[5])
        music.set_album(row[6])
        music.set_duration(row[7])
        return music


if __name__ == "__main__":
    dao = MusicDao()
    # MusicDao().select_by_mlid(2)
    # MusicDao().select_by_id(1)
    # m1 = Music()
    # m1.set_path("D:/13595/Music/ClariS - blossom.mp3")
    # m1.set_title("blossom")
    # m1.set_artist("ClariS")
    # m1.set_album("unknown")
    # m1.set_duration(231)
    # dao.insert(m1)
    # dao.delete(12)
    music = Music()
    music.set_mlid(1)
    music.set_path("/path/a.mp3")
    musics = dao.select_by_selective(music)
    for music in musics:
        print(music)
