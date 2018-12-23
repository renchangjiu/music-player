import re


class LyricLine:
    # start: 该行歌词的开始时间(毫秒)
    # end: 该行歌词的结束时间(毫秒)
    # text: 歌词文本
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text


# TODO 歌词行过长
class LRC:
    def __init__(self, path):
        self.lrc_lines = []
        file = open(path, "r", encoding="gbk", )
        # [al:Love light]
        # [00:24.200]
        # [00:55.720]流れてく 時の中ででも
        ls = file.readlines()
        file.close()
        regex = "\[(\d.*?\d)\](.*)"
        ptn = re.compile(regex)

        for line in ls:
            match = ptn.match(line)
            if match is not None:
                time_str = match.group(1)
                split = time_str.split(":")
                time = int(int(split[0]) * 60 * 1000 + float(split[1]) * 1000)
                lrc_line = {"time": time, "text": match.group(2)}
                self.lrc_lines.append(lrc_line)
        # for lrc_line in self.lrc_lines:
        #     print(lrc_line)
        # for i in range(len(self.lrc_lines)):
        #     print(str(i) + " : " + str(self.lrc_lines[i]))

    # time: 毫秒, 返回该时间在歌词中对应的行数(从0开始计数)
    def get_cur_line(self, time):
        for i in range(len(self.lrc_lines)):
            t = self.lrc_lines[i]["time"]
            if t > time:
                if i == 0:
                    return 0
                return i - 1
        else:
            return len(self.lrc_lines) - 1

    def show2(self, time):
        ret = []
        count = 0
        # 当前歌词所在行数
        cur_line = -1
        # 当前歌词行之前的空行数, 用来计算应滚动的高度
        enpty_lines = 0
        for i in range(len(self.lrc_lines)):
            line = self.lrc_lines[i]
            t = line["time"]
            if count < 1:
                if t > time:
                    if i != 0:
                        text = self.lrc_lines[i - 1]["text"]
                        if text == "":
                            ret[i - 1] = "<p>&nbsp;</p>"
                        else:
                            ret[i - 1] = "<p style='color:white'>%s</p>" % text
                        count += 1
                        cur_line = i
                else:
                    enpty_lines += 1
            text = self.lrc_lines[i]["text"]
            if text == "":
                ret.append("<p>&nbsp;</p>")
            else:
                ret.append("<p>%s</p>" % text)
        return cur_line, enpty_lines, "".join(ret)

    def show(self, time):
        ret = []
        # 当前歌词行之前的空行数, 用来计算应滚动的高度
        empty_lines = 0
        cur_line = self.get_cur_line(time)
        # print(cur_line)
        for i in range(len(self.lrc_lines)):
            text = self.lrc_lines[i]["text"]
            # 计算空行
            if i <= cur_line:
                if text == "":
                    empty_lines += 1
            if text == "":
                ret.append("<p>&nbsp;</p>")
            else:
                if i == cur_line:
                    ret.append("<p style='color:white'>%s</p>" % text)
                else:
                    ret.append("<p>%s</p>" % text)
        return cur_line, empty_lines, "".join(ret)


if __name__ == "__main__":
    path = "./resource/周杰伦 - 红尘客栈.lrc"
    lrc = LRC(path)
    # print(lrc.get_cur_line(120000))
    print(lrc.show(250000))
