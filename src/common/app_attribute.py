import os


class AppAttribute(object):
    # 应用名称
    app_name = "Rikka Player"

    # 应用根目录, 如: D:/su/GitHub/music-player
    root = ""

    # 数据库文件目录, 如: D:/su/GitHub/music-player/data
    data_path = ""

    # 资源文件目录, D:/su/GitHub/music-player/resource
    res_path = ""

    @classmethod
    def init(cls, argv):
        cls.root = os.path.split(os.path.abspath(argv[0]))[0].replace("\\", "/")
        cls.data_path = cls.root + "/data"
        cls.res_path = cls.root + "/resource"
