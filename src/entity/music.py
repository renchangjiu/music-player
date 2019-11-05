class Music:
    def __init__(self):
        # 歌曲ID
        self.id = None

        # 所属歌单ID
        self.mid = None

        # 文件相关属性
        self.path = None
        self.size = None

        # mp3相关属性
        self.image = b""
        self.title = None
        self.artist = None
        self.album = None
        self.duration = None

    def __str__(self):
        if self.__from is not None:
            ret = "Music [path: %s, from: %s,  title: %s, artist: %s, album: %s, duration: %d, size: %s" % (
                self.path, self.__from.name, self.title, self.artist, self.album,
                self.duration, self.size)
        else:
            ret = "Music [path: %s, from: none,  title: %s, artist: %s, album: %s, duration: %d, size: %s" % (
                self.path, self.title, self.artist, self.album,
                self.duration, self.size)
        if self.image != "" and self.image != b"":
            ret += ", image: has image ]"
        else:
            ret += ", image: ]"
        return ret


if __name__ == "__main__":
    pass
