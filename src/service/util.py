import os

from PyQt5.QtGui import QFontMetrics

from src.service import global_variable as gv
from src.entity.music_list import MusicList


# 把秒级时间格式化为mm:ss形式, second: str
def format_time(second):
    second = int(float(second))
    min = "00"
    sec = "00"
    if second < 60:
        if second < 10:
            sec = "0" + str(second)
        else:
            sec = str(second)
    if second >= 60:
        min_int = int(second / 60)
        sec_int = second % 60
        if min_int < 10:
            min = "0" + str(min_int)
        else:
            min = str(min_int)
        if sec_int < 10:
            sec = "0" + str(sec_int)
        else:
            sec = str(sec_int)
    ret = min + ":" + sec
    return ret


# 返回以KB 或 MB表示的文件大小, size: 字节数
def format_size(size):
    pass


# 读取创建的歌单
def get_music_lists():
    music_lists = []
    names = os.listdir(gv.music_list_path)
    for name in names:
        music_lists.append(MusicList.from_disk(gv.music_list_path + name))
    return music_lists


# 把字符串中的特殊字符转义
def encode(str_=""):
    return str_.replace('"', "&#34;").replace('\\', "&#92;")


# 反转义
def decode(str_=""):
    return str_.replace("&#34;", '"').replace('&#92;', "\\")


def search_local_music():
    pass


def get_elided_text(QFont_, str_, max_width):
    fm = QFontMetrics(QFont_)
    # 计算字符串宽度
    w = fm.width(str_)
    # 当字符串宽度大于最大宽度时进行转换
    if w < max_width:
        return str_
    else:
        return __sub(str_, max_width, fm)


def __sub(s, max_width, fm):
    w = fm.width(s)
    if w < max_width:
        return s + "..."
    else:
        return __sub(s[0:-1], max_width, fm)


if __name__ == "__main__":
    pass
