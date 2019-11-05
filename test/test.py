import os
import sqlite3


# 统计代码行数, 包括注释及空行
def count_code_lines():
    root = os.path.abspath(os.pardir)
    dirs = [root]
    py_files = []
    while len(dirs) > 0:
        head = dirs.pop(0)
        list_dirs = os.listdir(head)
        for file in list_dirs:
            abs_path = head + "/" + file
            if os.path.isdir(abs_path):
                dirs.append(abs_path)
            elif abs_path.endswith("py"):
                py_files.append(abs_path)
    count = 0
    for py_file in py_files:
        file = open(py_file, mode="r", encoding="utf-8")
        lines = file.readlines()
        count = count + len(lines)
        print(lines)
    print("总行数(含注释及空行): " + str(count))


def select():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # 执行查询语句:
    # cursor.execute("select * from t_test")
    cursor.execute("select * from t_test where id = ?", ("2",))
    # 获得查询结果集:
    values = cursor.fetchall()
    print(type(values))
    print(values)
    cursor.close()
    conn.close()


def example():
    # 连接到SQLite数据库, 数据库文件是test.db, 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('test.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表:
    cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
    # 继续执行一条SQL语句，插入一条记录:
    cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
    # 通过rowcount获得插入的行数:
    print(cursor.rowcount)
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


if __name__ == "__main__":
    print()
    count_code_lines()
    # select()
