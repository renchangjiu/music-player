import sqlite3
from datetime import datetime

from src.common.app_attribute import AppAttribute
from src.entity.music_list import MusicList


class MusicListDao:
    def __init__(self):
        # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建
        self.database = AppAttribute.data_path + "/data.db"
        self.conn = sqlite3.connect(self.database)

    def select_list(self) -> list:
        """
        查询所有歌单, 注: 本地音乐也是歌单, 其id=0

        :return: music_lists
        """
        music_lists = []
        sql = "select * from t_music_list where is_deleted = 0 and created > 0 order by created"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()
        for row in ret:
            music_list = self.__row_2_music_list(row)
            music_lists.append(music_list)
        return music_lists

    def select_by_id(self, id_: int) -> MusicList:
        """
        select music list by id

        :param id_: 歌单id
        :return: MusicList
        """
        sql = "select * from t_music_list where id = ? and is_deleted = 0"
        cursor = self.conn.cursor()
        cursor.execute(sql, (id_,))
        row = cursor.fetchall()[0]
        cursor.close()
        music_list = self.__row_2_music_list(row)
        return music_list

    def logic_delete(self, _id: int):
        try:
            sql = "update t_music_list set is_deleted = 1 where id = ?"
            cursor = self.conn.cursor()
            cursor.execute(sql, (_id,))
            ret = cursor.fetchall()
            self.conn.commit()
            cursor.close()
        except sqlite3.OperationalError as err:
            print(err)

    def play_count_incr(self, _id: int):
        try:
            sql = "update t_music_list set play_count = play_count + 1 where id = ?"
            cursor = self.conn.cursor()
            cursor.execute(sql, (_id,))
            # ret = cursor.fetchall()
            self.conn.commit()
            cursor.close()
            # print(ret)
        except sqlite3.OperationalError as err:
            print(err)

    def insert(self, music_list: MusicList):
        """
        id integer primary key autoincrement,
          name text  not null, -- 歌单名
          play_count integer  not null, -- 播放次数
          created text  not null, -- 创建时间, yyyy-mm-dd
          is_deleted int default 0 check ( is_deleted = 1 or is_deleted = 0 ) """
        sql = "insert into t_music_list values (null, ?, 0, ?, 0)"
        self.conn.execute(sql, (music_list.name, music_list.created,))
        self.conn.commit()

    @staticmethod
    def __music_list_2_row(ml: MusicList) -> tuple:
        return ml.name, ml.created,

    @staticmethod
    def __row_2_music_list(row: tuple) -> MusicList:
        """
        把表中查询到的一行数据封装成一个 MusicList 对象
        :param row: 一行数据
        :return: MusicList
        """
        music_list = MusicList()
        music_list.id = row[0]
        music_list.name = row[1]
        music_list.play_count = row[2]
        if row[3] != 0:
            # 时间戳转字符串
            _datetime = datetime.fromtimestamp(row[3])
            _str = _datetime.strftime("%Y-%m-%d")
            music_list.created = _str
        return music_list

    def close(self):
        # 关闭Connection:
        self.conn.close()


if __name__ == "__main__":
    dao = MusicListDao()
    # MusicListDao().select_by_id(1)
    # MusicListDao().select_list()
    # MusicListDao().logic_delete(20)
    # music_list = MusicList()
    # music_list.name = "n4"
    # music_list.created = time.strftime("%Y-%m-%d")
    # dao.insert(music_list)
    # dao.select_by_id_include_music()
