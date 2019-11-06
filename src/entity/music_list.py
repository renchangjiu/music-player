from src.entity.music import Music


class MusicList:
    """歌单"""

    # 默认歌单(即本地歌单)ID
    DEFAULT_ID = 0

    def __init__(self):
        # 歌单id
        self.id = None

        # 歌单名
        self.name = None

        # 创建日期(秒级时间戳)
        self.created = None
        self.created_label = ""

        # 播放次数
        self.play_count = None

        # 所属歌单音乐列表
        self.musics = []

    def get(self, index) -> Music:
        return self.musics[index]

    def __str__(self):
        ret = "MusicList [\n\tid: %s\n\tname: %s,\n\tplay_count: %d\n\tcreted: %s\n\tsize: %d" % (
            self.id, self.name, self.play_count, self.created, len(self.musics))
        ret += "\n\tmusic:[\n"
        for music in self.musics:
            ret += music.__str__()
        ret += "\t]\n]"
        return ret


if __name__ == "__main__":
    pass
