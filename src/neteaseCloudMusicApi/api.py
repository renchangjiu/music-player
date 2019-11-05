import json

import requests

from src.entity.music import Music
from src.neteaseCloudMusicApi import encrypt


class NeteaseCloudMusicApi:
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    }

    def lyric(self, id: str):
        url = "http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1" % id
        resp = requests.get(url)
        return resp.text
        # print(resp.text)

    def search(self, keyword: str, type=1, offset=0, total=True, limit=50):
        params = {
            "s": keyword,
            "type": type,
            "offset": offset,
            "total": total,
            "limit": limit,
        }
        url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        params = encrypt.get_params(params)
        encSecKey = encrypt.get_encSecKey()
        data = {
            "params": params,
            "encSecKey": encSecKey
        }
        #
        resp = requests.post(url, headers=self.headers, data=data)
        return resp.text

    def comment(self, id: str):
        params = {
            "rid": "",
            "offset": "0",
            "total": "true",
            "limit": "20",
            "csrf_token": "",
        }
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=" % id
        params = encrypt.get_params(params)
        encSecKey = encrypt.get_encSecKey()
        data = {
            "params": params,
            "encSecKey": encSecKey
        }
        resp = requests.post(url, headers=self.headers, data=data)
        print(resp.text)

    def match_lyric(self, music: Music):
        search_resp = self.search("%s %s" % (music.title, music.artist))
        # 解析搜索响应, 找到最匹配的记录获得其ID
        loads = json.loads(search_resp)
        if loads["result"]["songCount"] <= 0:
            return
        songs = loads["result"]["songs"]
        for song in songs:
            name = song["name"]
            album = song["al"]["name"]
            if name == music.title and album == music.album:
                id = song["id"]
                lyric_resp = self.lyric(id)
                print(lyric_resp)
                lyric_loads = json.loads(lyric_resp)
                if "uncollected" in lyric_loads:
                    return ""
                lyric = lyric_loads["lrc"]["lyric"]
                return lyric


if __name__ == "__main__":
    api = NeteaseCloudMusicApi()
    # api.comment("26333122")
    # api.search("灼之花 洛天依/乐正绫")
    # api.search("only my railgun fripSide")
    # api.lyric("26333122")
    music = Music()
    music.title = "灼之花"
    music.artist = "洛天依/乐正绫"
    music.album = "洛天依作品集"
    api.match_lyric(music)
