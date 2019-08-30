from PyQt5.QtGui import QFontMetrics, QFont

from src.entity.music import Music
from src.entity.music_list import MusicList


# 把秒级时间格式化为mm:ss形式
def format_time(second: int):
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
def format_size(size: int) -> str:
    if size < 1024 * 1024:
        size = str(int(size / 1024)) + "KB"
    else:
        size = str(round(size / 1024 / 1024, 1)) + "MB"
    return size


def search_local_music():
    pass


def get_elided_text(font: QFont, str_: str, max_width: int):
    fm = QFontMetrics(font)
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


def convert_music_list(obj) -> MusicList:
    """ 把参数转换成MusicList, 以方便IDE提示(参数必须是MusicList类型)"""
    return obj


def convert_music(obj) -> Music:
    """ 把参数转换成Music, 以方便IDE提示(参数必须是Music类型)"""
    return obj


if __name__ == "__main__":
    pass
