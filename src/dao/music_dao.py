import sqlite3

from src.entity.music import Music
from src.common.app_attribute import AppAttribute
from src.util.string_util import StringUtils


class MusicDao:
    def __init__(self):
        self.database = AppAttribute.data_path + "/data.db"
        self.conn = sqlite3.connect(self.database)

    def list_by_mid(self, mid: int) -> list:
        """
        根据歌单ID, 查询该歌单所属的所有歌曲
        :param mid:
        :return:
        """
        sql = "select * from t_music where mid = ?"
        musics_ = []
        cursor = self.conn.cursor()
        cursor.execute(sql, (mid,))
        ret = cursor.fetchall()
        cursor.close()
        for row in ret:
            m = self.__row_2_music(row)
            musics_.append(m)
        return musics_

    def select_by_id(self, _id: int) -> Music:
        sql = "select * from t_music where id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (_id,))
        ret = cursor.fetchall()
        ret = ret[0]
        cursor.close()
        m = self.__row_2_music(ret)
        return m

    def list_(self, m: Music) -> list:
        sql = "select * from t_music where 1 = 1"
        if m is not None:
            if StringUtils.is_not_empty(m.id):
                sql = sql + " and id = '" + str(m.id) + "'"
            if StringUtils.is_not_empty(m.mid):
                sql = sql + " and mid = '" + str(m.mid) + "'"
            if StringUtils.is_not_empty(m.path):
                sql = sql + " and path = '" + m.path + "'"
        musics_ = []
        cursor = self.conn.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()
        for row in ret:
            m = self.__row_2_music(row)
            musics_.append(m)
        return musics_

    def insert(self, music: Music):
        sql = "insert into t_music values (null, ?, ?, ?, ?, ?, ?, ?)"
        self.conn.execute(sql, self.__music_2_row(music))
        self.conn.commit()

    def batch_insert(self, musics: list):
        """ 批量插入 """
        sql = "insert into t_music values (null, ?, ?, ?, ?, ?, ?, ?)"
        for m in musics:
            self.conn.execute(sql, self.__music_2_row(m))
        self.conn.commit()

    def delete(self, id_: int):
        """
        删除该歌曲
        :param id_: 歌曲ID
        """
        sql = "delete from t_music where id = ?"
        self.conn.execute(sql, (id_,))
        self.conn.commit()

    def batch_delete(self, ids_: list):
        """ 批量删除 """
        sql = "delete from t_music where id = ?"
        for _id in ids_:
            self.conn.execute(sql, (_id,))
        self.conn.commit()

    def delete_by_mid(self, mid: int):
        """ 根据歌单ID删除属于该歌单的所有歌曲 """
        sql = "delete from t_music where mid = ?"
        self.conn.execute(sql, (mid,))
        self.conn.commit()

    @staticmethod
    def __music_2_row(m: Music) -> tuple:
        return (
            m.mid, m.path, m.size, m.title,
            m.artist, m.album, m.duration)

    @staticmethod
    def __row_2_music(row: tuple):
        """
        把表中查询到的一行数据封装成一个Music对象
        :param row: 一行数据
        :return: Music
        """
        m = Music()
        m.id = row[0]
        m.mid = row[1]
        m.path = row[2]
        m.size = row[3]
        m.title = row[4]
        m.artist = row[5]
        m.album = row[6]
        m.duration = row[7]
        return m


if __name__ == "__main__":
    pass
