import sqlite3
import global_variable as gv


class MusicListDao:
    def __init__(self):
        # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建
        self.database = "../../data/data.db"
        self.conn = sqlite3.connect(self.database)

    def select_list(self):
        sql = "select * from user"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        print(ret)

    def test(self):
        # 创建一个Cursor:
        cursor = self.conn.cursor()
        # 执行一条SQL语句，创建user表:
        cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
        # 继续执行一条SQL语句，插入一条记录:
        cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
        # 通过rowcount获得插入的行数:
        print(cursor.rowcount)
        # 关闭Cursor:
        cursor.close()
        # 提交事务:
        self.conn.commit()

    def close(self):
        # 关闭Connection:
        self.conn.close()


if __name__ == "__main__":
    MusicListDao().select_list()
