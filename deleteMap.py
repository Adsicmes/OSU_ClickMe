'''
Author: Adsicmes
Date: 2022-02-03 10:16:47
LastEditTime: 2022-02-07 21:52:51
LastEditors: Adsicmes
Description: 批量指定参数删除osu的铺面文件
FilePath: \OSU!_IF....ClickMe!\deleteMap.py
My Mail: adsicmes@foxmail.com
suggest_en: If you have some suggestions, welcome to send it to my mail.
suggest_zh: 如果你对代码有好的建议，欢迎发送到我的邮箱.
'''
from os import walk
from os import remove as delfile
from os.path import join as pathjoin
from shutil import rmtree
from sys import stdout
from tkinter import messagebox
from package.osuDir import songsDir, osuDirGet
from loguru import logger
from time import sleep
from tkinter import *
from retrying import retry
import oppadc

__version__ = 2.0

OSUDIR = osuDirGet()
SONGSDIR = songsDir()

UPDATE_INFO = """
--------------v2.0--------------

添加：删除所有铺面
添加：删除非std铺面
添加：删除计算错误的铺面(aspire 不正常图 无sid bid图 notsubmitted等)
添加：删除不包含铺面文件的文件夹

--------------v1.0--------------

实现基本功能，筛选星数,四维,bpm,长度删图
"""

"""
添加: 删除除了std外所有模式的图
TODO: 添加：清理无用素材
TODO: 添加: 删除指定mapper，artist的图
TODO: 改善：异步运行解析
TODO: 添加：删除带有重复文件(md5_hash)的文件夹，删小的
"""


def set_logger() -> None:
    logger.remove()
    LOGURU_FORMAT = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>"
    )
    logger.add(stdout, colorize=True, format=LOGURU_FORMAT)
    logger.add("log\log_{time}.log")


def get_dirs_and_files(path: str) -> tuple[list]:
    """
    获取文件夹下的所有文件和文件夹

    Args:
        path (str): 文件夹路径

    Returns:
        tuple: 返回元组，元组内包含两个列表，第一个是文件夹列表，第二个是文件列表
    """
    input_path = path

    dir_list = []
    file_list = []

    for _, dirs, files in walk(input_path):
        dir_list = dirs
        file_list = files
        break

    return dir_list, file_list


def get_all_maps_osu() -> list:
    all_beatmaps = []

    logger.info("正在获取Songs文件夹下的所有文件夹")
    songFolders, songFiles = get_dirs_and_files(SONGSDIR)
    logger.info(f"获取完毕，共{len(songFolders)}个")

    try:
        songFolders.remove("Failed")
        logger.info("排除Failed文件夹(导入失败铺面的文件夹)")
    except ValueError:
        logger.info("没有导入失败的铺面")

    logger.info("准备遍历所有文件夹下的文件..")
    sleep(1)

    n = 1
    for fold in songFolders:
        full_fold = pathjoin(SONGSDIR, fold)
        _, files = get_dirs_and_files(full_fold)

        if files == []:  # 空文件夹直接下一轮
            continue

        for i in files:  # 非空文件夹进行循环
            try:  # 防止文件名长度不足
                if i[-4:] == '.osu':
                    all_beatmaps.append([fold, i])
            except:
                pass

        logger.info(f"第{n}个文件夹遍历完毕: {fold}")
        n += 1

    logger.info("遍历完毕...")
    sleep(0.3)
    logger.info(f"共找到{len(all_beatmaps)}张铺面")
    sleep(1)
    return all_beatmaps


@retry
def user_input() -> dict | bool | bool | bool | bool | bool:
    window = Tk()
    window.title("Delete Params Input")

    label_delete_star = Label(window, text="删除star")
    label_most_star = Label(window, text="以下          ")
    label_least_star = Label(window, text="以上的图        ")
    label_delete_star.grid(row=0, column=0)
    label_most_star.grid(row=0, column=2)
    label_least_star.grid(row=0, column=4)

    star_most = StringVar()
    star_most.set("0.0")

    star_least = StringVar()
    star_least.set("1000.0")

    entry_star_most = Entry(window, textvariable=star_most, width=10)
    entry_star_least = Entry(window, textvariable=star_least, width=10)
    entry_star_most.grid(row=0, column=1)
    entry_star_least.grid(row=0, column=3)

    label_delete_cs = Label(window, text="删除cs")
    label_most_cs = Label(window, text="以下          ")
    label_least_cs = Label(window, text="以上的图        ")
    label_delete_cs.grid(row=1, column=0)
    label_most_cs.grid(row=1, column=2)
    label_least_cs.grid(row=1, column=4)

    cs_most = StringVar()
    cs_most.set("0.0")

    cs_least = StringVar()
    cs_least.set("1000.0")

    entry_cs_most = Entry(window, textvariable=cs_most, width=10)
    entry_cs_least = Entry(window, textvariable=cs_least, width=10)
    entry_cs_most.grid(row=1, column=1)
    entry_cs_least.grid(row=1, column=3)

    label_delete_ar = Label(window, text="删除ar")
    label_most_ar = Label(window, text="以下          ")
    label_least_ar = Label(window, text="以上的图        ")
    label_delete_ar.grid(row=2, column=0)
    label_most_ar.grid(row=2, column=2)
    label_least_ar.grid(row=2, column=4)

    ar_most = StringVar()
    ar_most.set("0.0")

    ar_least = StringVar()
    ar_least.set("1000.0")

    entry_ar_most = Entry(window, textvariable=ar_most, width=10)
    entry_ar_least = Entry(window, textvariable=ar_least, width=10)
    entry_ar_most.grid(row=2, column=1)
    entry_ar_least.grid(row=2, column=3)

    label_delete_od = Label(window, text="删除od")
    label_most_od = Label(window, text="以下          ")
    label_least_od = Label(window, text="以上的图        ")
    label_delete_od.grid(row=3, column=0)
    label_most_od.grid(row=3, column=2)
    label_least_od.grid(row=3, column=4)

    od_most = StringVar()
    od_most.set("0.0")

    od_least = StringVar()
    od_least.set("1000.0")

    entry_od_most = Entry(window, textvariable=od_most, width=10)
    entry_od_least = Entry(window, textvariable=od_least, width=10)
    entry_od_most.grid(row=3, column=1)
    entry_od_least.grid(row=3, column=3)

    label_delete_hp = Label(window, text="删除hp")
    label_most_hp = Label(window, text="以下          ")
    label_least_hp = Label(window, text="以上的图        ")
    label_delete_hp.grid(row=4, column=0)
    label_most_hp.grid(row=4, column=2)
    label_least_hp.grid(row=4, column=4)

    hp_most = StringVar()
    hp_most.set("0.0")

    hp_least = StringVar()
    hp_least.set("1000.0")

    entry_hp_most = Entry(window, textvariable=hp_most, width=10)
    entry_hp_least = Entry(window, textvariable=hp_least, width=10)
    entry_hp_most.grid(row=4, column=1)
    entry_hp_least.grid(row=4, column=3)

    label_delete_bpm = Label(window, text="删bpm")
    label_most_bpm = Label(window, text="以下          ")
    label_least_bpm = Label(window, text="以上的图        ")
    label_delete_bpm.grid(row=5, column=0)
    label_most_bpm.grid(row=5, column=2)
    label_least_bpm.grid(row=5, column=4)

    bpm_most = StringVar()
    bpm_most.set("0.0")

    bpm_least = StringVar()
    bpm_least.set("1000.0")

    entry_bpm_most = Entry(window, textvariable=bpm_most, width=10)
    entry_bpm_least = Entry(window, textvariable=bpm_least, width=10)
    entry_bpm_most.grid(row=5, column=1)
    entry_bpm_least.grid(row=5, column=3)

    label_delete_length = Label(window, text="删除length")
    label_most_length = Label(window, text="以下          ")
    label_least_length = Label(window, text="以上的图        ")
    label_delete_length.grid(row=6, column=0)
    label_most_length.grid(row=6, column=2)
    label_least_length.grid(row=6, column=4)

    length_most = StringVar()
    length_most.set("0.0")

    length_least = StringVar()
    length_least.set("1000.0")

    entry_length_most = Entry(window, textvariable=length_most, width=10)
    entry_length_least = Entry(window, textvariable=length_least, width=10)
    entry_length_most.grid(row=6, column=1)
    entry_length_least.grid(row=6, column=3)

    label = Label(window, text="请确保游戏处于关闭状态!", height=2)
    label.grid(row=8, column=0, columnspan=5)

    CheckVar1 = IntVar()
    C1 = Checkbutton(window, text="(暂时不可用)删除清除铺面后没用的素材\n(不会删除自己放进去的东西)(耗费时间)", variable=CheckVar1,
                     onvalue=1, offvalue=0, width=60, height=3)
    C1.grid(row=7, column=0, columnspan=4)

    CheckVar2 = IntVar()
    C2 = Checkbutton(window, text="删除计算错误(???)的铺面\n(包括not submitted， 你自己做的铺面，aspire等)", variable=CheckVar2,
                     onvalue=1, offvalue=0, width=60, height=2)
    C2.grid(row=9, column=0, columnspan=5)

    CheckVar3 = IntVar()
    C3 = Checkbutton(window, text="删除非std铺面", variable=CheckVar3,
                     onvalue=1, offvalue=0, width=30, height=2)
    C3.grid(row=10, column=0, columnspan=2)

    CheckVar4 = IntVar()
    CheckVar4.set(1)
    C4 = Checkbutton(window, text="删除不包含铺面文件的文件夹", variable=CheckVar4,
                     onvalue=1, offvalue=0, width=30, height=2)
    C4.grid(row=10, column=2, columnspan=3)

    CheckVar5 = IntVar()
    C5 = Checkbutton(window, text="删  了  所  有  的  图", variable=CheckVar5,
                     onvalue=1, offvalue=0, width=50, height=3)
    C5.grid(row=13, column=0, columnspan=5)

    def oka(event):
        window.destroy()

    ok = Button(window, text="ok", width=5)
    ok.grid(row=7, column=4)

    ok.bind('<Button-1>', oka)

    window.mainloop()

    return_list = {
        "cs": [float(cs_most.get()), float(cs_least.get())],
        "ar": [float(ar_most.get()), float(ar_least.get())],
        "od": [float(od_most.get()), float(od_least.get())],
        "hp": [float(hp_most.get()), float(hp_least.get())],
        "bpm": [float(bpm_most.get()), float(bpm_least.get())],
        "length": [float(length_most.get()), float(length_least.get())],
        "star": [float(star_most.get()), float(star_least.get())]
    }

    match CheckVar1.get():
        case 1: clearfile = True
        case 0: clearfile = False

    match CheckVar2.get():
        case 1: clearcaluerror = True
        case 0: clearcaluerror = False

    match CheckVar3.get():
        case 1: clearnotstd = True
        case 0: clearnotstd = False

    match CheckVar4.get():
        case 1: clearfolderwithnomap = True
        case 0: clearfolderwithnomap = False

    match CheckVar5.get():
        case 1: delall = True
        case 0: delall = False

    return return_list, clearfile, clearcaluerror, clearnotstd, clearfolderwithnomap, delall


def calu_bpm(mp: oppadc.OsuMap) -> tuple[float]:
    min = max = 60*1000/mp.timingpoints[0].ms_per_beat
    for i in mp.timingpoints:
        if i.change:
            result = 60*1000/i.ms_per_beat
            if result > max:
                max = result
            if result < min:
                min = result

    return min, max


def calu_length(mp: oppadc.OsuMap) -> float:  # tuple[int, float]:
    length_ms = mp.hitobjects[-1].starttime - mp.hitobjects[0].starttime
    length_s = length_ms/1000
    return round(length_s, 2)  # int(length_s/60), round(length_s%60, 2)


def isdel(mp: oppadc.OsuMap, params: dict) -> bool:

    bpm_min, bpm_max = calu_bpm(mp)

    length = calu_length(mp)

    """{
        "cs": [float(cs_most.get()), float(cs_least.get())],
        "ar": [float(ar_most.get()), float(ar_least.get())],
        "od": [float(od_most.get()), float(od_least.get())],
        "hp": [float(hp_most.get()), float(hp_least.get())],
        "bpm": [float(bpm_most.get()), float(bpm_least.get())],
        "length": [float(length_most.get()), float(length_least.get())],
        "star": [float(star_most.get()), float(star_least.get())]
    }"""

    mp_star = mp.getStats().total

    if params["star"][0] > mp_star or params["star"][1] < mp_star:
        return True

    if params["bpm"][0] > bpm_max or params["bpm"][1] < bpm_min:
        return True

    if params["length"][0] > length or params["length"][1] < length:
        return True

    if params["ar"][0] > mp.ar or params["ar"][1] < mp.ar:
        return True

    if params["od"][0] > mp.od or params["od"][1] < mp.od:
        return True

    if params["cs"][0] > mp.cs or params["cs"][1] < mp.cs:
        return True

    if params["hp"][0] > mp.hp or params["hp"][1] < mp.hp:
        return True

    return False


def main() -> None:
    print(UPDATE_INFO)
    sleep(3)

    set_logger()
    param, ifFileClear, ifCaluClear, ifNStdClear, ifFolderClear, ifDelAll = user_input()

    if ifDelAll:
        print("听说你想删了所有的图？？")
        sleep(3)
        print("小伙子不错啊~")
        sleep(3)
        sec = input("你真要全删啊？？？")

        match sec:
            case 'y' | 'Y': go = True
            case 'n' | 'N': go = False
        if go:
            logger.info("啊哈哈哈！删你图！！！")
            rmtree(SONGSDIR)

            logger.info("啊哈哈哈！删你数据库！！！")
            sleep(1)
            delfile(pathjoin(OSUDIR, 'osu!.db'))

            logger.info("啊哈哈哈！删你收藏夹！！！")
            sleep(1)
            delfile(pathjoin(OSUDIR, 'collection.db'))
        messagebox.showinfo(
            title="ok", message=f"删除完毕\n总计:\n删除了Songs文件夹\n删除了osu根目录下的osu!.db和collection.db")

    else:
        logger.info(f'准备读取Songs目录: {SONGSDIR}')
        sleep(1)
        all_maps_osu = get_all_maps_osu()

        logger.info('遍历添加要删的图...')
        sleep(3)

        map_to_delete = []

        for i in all_maps_osu:
            songdir = pathjoin(SONGSDIR, i[0])
            mappath = pathjoin(songdir, i[1])
            logger.info(f"解析{i[0]}下的{i[1]}")
            try:
                mp = oppadc.OsuMap(file_path=mappath)
            except NotImplementedError:
                if ifNStdClear:
                    logger.warning(f"非std铺面，加入删除列表{i[1]}")
                    map_to_delete.append(i)
                else:
                    logger.warning(f"非std铺面，跳过解析{i[1]}")
                continue
            except ValueError:
                if ifCaluClear:
                    logger.warning(f"数值计算出错，加入删除列表{i[1]}")
                    map_to_delete.append(i)
                else:
                    logger.warning(f"数值计算出错，跳过解析{i[1]}")
                continue
            except Exception as e:
                logger.warning(f"解析出错 - {e}，跳过解析{i[1]}")
                continue

            try:
                if isdel(mp, param):
                    logger.info(f"添加至删除列表{i[1]}")
                    map_to_delete.append(i)
            except NotImplementedError:
                if ifNStdClear:
                    logger.warning(f"非std铺面，加入删除列表{i[1]}")
                    map_to_delete.append(i)
                else:
                    logger.warning(f"非std铺面，跳过解析{i[1]}")
                continue
            except ValueError:
                if ifCaluClear:
                    logger.warning(f"数值计算出错，加入删除列表{i[1]}")
                    map_to_delete.append(i)
                else:
                    logger.warning(f"数值计算出错，跳过解析{i[1]}")
                continue
            except Exception as e:
                logger.warning(f"解析出错 - {e}，跳过解析{i[1]}")
                continue

        logger.info(f"开始删除，总计{len(map_to_delete)}张图")
        sleep(3)
        for i in map_to_delete:
            full_path = pathjoin(SONGSDIR, i[0], i[1])
            logger.info(f'删除{full_path}')
            delfile(full_path)

        """file_to_del = []
        if ifFileClear:
            pass

        for i in file_to_del:
            # logger.info(f'删除{i}')
            delfile(i)"""

        sleep(1)

        if ifFolderClear:
            dir_to_del = []
            logger.info("开始检测清理空文件夹")
            sleep(3)
            alldir, _ = get_dirs_and_files(SONGSDIR)
            for dir in alldir:
                osu = []
                logger.info(f"正在检测{dir}")
                _, file = get_dirs_and_files(pathjoin(SONGSDIR, dir))
                for f in file:
                    if f[-4:] == ".osu":
                        osu.append(f)
                if osu == []:
                    dir_to_del.append(pathjoin(SONGSDIR, dir))
            sleep(3)
            for i in dir_to_del:
                logger.info(f"正在删除{i}")
                rmtree(i)
        messagebox.showinfo(
            title="ok", message=f"删除完毕\n总计:\n删除了{len(map_to_delete)}个.osu文件\n删除了{len(dir_to_del)}个文件夹")

    logger.info("程序运行完毕")


if __name__ == '__main__':
    # mp = oppadc.OsuMap(r"D:\OSU\Songs\1371996 umu - Ai no Sukima\umu. - Ai no Sukima (Half) [Howling].osu")
    # print(calu_bpm(mp))
    # print(calu_length(mp))
    # user_input()

    main()
