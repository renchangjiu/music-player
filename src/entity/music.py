import os.path


class Music:
    def __init__(self):
        # 歌曲ID
        self.__id = -1

        # 所属歌单ID
        self.__mlid = -1

        # 文件相关属性
        self.__path = ""
        self.__size = "0KB"

        # mp3相关属性
        self.__image = b""
        self.__title = ""
        self.__artist = ""
        self.__album = ""
        self.__duration = -1

    def __str__(self):
        if self.__from is not None:
            ret = "Music [path: %s, from: %s, file_name: %s, title: %s, artist: %s, album: %s, duration: %d, size: %s" % (
                self.__path, self.__from.get_name(), self.get_file_name(), self.__title, self.__artist, self.__album,
                self.__duration, self.__size)
        else:
            ret = "Music [path: %s, from: none, file_name: %s, title: %s, artist: %s, album: %s, duration: %d, size: %s" % (
                self.__path, self.get_file_name(), self.__title, self.__artist, self.__album,
                self.__duration, self.__size)
        if self.__image != "" and self.__image != b"":
            ret += ", image: has image ]"
        else:
            ret += ", image: ]"
        return ret

    def get_id(self):
        return self.__id

    def set_id(self, _id):
        self.__id = _id

    def get_mlid(self):
        return self.__mlid

    def set_mlid(self, _mlid):
        self.__mlid = _mlid

    def get_path(self):
        return self.__path

    def get_file_name(self):
        return os.path.basename(self.__path)

    def get_image(self):
        return self.__image

    def get_title(self):
        return self.__title

    def get_artist(self):
        return self.__artist

    def get_album(self):
        return self.__album

    def get_duration(self):
        return self.__duration

    def set_path(self, path):
        self.__path = path

    def set_image(self, image):
        self.__image = image

    def set_title(self, title):
        self.__title = title

    def set_artist(self, artist):
        self.__artist = artist

    def set_album(self, album):
        self.__album = album

    def set_duration(self, duration):
        self.__duration = duration

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size


if __name__ == "__main__":
    m = Music()
    m.set_path("d:/test.mp3")
    print(m.get_path())
