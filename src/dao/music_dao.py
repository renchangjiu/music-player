import sqlite3

from src.entity.music import Music


class MusicDao:
    def __init__(self):
        # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建
        self.database = "../../data/data.db"
        self.conn = sqlite3.connect(self.database)

    def select_by_mlid(self, music_list_id: str):
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

    def select_by_id(self, _id: str):
        sql = "select * from t_music where id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (_id,))
        ret = cursor.fetchall()[0]
        cursor.close()
        music = self.__row_2_music(ret)
        return music

    def insert(self, music: Music):
        """  id integer primary key autoincrement,
              mlid integer not null, --关联的歌单id
              path text not null, --文件绝对路径
              size integer, --文件大小, 字节
              image text, --封面图片路径
              title text, --MP3 title
              artist text, --MP3 歌手名
              album text, --MP3 专辑名
              duration integer --MP3 时长, 秒"""
        sql = "insert into t_music values (null, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.conn.execute(sql, self.__music_2_row(music))
        self.conn.commit()

    def delete(self, _id: int):
        sql = "delete from t_music where id = ?"
        self.conn.execute(sql, (_id, ))
        self.conn.commit()

    def __music_2_row(self, music: Music) -> tuple:
        return (
            music.get_mlid(), music.get_path(), music.get_size(), music.get_image(), music.get_title(),
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
        music.set_image(row[4])
        music.set_title(row[5])
        music.set_artist(row[6])
        music.set_album(row[7])
        music.set_duration(row[8])
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
    dao.delete(12)
