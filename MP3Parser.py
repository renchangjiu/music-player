import os


def trip_space(s):
    while len(s) > 0 and s[-1] == '\x00':
        s = s[:-1]
    return s


# 获取ID3V2 相关信息
class ID3V2:
    def __init__(self, file):
        self.file = open(file, 'rb')
        self.ret = {}
        self.ret["has-ID3V2"] = True
        self.ret["TIT2"] = ""
        self.ret["TPE1"] = ""
        self.ret["TALB"] = ""
        self.ret["image-mime-type"] = ""
        self.ret["image-ext"] = ""
        self.ret["image"] = b""

        if self.file.read(3) != b'ID3':
            self.file.close()
            self.ret["has-ID3V2"] = False
            return

        HDR = self.file.read(7)
        # 标签大小
        self.tag_size = HDR[-1] + HDR[-2] * 0x80 + HDR[-3] * 0x4000 + HDR[-4] * 0x200000 + 10

        while True:
            a = self.file.read(1)
            if a == b'\x00' or a == b'\xff': break
            self.file.seek(-1, 1)
            # 帧头的10个字节
            fhdr = self.file.read(10)
            sz = fhdr[-3] + fhdr[-4] * 0x100 + fhdr[-5] * 0x10000 + fhdr[-6] * 0x1000000
            # 标签帧的帧头
            kind = fhdr[0:4].decode()
            # print(kind)
            # TIT2  \x00\x00\x00\t    \x00\x00  \x00 \xc1\xfa\xd5\xbd\xc6\xef\xca\xbf
            # TIT2  \x00\x00\x00\x05  \x00\x00  \x00 \xc6\xae\xd2\xc6
            # 如果是文本类型的标签帧
            if kind != 'APIC':
                # 帧内容
                info = self.file.read(sz)
                # print(kind + str(info))
                try:
                    # 原代码
                    st = info.rfind(b'\xff\xfe')
                    # print("st: " + str(st))
                    if st != -1:  # \x01\xff\xfe.....\xff\xfe
                        self.ret[kind] = trip_space(info[st + 2:].decode('utf16'))
                    elif info.startswith(b'\x03'):
                        self.ret[kind] = trip_space(info[1:].decode())
                    else:  # \x00
                        # print("gbk")
                        # print(info[1:].replace(b'\x00', b'\x20').decode('gbk'))
                        self.ret[kind] = info[1:].replace(b'\x00', b'\x20').decode('gbk')

                    # 我修改的(有些不符合规范的mp3无法处理)
                    # sign_enc = info[0:1]
                    # if sign_enc == b"\x00":
                    #     self.ret[kind] = info[1:].decode("ISO8859-1")
                    # elif sign_enc == b"\x01":
                    #     self.ret[kind] = info[1:].decode("utf-16")
                    # elif sign_enc == b"\x02":
                    #     self.ret[kind] = info[1:].decode("utf-16BE")
                    # elif sign_enc == b"\x03":
                    #     self.ret[kind] = info[1:].decode("utf-8")
                except UnicodeDecodeError as msg:
                    pass
            # 如果文件含有图片
            else:
                byte = self.file.read(sz)
                image_index = byte.find(b"\x69\x6D\x61\x67\x65\x2F")
                byte = byte[image_index + 6:]
                mime_type = "image/"
                # 读取MIME type
                while True:
                    b = byte[0: 1]
                    if b == b"\x00":
                        break
                    else:
                        mime_type += b.decode()
                        byte = byte[1:]
                self.ret["image-mime-type"] = mime_type
                # picture type : 查表可知
                pic_type = byte[1:2]
                byte = byte[2:]
                # 读取description, 一般都是空, 就不编码了
                desc = []
                while True:
                    b = byte[0:1]
                    if b == b"\x00":
                        break
                    else:
                        desc.append(b)
                        byte = byte[1:]
                byte = byte[1:]
                # 图片格式的标志位(jpg or png...)
                sign_byte = byte[0: 2]
                # jpg
                if sign_byte == b"\xff\xd8":
                    self.ret["image-ext"] = ".jpg"
                # png
                elif sign_byte == b"\x89\x50":
                    self.ret["image-ext"] = ".png"
                else:
                    self.ret["image-ext"] = ""
                self.ret["image"] = byte
        # print(self.ret["TIT2"])
        self.file.close()


# 获取ID3V1信息
class ID3V1():
    def __init__(self, path):
        file = open(path, "rb")
        start_index = os.path.getsize(path) - 128
        file.seek(start_index, 0)
        id3v1 = file.read(3)

        self.ret = {}
        self.ret["has-ID3V1"] = False
        self.ret["title"] = ""
        self.ret["artist"] = ""
        self.ret["album"] = ""
        self.ret["year"] = ""
        self.ret["comm"] = ""
        self.ret["category"] = ""
        try:
            if id3v1.decode() == "TAG":
                self.ret["has-ID3V1"] = True
                return
        except UnicodeDecodeError as err:
            return
        # 编码方式不能确定
        # self.ret["title"] = file.read(30).replace(b"\x00", "".encode()).decode("gbk")
        self.ret["title"] = file.read(30).replace(b"\x00", "".encode())
        self.ret["artist"] = file.read(30).replace(b"\x00", "".encode())
        self.ret["album"] = file.read(30).replace(b"\x00", "".encode())
        self.ret["year"] = file.read(4).replace(b"\x00", "".encode())
        self.ret["comm"] = file.read(30).replace(b"\x00", "".encode())
        self.ret["category"] = file.read(1).replace(b"\xff", "".encode()).replace(b"\x0c", "".encode())

        file.close()

    def decode(self):
        pass


# 获取比特率等信息
class MP3Info:
    MP3Version = {0b00: 'MPEG 2.5', 0b01: 'UNDEFINED', 0b10: 'MPEG 2', 0b11: 'MPEG 1'}
    MP3Layer = {0b00: 'UNDEFINED', 0b01: 'Layer 3', 0b10: 'Layer 2', 0b11: 'Layer 1'}
    MP3CRC = {0b0: '校检', 0b1: '非校检'}
    MP3Bitrate = {0b0000: 'free',
                  0b0001: 32,
                  0b0010: 40,
                  0b0011: 48,
                  0b0100: 56,
                  0b0101: 64,
                  0b0110: 80,
                  0b0111: 96,
                  0b1000: 112,
                  0b1001: 128,
                  0b1010: 160,
                  0b1011: 192,
                  0b1100: 224,
                  0b1101: 256,
                  0b1110: 320,
                  0b1111: 'bad'}
    MP3Samp_freq = {0b00: 441000, 0b01: 48000, 0b10: 32000, 0b11: 'UNdefined'}
    MP3Frame_mod = {0: '无需调整', 1: '调整'}
    MP3Trackmod = {0b00: '立体声', 0b01: '联合立体声', 0b10: '双声道', 0b11: '单声道'}
    MP3Copyright = {0b0: '不合法', 0b1: '合法'}
    MP3Original = {0b0: '非原版', 0b1: '原版'}

    def __init__(self, file):
        self.name = file
        try:
            self.file = open(file, 'rb')
        except IOError as msg:
            print('{0:s} open Error! {1:s}'.format(self.name, msg))
            return
        if self.file.read(3) == b'ID3':
            HDR = self.file.read(7)
            tagsz = HDR[-1] + HDR[-2] * 0x80 + HDR[-3] * 0x4000 + HDR[-4] * 0x200000 + 10
            self.file.seek(tagsz, 0)
        else:
            self.file.seek(0)
        framehdr = self.file.read(4)
        vbrinfo = self.file.read(32)
        self.file.close()
        self.ret = {}
        self.version = self.MP3Version[(framehdr[1] & 0b00011000) >> 3] + ' - ' + self.MP3Layer[
            (framehdr[1] & 0b00000110) >> 1]

        self.bitrate = self.MP3Bitrate[framehdr[2] >> 4]
        self.sample_freq = self.MP3Samp_freq[(framehdr[2] & 0b00001100) >> 2]
        self.padding = (framehdr[2] & 0b00000010) >> 1
        self.frame_mod = self.MP3Frame_mod[self.padding]
        self.trackmod = self.MP3Trackmod[framehdr[3] >> 6]
        self.copyright = self.MP3Copyright[(framehdr[3] & 0b00001000) >> 3]
        self.original = self.MP3Original[(framehdr[3] & 0b00000100) >> 2]
        if self.version: self.ret['Version'] = self.version
        if self.bitrate: self.ret['Bitrate'] = self.bitrate
        if self.sample_freq: self.ret['Sample Frequency'] = self.sample_freq
        if self.frame_mod: self.ret['Frame Mode'] = self.frame_mod
        if self.trackmod: self.ret['Track Mode'] = self.trackmod
        if self.copyright: self.ret['Copyright'] = self.copyright
        if self.original: self.ret['Original'] = self.original


class MP3:
    def __init__(self, file):
        self.ret = {}
        if not os.path.exists(file):
            self.ret["error"] = "file not found"
            return

        # 结果集(title, artist, album, image, image-mime-type, image-ext)
        self.ret = {}
        self.path = file
        self.file_name = os.path.basename(file)
        self.title = ""
        self.artist = ""
        self.album = ""
        self.duration = 0
        self.image = b""

        self.bitrate = ""
        self.trackmod = ""
        self.sample_freq = ""

        mp3info = MP3Info(file)
        self.bitrate = mp3info.bitrate
        self.trackmod = mp3info.trackmod
        self.sample_freq = mp3info.sample_freq

        id3v2 = ID3V2(file)
        id3v2_ret = id3v2.ret
        id3v1 = ID3V1(file)
        id3v1_ret = id3v1.ret
        # print(id3v1_ret)

        self.image = id3v2_ret["image"]
        self.ret["image-mime-type"] = id3v2_ret["image-mime-type"]
        self.ret["image-ext"] = id3v2_ret["image-ext"]

        # 计算时长, 秒
        file_size = os.path.getsize(file)
        if mp3info.bitrate != "free" and mp3info.bitrate != "bad" and id3v2.ret["has-ID3V2"]:
            duration_microsec = (file_size - id3v2.tag_size - 128) / mp3info.bitrate * 8000
            self.duration = self.ret["duration"] = int(duration_microsec / 1000 / 1000)

        if id3v2_ret["TIT2"] is None or id3v2_ret["TIT2"].strip() == "":
            self.title = id3v1_ret["title"]
        else:
            self.title = id3v2_ret["TIT2"]

        if id3v2_ret["TPE1"] is None or id3v2_ret["TPE1"].strip() == "":
            self.artist = id3v1_ret["artist"]
        else:
            self.artist = id3v2_ret["TPE1"]

        if id3v2_ret["TALB"] is None or id3v2_ret["TALB"].strip() == "":
            self.album = id3v1_ret["album"]
        else:
            self.album = id3v2_ret["TALB"]

        for k, v in mp3info.ret.items():
            self.ret[k] = v

        for k, v in id3v1_ret.items():
            self.ret[k] = v

        for k, v in id3v2_ret.items():
            self.ret[k] = v
        if self.image != b"":
            self.ret["image"] = b"show in self.image"
        self.ret["path"] = file


# TODO 无法正确处理不符合规范的mp3文件(如id3v2中, 其设置的编码方式不能解码其内容)
# ------------------------------------------------------ usage ------------------------------------------------------ #
def __usage():
    # path = r"D:/13595/Music/李玉刚 石头 - 雨花石.MP3"
    # path = r"D:\13595\Music\周杰伦\周杰伦 - 最长的电影.mp3"
    # path = r"D:\13595\Music\乐正绫 言和 - 清明上河图.mp3"
    # path = r"D:/Applications/Steam/steamapps/common/Left 4 Dead 2/left4dead2/sound/music/gallery_music.mp3"
    # path = r"D:/13595/Music/周杰伦/周杰伦 - 暗号.mp3"
    path = r"D:\13595\Music\初音未来 - 甩葱歌.mp3"
    mp3 = MP3(path)
    print(mp3.path)
    print(mp3.title)
    print(mp3.artist)
    print(mp3.album)
    print(mp3.duration)
    print(mp3.ret)
    # 获取专辑图片
    # if mp3.image != "":
    #     f = open("./" + mp3.file_name + mp3.ret["image-ext"], "wb")
    #     f.write(mp3.image)
    #     f.close()


def __usage1():
    # path = r"D:/13595/Music/"
    path = r"D:/13595/Music/周杰伦/"
    for file in os.listdir(path):
        if file.endswith("mp3") or file.endswith("MP3"):
            mp3 = MP3(path + file)
            print(mp3.title)
            print(mp3.artist)
            print(mp3.album)
            print(mp3.duration)
            print(mp3.ret)


def __test1():
    path = r"D:/13595/Music/"
    for file in os.listdir(path):
        if file.endswith("mp3") or file.endswith("MP3"):
            print()
            mp3 = MP3(path + file)
            print(mp3.title)
            print(mp3.ret)


def __test():
    path = r"D:/13595/Music/李玉刚 石头 - 雨花石.MP3"
    file = open(path, "rb")
    file.read(20000)
    # print(file.read(20000))
    file.read(20000)
    print(file.read())


if __name__ == "__main__":
    __usage()
    # pass
    # test()
    # test1()
    # usage1()
# ---------------------------------------------------------- appendix ------------------------------------------------#
# ID3V2 :
# TIT2 标题
# TPE1 歌手
# TALB 专辑
# APIC 图片
# COMM 备注
# TYER 年代
