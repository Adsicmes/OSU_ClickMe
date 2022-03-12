from package.mirror.search import Osusearch, Sayobot
from package.mirror.download import *
from package.beatmapClass import bmset
from re import compile
from sys import stdout
from package.osuDir import songsDir as songs_dir_get
from loguru import logger
from tkinter import *
from tkinter import messagebox
from time import sleep
# from tqdm import tqdm
from os import mkdir
from package.osuMaps import get_existing_beatmaps
from package.osuMaps import get_mp_dl_ed
from package.downloadInit import initSelection

__version__ = 2.0
__searchMirror__ = ['sayobot', 'osusearch']
__downloadMirror__ = ['sayobot', 'chimu', 'kitsu', 'beatconnect']  # chimu：血猫 chimu.moe

# 非法字符
ILLEGAL_CHARS = compile(r"[\<\>:\"\/\\\|\?*]")


def logconfig() -> None:
    """
    日志类定义
    """
    logger.remove()
    LOGURU_FORMAT = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>"
    )
    logger.add(stdout, colorize=True, format=LOGURU_FORMAT)
    logger.add("log\log_{time}.log")


def newdir() -> None:
    """
    每次启动尝试创建文件夹防止FileNotFoundError
    """
    for i in ['download', 'data']:
        try:
            mkdir(i)
        except:
            pass


def scrape_beatmaps(self):
    """
    搜刮铺面
    Args:
        self: 传入一个类

    Returns:
        获取到的sid的集合
    """
    bm = []
    total = int(self.dlCount.get())
    exist_maps = get_existing_beatmaps()
    logger.info(f"目前已存在{len(exist_maps)}套铺面")

    bm_dl_ed = get_mp_dl_ed()

    while len(bm) < total:
        bm: list[bmset]
        bm, pd = self.getmaps(bm, int(self.dlCount.get()), self.postdata)

        n = 0
        map_to_del = []
        for i in bm:
            if i.sid in exist_maps:
                logger.info(f"该铺面已存在: {i.sid} {i.artist}-{i.title}")
                map_to_del.append(n)  # 添加的是索引
            n += 1

        n = 0
        for i in bm:
            if i.sid in bm_dl_ed:
                logger.info(f"该铺面已用该下载器下载过: {i.sid} {i.artist}-{i.title}")
                map_to_del.append(n)
            n += 1

        map_to_del = list(set(map_to_del))

        map_to_del.sort(reverse=True)  # 反向排序，从最后删，这样前边的索引就不会变了
        for i in map_to_del:
            bm.pop(i)

        if not pd:
            break

    return bm


def main() -> None:
    newdir()
    searchmirror, downloadmirror = initSelection()
    window = eval(f'{searchmirror.capitalize()}()')

    window.call_out()
    logger.info(f"要下载的数量: {window.dlCount.get()} ,要post的请求如下:\n{window.postdata}")
    sleep(1)

    bm = scrape_beatmaps(window)
    sids = [i.sid for i in bm]
    logger.info(f"要下载的铺面如下:\n{sids}")
    sleep(1)

    logger.info("避免再次下载，添加sid至data文件夹下的sids_have_downloaded.txt ...")
    with open("data/sids_have_downloaded.txt", "a") as f:
        for i in sids:
            f.write(str(f"{i}\n"))

    if type(window.dlType) == IntVar:
        dlType = window.dlType.get()
        match dlType:
            case 1:
                dlType = "full"
            case 2:
                dlType = "novideo"
            case 3:
                dlType = "mini"
    elif type(window.dlType) == str:
        dlType = window.dlType
    else:
        dlType = 'full'

    match dlType:
        case 1:
            dlType = 'full'
        case 2:
            dlType = 'novideo'
        case 3:
            dlType = 'mini'

    for i in bm:
        # bm = map_detial(i)
        title, artist, creator = i.title, i.artist, i.mapper
        logger.info(f"正在下载{creator}作图的{artist}-{title}")
        fn = ILLEGAL_CHARS.sub("_", f"{i.sid} {artist}-{title}.osz")
        savepath = f"{songs_dir_get()}\\{fn}"
        logger.info(f"下载复制到路径: {savepath}")
        # downloadfile(url, f"download\\{savepath}")
        eval(f"""download_{downloadmirror}("{dlType}", {i.sid}, "{fn}", "{songs_dir_get()}")""")
        sleep(1)

    messagebox.showinfo(title="ok", message="下载完毕")
    logger.info("程序运行完毕")


if __name__ == '__main__':
    logconfig()
    main()
