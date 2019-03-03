import sqlite3, time
from datetime import datetime

from src.entity.music import Music
from src.entity.music_list import MusicList


class MusicListDao:
    def __init__(self):
        # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建
        self.database = "./data/data.db"
        # self.database = "../../data/data.db"
        self.conn = sqlite3.connect(self.database)

    def select_list(self) -> list:
        """
        查询所有歌单, 注: 本地音乐也是歌单, 但是他的id=0, created=0

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

    def select_local_music(self) -> MusicList:
        """
        查询本地音乐
        :return: music_lists
        """
        sql = "select * from t_music_list where id = 0"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()[0]
        cursor.close()
        music_list = self.__row_2_music_list(row)
        return music_list

    def select_by_id(self, _id: int) -> MusicList:
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

    def logic_delete(self, _id: int):
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
        self.conn.execute(sql, (music_list.get_name(), music_list.get_created(),))
        self.conn.commit()

    def __music_list_2_row(self, ml: MusicList) -> tuple:
        return ml.get_name(), ml.get_created(),

    def __row_2_music_list(self, row: tuple) -> MusicList:
        """
        把表中查询到的一行数据封装成一个 MusicList 对象
        :param row: 一行数据
        :return: MusicList
        """
        music_list = MusicList()
        music_list.set_id(row[0])
        music_list.set_name(row[1])
        music_list.set_play_count(row[2])
        if row[3] != 0:
            # 时间戳转字符串
            _datetime = datetime.fromtimestamp(row[3])
            _str = _datetime.strftime("%Y-%m-%d")
            music_list.set_created(_str)
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
    # music_list.set_name("n4")
    # music_list.set_created(time.strftime("%Y-%m-%d"))
    # dao.insert(music_list)
    # dao.select_by_id_include_music()

