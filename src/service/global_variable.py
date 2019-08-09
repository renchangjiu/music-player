import os


# 项目的全局参数

class GlobalVar:
    # 项目的根目录
    root_path = os.path.abspath("./")

    # 数据库文件路径
    database_path = root_path + "./data"

    # 资源文件路径
    resource_path = root_path + "./resource"
