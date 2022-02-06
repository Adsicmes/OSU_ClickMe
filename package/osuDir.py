import win32api
import win32con
from getpass import getuser


def osuDirGet():
    """
    通过注册表获取osu的目录
    最后结尾为双右斜杠  \ \ 
    :return: osu目录
    """
    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,
                              'osu\\DefaultIcon', 0, win32con.KEY_READ)
    osu = win32api.RegQueryValue(key, '')
    osu = str(osu).split("\"")[1].split("\\")
    del osu[-1]
    dir = ''
    for i in osu:
        dir = dir + i + '\\'

    return dir


def songsDir():
    """
    获取osu的Songs文件夹
    :return: Songs文件夹目录
    """
    dir = osuDirGet()
    config = dir + 'osu!.' + getuser() + '.cfg'

    with open(config, encoding='utf-8', errors='ignore') as f:
        a = f.readlines()

    n = 0
    for i in a:
        if 'BeatmapDirectory' in i:
            break
        else:
            n += 1
    a = a[n].replace("\n", "").split(' = ')

    if ':\\' not in a[1]:
        dir = dir + a[1]
    else:
        dir = a[1]

    return dir


if __name__ == '__main__':
    print(songsDir())
