import os, json

from MP3Parser import MP3
from util import format_time, encode, decode

from music import Music
from music_list import MusicList


class SearchLocalMusic:
    def __init__(self):
        pass

    @staticmethod
    def search():
        # todo 搜索完成, 写入文件, 发出信号, 使其重读取文件
        # 以 .mp3结尾, 大于100kb的文件
        paths = []
        # 合法的mp3文件
        musics = []
        pans = SearchLocalMusic.__get_exist_pan()
        for pan in pans:
            paths = SearchLocalMusic.__loop_all(pan, paths)
        print(len(paths))
        print(paths)
        print(musics)
        musics = SearchLocalMusic.__get_mp3_info(paths, musics)
        print(musics)
        file = open("./data/local-music.json", "w", encoding="utf-8")
        file.write(SearchLocalMusic.__to_json(musics))
        file.close()

    @staticmethod
    def __to_json(musics):
        ret = '{"size": %d, "musics": [' % len(musics)
        for music in musics:
            music_str = '{'
            music_str += '"path": "%s", "title": "%s", "artist": "%s", "album": "%s", "duration": "%s", "size": "%s"' % (
                encode(music["path"]), encode(music["title"]), encode(music["artist"]), encode(music["album"]),
                music["duration"],
                encode(music["size"]))
            music_str += '},'
            ret += music_str
        if len(musics) > 0:
            ret = ret[0:-1]
        ret += ']}'
        return ret

    @staticmethod
    def __from_json():
        path = "./data/local-music.json"
        file = open(path, "r", encoding="utf-8")
        print(json.loads(file.read()))
        file.close()

    @staticmethod
    def get_exist_result():
        try:
            path = "./data/local-music.json"
            return MusicList.from_disk(path)
        except FileNotFoundError as err:
            return None

    @staticmethod
    def __get_exist_pan():
        pan_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        exist_pan = []
        for pan in pan_list:
            if os.path.isdir(pan + ":/"):
                exist_pan.append(pan + ":/")
        return exist_pan

    @staticmethod
    def __loop_all(path, paths):
        try:
            listdir = os.listdir(path)
            for f in listdir:
                if not path.endswith("/"):
                    p = path + "/" + f
                else:
                    p = path + f
                print(p)
                if (f.endswith("mp3") or f.endswith("MP3")) and os.path.getsize(p) > 100 * 1024:
                    paths.append(p)
                if os.path.isdir(p):
                    SearchLocalMusic.__loop_all(p, paths)
            return paths
        except PermissionError as e:
            pass

    @staticmethod
    def __get_mp3_info(paths, musics):
        for path in paths:
            try:
                print(path)
                mp3 = MP3(path)
                if mp3.ret["has-ID3V2"] and mp3.duration >= 30:
                    size = "0"
                    file_size = os.path.getsize(path)
                    if file_size < 1024 * 1024:
                        size = str(int(file_size / 1024)) + "KB"
                    else:
                        size = str(round(file_size / 1024 / 1024, 1)) + "MB"
                    title = mp3.title
                    if title == "":
                        title = os.path.basename(path)

                    artist = mp3.artist
                    if artist == "":
                        artist = "未知歌手"

                    album = mp3.album
                    if album == "":
                        album = "未知专辑"

                    duration = mp3.duration
                    music = {"path": path, "title": title, "artist": artist, "album": album,
                             "duration": duration, "size": size}
                    # music = Music()
                    # music.set_path(path)
                    # music.set_title(title)
                    # music.set_artist(artist)
                    # music.set_album(album)
                    # music.set_duration(duration)
                    # music.set_size(size)
                    musics.append(music)
            except IndexError as e:
                pass
            except UnicodeDecodeError as e1:
                pass
        return musics


if __name__ == "__main__":
    # SearchLocalMusic.search()
    local_musics = SearchLocalMusic.get_exist_result()
    print(type(local_musics))
    print(local_musics)
