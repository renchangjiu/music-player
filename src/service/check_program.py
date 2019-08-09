import os, shutil
from src.service.global_variable import GlobalVar


class CheckProgram:

    # def init_install():
    #     if not os.path.exists("./data/install-flag"):
    #         with open("./data/install-flag", "w", encoding="utf-8") as p:
    #             pass
    #         key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    #                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    #         windows_music_path = winreg.QueryValueEx(key, "My Music")[0]
    #         if not os.path.exists("./data/config.ini"):
    #             config_file = open("./data/config.ini", "w", encoding="utf-8")
    #             config_file.write("[music-path]\npath=%s*checked" % windows_music_path)
    #             config_file.close()

    # 检查程序完整性
    @staticmethod
    def check_program():
        db_path = GlobalVar.root_path + "/data/data.db"
        if not os.path.exists(db_path):
            shutil.copyfile(GlobalVar.resource_path + "/empty.db", db_path)
