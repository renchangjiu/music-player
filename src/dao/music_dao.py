import sqlite3


class MusicDao:
    def __init__(self):
        # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建
        self.database = "../../data/data.db"
        self.conn = sqlite3.connect(self.database)


    def select_by_mlid(self, music_list_id):
        sql = "select * from t_music where mlid = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (music_list_id,))
        ret = cursor.fetchall()
        print(ret)


if __name__ == "__main__":
    MusicDao().select_by_mlid(2)
