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
        sql = "select * from t_music_list"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        for i in range(len(ret)):
            row = ret[i]
            ml = MusicList()
            ml.set_id(row[0])
            ml.set_name(row[1])
            ml.set_play_count(row[2])
            ml.set_created(row[3])
            music_lists.append(ml)
        return music_lists

    def select_by_id(self, _id) -> MusicList:
        """
        select music list by id

        :param _id: 歌单id
        :return: MusicList
        """
        sql = "select * from t_music_list where id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (_id,))
        ret = cursor.fetchall()[0]
        music_list = MusicList()
        music_list.set_id(ret[0])
        music_list.set_name(ret[1])
        music_list.set_play_count(ret[2])
        music_list.set_created(ret[3])
        cursor.close()
        return music_list

    def close(self):
        # 关闭Connection:
        self.conn.close()


if __name__ == "__main__":
    # MusicListDao().select_by_id(1)
    MusicListDao().select_list()
