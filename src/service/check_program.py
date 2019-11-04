import os, shutil
from src.common.app_attribute import AppAttribute
from src.entity.music_list import MusicList
from src.service.music_service import MusicService


class CheckProgram:

    @staticmethod
    def check_program():
        """检查程序完整性"""
        db_file = AppAttribute.db_path + "/data.db"
        if not os.path.exists(db_file):
            shutil.copyfile(AppAttribute.db_path + "/empty.db", db_file)
            music_service = MusicService()
            path = AppAttribute.res_path + "/洛天依 - 清明上河图.mp3"
            music = music_service.gen_music_by_path(path, MusicList.default_id)
            music_service.insert(music)
