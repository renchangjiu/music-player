import sqlite3
from src.entity.music_list import MusicList


class MusicListDao:
    def __init__(self):
        # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建
        self.database = "../../data/data.db"
        self.conn = sqlite3.connect(self.database)

    def select_list(self) -> list:
        """
        查询所有歌单

        :return: music_lists
        """
        music_lists = []
        sql = "select * from t_music_list where is_deleted = 0 order by created"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()
        for row in ret:
            music_list = self.__row_2_music_list(row)
            music_lists.append(music_list)
        return music_lists

    def select_by_id(self, _id) -> MusicList:
        """
        select music list by id

        :param _id: 歌单id
        :return: MusicList
        """
        sql = "select * from t_music_list where id = ? and is_deleted = 0"
        cursor = self.conn.cursor()
        cursor.execute(sql, (_id,))
        row = cursor.fetchall()[0]
        cursor.close()
        music_list = self.__row_2_music_list(row)
        return music_list

    def logic_delete(self, _id):
        try:
            sql = "update t_music_list set is_deleted = 1 where id = ?"
            cursor = self.conn.cursor()
            cursor.execute(sql, (_id,))
            ret = cursor.fetchall()
            self.conn.commit()
            cursor.close()
            print(ret)
        except sqlite3.OperationalError as err:
            print(err)

    def __row_2_music_list(self, row) -> MusicList:
        """
        把表中查询到的一行数据封装成一个 MusicList 对象
        :param row: 一行数据
        :return: MusicList
        """
        music_list = MusicList()
        music_list.set_id(row[0])
        music_list.set_name(row[1])
        music_list.set_play_count(row[2])
        music_list.set_created(row[3])
        return music_list

    def close(self):
        # 关闭Connection:
        self.conn.close()


if __name__ == "__main__":
    # MusicListDao().select_by_id(1)
    # MusicListDao().select_list()
    MusicListDao().logic_delete(20)
