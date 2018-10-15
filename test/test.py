import winreg


def clear_list(list):
    list.clear()
    list = None


if __name__ == "__main__":
    list = [1, 2, 3]
    clear_list(list)
    print(list)
