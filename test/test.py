import json

path = "../data/本地音乐"
f = open(path, "r", encoding="utf-8")
json_str = json.loads(f.read(), encoding="utf-8")
print(json_str)
