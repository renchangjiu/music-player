import sqlite3

from src.entity.music import Music


class MusicDao:
    def __init__(self):
        # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建
        self.database = "../../data/data.db"
        self.conn = sqlite3.connect(self.database)

    def select_by_mlid(self, music_list_id):
        sql = "select * from t_music where mlid = ?"
        musics = []
        cursor = self.conn.cursor()
        cursor.execute(sql, (music_list_id,))
        ret = cursor.fetchall()
        for row in ret:
            music = self.__tuple_2_music(row)
            musics.append(music)
        return musics

    def select_by_id(self, _id):
        sql = "select * from t_music where id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (_id,))
        ret = cursor.fetchall()[0]
        music = self.__tuple_2_music(ret)
        return music

    def __tuple_2_music(self, _tuple):
        """
        把表中查询到的一行数据装换成一个Music对象
        :param _tuple: 一行数据
        :return: Music
        """
        music = Music()
        music.set_id(_tuple[0])
        music.set_mlid(_tuple[1])
        music.set_path(_tuple[2])
        music.set_size(_tuple[3])
        music.set_image(_tuple[4])
        music.set_title(_tuple[5])
        music.set_artist(_tuple[6])
        music.set_album(_tuple[7])
        music.set_duration(_tuple[8])
        return music

if __name__ == "__main__":
    MusicDao().select_by_mlid(2)
    # MusicDao().select_by_id(1)
