import winreg


def get_windows_music_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "My Music")[0]


if __name__ == "__main__":
    print(get_windows_music_path())
