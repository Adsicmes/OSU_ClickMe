'''
Author: Adsicmes
Date: 2022-02-03 10:16:47
LastEditTime: 2022-02-06 10:58:24
LastEditors: Adsicmes
Description: 对osu批量指定参数下载新的铺面
FilePath: \OSU!_IF....ClickMe!\downloadNewMap.py
My Mail: adsicmes@foxmail.com
suggest_en: If you have some suggestions, welcome to send it to my mail.
suggest_zh: 如果你对代码有好的建议，欢迎发送到我的邮箱.
'''
from json import dumps
from re import I, compile
from sys import stdout
from package.osu_db import OsuDB
from package.osu_db import create_db as osu_db_export
from package.osuDir import osuDirGet as osu_dir_get
from package.osuDir import songsDir as songs_dir_get
import requests
from loguru import logger
from retrying import retry
from tkinter import *
from tkinter import messagebox
from time import sleep
# from tqdm import tqdm
from shutil import copy
from os import remove
from os import mkdir
from contextlib import closing


__version__ = 1.2


"""
TODO: 添加：osusearch搜索源，更加详细的参数设定 url: https://osusearch.com/search/

osusearch:
https://osusearch.com/query/?

title=1&
artist=1&
source=1&
mapper=1&
diff_name=1&

genres=Novelty&
languages=Instrumental,English&

statuses=Unranked&

modes=Standard,Mania&

date_start=2022-01-30&
date_end=2022-02-01&

min_length=1&
max_length=50424&

min_bpm=54&
max_bpm=28727&

min_favorites=72&
max_favorites=8378&

min_play_count=783&
max_play_count=782374523&

star=(0.00,8.60)&
ar=(5.50,10.00)&
cs=(3.50,10.00)&
hp=(0.00,7.60)&

offset=0
"""

ILLEGAL_CHARS = compile(r"[\<\>:\"\/\\\|\?*]")  # 非法字符


class bmset:
    def __init__(self, title:str, artist:str, mapper:str, sid:int):
        self.title:str = title
        self.artist:str = artist
        self.mapper:str = mapper
        self.sid:int = sid


class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def logconfig() -> None:
    logger.remove()
    LOGURU_FORMAT = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>"
    )
    logger.add(stdout, colorize=True, format=LOGURU_FORMAT)
    logger.add("log\log_{time}.log")


"""@ retry
def user_input() -> int | dict:
    '''
    description: 用户输入数据
    param {*}
    return {*}
    '''
    messagebox.showinfo(title="注意！", message="温馨提示:\n"
                        "1.没必要的地方可以不更改，只更改需要的地方\n"
                        "2.搜索类型会默认为search, search下全功能可用\n"
                        "3.搜索类型不为search则输入信息无效\n"
                        "4.不要开代理！不要开代理！不要开代理！！！\n"
                        "5.把控制台拉宽，不然进度条会不断刷新！\n"
                        "6.窗口没了可能是在最下面，去任务栏找找吧！\n\n"
                        "PS: 该窗口只是组织post数据发送向sayo请求铺面列表，\n    "
                        "具体返回视你填写的参数和sayo具体的返回")

    window = Tk()  # 实例化tk

    window.title("Download Params Input")
    # window.geometry('500x100')

    dlCount = StringVar()
    dlCount.set("200")

    keyword = StringVar()

    label_dlCount = Label(window, text="下载量")
    label_keyword = Label(window, text="搜索关键字")
    entry_dlCount = Entry(window, textvariable=dlCount)
    entry_keyword = Entry(window, textvariable=keyword)

    label_starsL = Label(window, text="最低star")
    label_starsH = Label(window, text="最高star")
    label_arL = Label(window, text="最低ar")
    label_arH = Label(window, text="最高ar")
    label_hpL = Label(window, text="最低hp")
    label_hpH = Label(window, text="最高hp")
    label_odL = Label(window, text="最低od")
    label_odH = Label(window, text="最高od")
    label_csL = Label(window, text="最低cs")
    label_csH = Label(window, text="最高cs")
    label_bpmL = Label(window, text="最低bpm")
    label_bpmH = Label(window, text="最高bpm")
    label_lengthL = Label(window, text="最低length")
    label_lengthH = Label(window, text="最高length")

    starsL = StringVar()
    starsL.set("0")

    starsH = StringVar()
    starsH.set("9999")

    arL = StringVar()
    arL.set("0")

    arH = StringVar()
    arH.set("9999")

    hpL = StringVar()
    hpL.set("0")

    hpH = StringVar()
    hpH.set("9999")

    odL = StringVar()
    odL.set("0")

    odH = StringVar()
    odH.set("9999")

    csL = StringVar()
    csL.set("0")

    csH = StringVar()
    csH.set("9999")

    bpmL = StringVar()
    bpmL.set("0")

    bpmH = StringVar()
    bpmH.set("9999")

    lengthL = StringVar()
    lengthL.set("0")

    lengthH = StringVar()
    lengthH.set("9999")

    entry_starsL = Entry(window, textvariable=starsL)
    entry_starsH = Entry(window, textvariable=starsH)
    entry_arL = Entry(window, textvariable=arL)
    entry_arH = Entry(window, textvariable=arH)
    entry_hpL = Entry(window, textvariable=hpL)
    entry_hpH = Entry(window, textvariable=hpH)
    entry_odL = Entry(window, textvariable=odL)
    entry_odH = Entry(window, textvariable=odH)
    entry_csL = Entry(window, textvariable=csL)
    entry_csH = Entry(window, textvariable=csH)
    entry_bpmL = Entry(window, textvariable=bpmL)
    entry_bpmH = Entry(window, textvariable=bpmH)
    entry_lengthL = Entry(window, textvariable=lengthL)
    entry_lengthH = Entry(window, textvariable=lengthH)

    label_dlCount.grid(row=0, column=0)
    label_keyword.grid(row=2, column=0)

    label_starsL.grid(row=3, column=0)
    label_starsH.grid(row=3, column=2)
    label_arL.grid(row=4, column=0)
    label_arH.grid(row=4, column=2)
    label_hpL.grid(row=5, column=0)
    label_hpH.grid(row=5, column=2)
    label_odL.grid(row=6, column=0)
    label_odH.grid(row=6, column=2)
    label_csL.grid(row=7, column=0)
    label_csH.grid(row=7, column=2)
    label_bpmL.grid(row=8, column=0)
    label_bpmH.grid(row=8, column=2)
    label_lengthL.grid(row=9, column=0)
    label_lengthH.grid(row=9, column=2)

    entry_dlCount.grid(row=0, column=1)
    entry_keyword.grid(row=2, column=1)

    entry_starsL.grid(row=3, column=1)
    entry_starsH.grid(row=3, column=3)
    entry_arL.grid(row=4, column=1)
    entry_arH.grid(row=4, column=3)
    entry_hpL.grid(row=5, column=1)
    entry_hpH.grid(row=5, column=3)
    entry_odL.grid(row=6, column=1)
    entry_odH.grid(row=6, column=3)
    entry_csL.grid(row=7, column=1)
    entry_csH.grid(row=7, column=3)
    entry_bpmL.grid(row=8, column=1)
    entry_bpmH.grid(row=8, column=3)
    entry_lengthL.grid(row=9, column=1)
    entry_lengthH.grid(row=9, column=3)

    dlType = IntVar()
    dlType.set(1)

    dlTypeSelect1 = Radiobutton(
        window,
        variable=dlType,
        value=1,
        text="full"
    )
    dlTypeSelect1.grid(row=0, column=2)

    dlTypeSelect2 = Radiobutton(
        window,
        variable=dlType,
        value=2,
        text="novideo"
    )
    dlTypeSelect2.grid(row=0, column=3)

    dlTypeSelect3 = Radiobutton(
        window,
        variable=dlType,
        value=3,
        text="mini"
    )
    dlTypeSelect3.grid(row=0, column=4)

    mapType = IntVar()
    mapType.set(4)

    mapTypeSelect1 = Radiobutton(
        window,
        variable=mapType,
        value=1,
        text='hot'
    )
    mapTypeSelect1.grid(row=10, column=0)

    mapTypeSelect2 = Radiobutton(
        window,
        variable=mapType,
        value=2,
        text='new'
    )
    mapTypeSelect2.grid(row=10, column=1)

    mapTypeSelect3 = Radiobutton(
        window,
        variable=mapType,
        value=3,
        text='packs'
    )
    mapTypeSelect3.grid(row=10, column=2)

    mapTypeSelect4 = Radiobutton(
        window,
        variable=mapType,
        value=4,
        text='search'
    )
    mapTypeSelect4.grid(row=10, column=3)

    subType = IntVar()
    subType.set(1)

    subTypeSelect1 = Radiobutton(
        window,
        variable=subType,
        value=1,
        text='title/titleU'
    )
    subTypeSelect1.grid(row=1, column=0)

    subTypeSelect2 = Radiobutton(
        window,
        variable=subType,
        value=2,
        text='artist/artistU'
    )
    subTypeSelect2.grid(row=1, column=1)

    subTypeSelect3 = Radiobutton(
        window,
        variable=subType,
        value=4,
        text='creator'
    )
    subTypeSelect3.grid(row=1, column=2)

    subTypeSelect4 = Radiobutton(
        window,
        variable=subType,
        value=8,
        text='version'
    )
    subTypeSelect4.grid(row=1, column=3)

    subTypeSelect5 = Radiobutton(
        window,
        variable=subType,
        value=16,
        text='tags'
    )
    subTypeSelect5.grid(row=1, column=4)

    subTypeSelect6 = Radiobutton(
        window,
        variable=subType,
        value=32,
        text='source'
    )
    subTypeSelect6.grid(row=1, column=5)

    mode = IntVar()
    mode.set(1)

    modeSelect1 = Radiobutton(
        window,
        variable=mode,
        value=1,
        text='std'
    )
    modeSelect1.grid(row=11, column=0)

    modeSelect2 = Radiobutton(
        window,
        variable=mode,
        value=2,
        text='taiko'
    )
    modeSelect2.grid(row=11, column=1)

    modeSelect3 = Radiobutton(
        window,
        variable=mode,
        value=4,
        text='ctb'
    )
    modeSelect3.grid(row=11, column=2)

    modeSelect4 = Radiobutton(
        window,
        variable=mode,
        value=8,
        text='mania'
    )
    modeSelect4.grid(row=11, column=3)

    status = IntVar()
    status.set(1)

    statusSelect1 = Radiobutton(
        window,
        variable=status,
        value=1,
        text='Ranked & Approved'
    )
    statusSelect1.grid(row=12, column=0)

    statusSelect2 = Radiobutton(
        window,
        variable=status,
        value=2,
        text='Qualified'
    )
    statusSelect2.grid(row=12, column=1)

    statusSelect3 = Radiobutton(
        window,
        variable=status,
        value=4,
        text='Loved'
    )
    statusSelect3.grid(row=12, column=2)

    statusSelect4 = Radiobutton(
        window,
        variable=status,
        value=8,
        text='Pending & WIP'
    )
    statusSelect4.grid(row=12, column=3)

    statusSelect5 = Radiobutton(
        window,
        variable=status,
        value=16,
        text='Graveyard'
    )
    statusSelect5.grid(row=12, column=4)

    postdata = {
        'offset': 0,
        'cmd': 'beatmaplist'
    }

    def oka(event):
        window.destroy()

    ok = Button(window, text="ok", width=10)
    ok.grid(row=13, column=2)

    ok.bind('<Button-1>', oka)

    window.mainloop()

    match dlType.get():
        case 1: dl = "full"
        case 2: dl = "novideo"
        case 3: dl = "mini"

    match int(mapType.get()):
        case 1: postdata["type"] = "hot"
        case 2: postdata["type"] = "now"
        case 3: postdata["type"] = "packs"
        case 4: postdata["type"] = "search"

    if int(mapType.get()) == 4:
        postdata["subType"] = int(mapType.get())
        postdata["mode"] = int(mode.get())
        postdata["class"] = int(status.get())
        postdata["stars"] = [float(starsL.get()), float(starsH.get())]
        postdata["ar"] = [float(arL.get()), float(arH.get())]
        postdata["od"] = [float(odL.get()), float(odH.get())]
        postdata["cs"] = [float(csL.get()), float(csH.get())]
        postdata["hp"] = [float(hpL.get()), float(hpH.get())]
        postdata["bpm"] = [float(bpmL.get()), float(bpmH.get())]
        postdata["length"] = [float(lengthL.get()), float(lengthH.get())]

    if keyword.get() != '':
        postdata["keyword"] = keyword.get()

    return int(dlCount.get()), postdata, dl
"""

def get_existing_beatmaps() -> list:
    logger.info("导出osu!.db...该过程耗时长短取决于你的电脑性能和osu!.db的大小...")
    osu_dir = osu_dir_get()
    logger.info(f"获取到osu的目录为{osu_dir}")
    osu_db_export(f"{osu_dir}\\osu!.db", "osudb_cache.db")
    database = OsuDB("osudb_cache.db")
    logger.info("获取osu目前已经存在的铺面sid...")
    bmset = database.allBeatmapset()
    return bmset

def get_mp_dl_ed() -> list:
    logger.info("读取已经下载过的sid...")
    try:
        bm_dl_ed = []
        with open("data/bm_have_downloaded.txt", 'r') as f:
            bm_dl = f.readlines()
            for i in bm_dl:
                bm_dl_ed.append(int(i))
        return bm_dl_ed
    except:
        return []

"""def scrape_beatmaps(dlcount: int, postdata: dict) -> list:
    sids = []
    total = dlcount
    exist_maps = get_existing_beatmaps()
    logger.info(f"目前已存在{len(exist_maps)}套铺面")
    logger.info("读取已经下载过的sid...")
    try:
        sids_dl_ed = []
        with open("data/sids_have_downloaded.txt", 'r') as f:
            sids_dl = f.readlines()
            for i in sids_dl:
                sids_dl_ed.append(int(i))
    except:
        pass
    while len(sids) < total:
        sids, postdata = getmaps(sids, dlcount, postdata)

        n = 0
        map_to_del = []
        for i in sids:
            if i in exist_maps:
                logger.info(f"该铺面已存在: {i}")
                map_to_del.append(n)  # 添加的是索引
            n += 1

        n = 0
        for i in sids:
            if i in sids_dl_ed:
                logger.info(f"该铺面已用该下载器下载过: {i}")
                map_to_del.append(n)
            n += 1

        map_to_del = list(set(map_to_del))

        map_to_del.sort(reverse=True)  # 反向排序，从最后删，这样前边的索引就不会变了
        for i in map_to_del:
            sids.pop(i)

        if not postdata:
            break

    return sids
"""

"""def map_detial(sid: int) -> dict:
    url = "https://api.sayobot.cn/v2/beatmapinfo"
    param = {
        "K": sid,
        "T": 0
    }
    resp = requests.get(url, params=param, verify=False).json()
    return resp
"""

def downloadfile(url: str, save_path: str) -> None:
    with closing(requests.get(url, stream=True, verify=False)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        progress = ProgressBar(save_path, total=content_size,
                               unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        with open(save_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))


class InputWindow:
    def __init__(self) -> None:
        messagebox.showinfo(title="注意！", message="温馨提示:\n"
                            "1.没必要的地方可以不更改，只更改需要的地方\n"
                            "2.搜索类型会默认为search, search下全功能可用\n"
                            "3.搜索类型不为search则输入信息无效\n"
                            "4.不要开代理！不要开代理！不要开代理！！！\n"
                            "5.把控制台拉宽，不然进度条有时会不断刷新！\n"
                            "6.窗口没了可能是在最下面，去任务栏找找吧！\n"
                            "7.sayo和osusearch两个系统不同，同样的数据两家的返回可能不同\n\n"
                            "关于搜索源选择:\n"
                            "sayo在中国大陆速度快，但下载慢"
                            "PS: 该窗口只是组织post数据发送请求铺面列表，\n"
                            "    具体情况视你填写的参数和具体的返回")

        self.window_pack_row = 0
        self.window = Tk()
        self.window.title("Download Params Input")
        self.pack_dl()
        self.pack_search()
        self.pack_diff()

    def pack_dl(self) -> None:
        self.dlCount = StringVar()
        self.dlCount.set("200")
        label_dlCount = Label(self.window, text="下载量")
        entry_dlCount = Entry(self.window, textvariable=self.dlCount)
        label_dlCount.grid(row=self.window_pack_row, column=0)
        entry_dlCount.grid(row=self.window_pack_row, column=1)
        self.window_pack_row += 1

    def pack_search(self) -> None:
        self.keyword = StringVar()
        label_keyword = Label(self.window, text="搜索关键字")
        entry_keyword = Entry(self.window, textvariable=self.keyword)
        label_keyword.grid(row=self.window_pack_row, column=0)
        entry_keyword.grid(row=self.window_pack_row, column=1)
        self.window_pack_row += 1

    def pack_diff(self) -> None:
        label_starsL = Label(self.window, text="最低star")
        label_starsH = Label(self.window, text="最高star")
        label_arL = Label(self.window, text="最低ar")
        label_arH = Label(self.window, text="最高ar")
        label_hpL = Label(self.window, text="最低hp")
        label_hpH = Label(self.window, text="最高hp")
        label_odL = Label(self.window, text="最低od")
        label_odH = Label(self.window, text="最高od")
        label_csL = Label(self.window, text="最低cs")
        label_csH = Label(self.window, text="最高cs")
        label_bpmL = Label(self.window, text="最低bpm")
        label_bpmH = Label(self.window, text="最高bpm")
        label_lengthL = Label(self.window, text="最低length")
        label_lengthH = Label(self.window, text="最高length")

        self.starsL = StringVar()
        self.starsL.set("0")

        self.starsH = StringVar()
        self.starsH.set("9999")

        self.arL = StringVar()
        self.arL.set("0")

        self.arH = StringVar()
        self.arH.set("9999")

        self.hpL = StringVar()
        self.hpL.set("0")

        self.hpH = StringVar()
        self.hpH.set("9999")

        self.odL = StringVar()
        self.odL.set("0")

        self.odH = StringVar()
        self.odH.set("9999")

        self.csL = StringVar()
        self.csL.set("0")

        self.csH = StringVar()
        self.csH.set("9999")

        self.bpmL = StringVar()
        self.bpmL.set("0")

        self.bpmH = StringVar()
        self.bpmH.set("9999")

        self.lengthL = StringVar()
        self.lengthL.set("0")

        self.lengthH = StringVar()
        self.lengthH.set("9999")

        entry_starsL = Entry(self.window, textvariable=self.starsL)
        entry_starsH = Entry(self.window, textvariable=self.starsH)
        entry_arL = Entry(self.window, textvariable=self.arL)
        entry_arH = Entry(self.window, textvariable=self.arH)
        entry_hpL = Entry(self.window, textvariable=self.hpL)
        entry_hpH = Entry(self.window, textvariable=self.hpH)
        entry_odL = Entry(self.window, textvariable=self.odL)
        entry_odH = Entry(self.window, textvariable=self.odH)
        entry_csL = Entry(self.window, textvariable=self.csL)
        entry_csH = Entry(self.window, textvariable=self.csH)
        entry_bpmL = Entry(self.window, textvariable=self.bpmL)
        entry_bpmH = Entry(self.window, textvariable=self.bpmH)
        entry_lengthL = Entry(self.window, textvariable=self.lengthL)
        entry_lengthH = Entry(self.window, textvariable=self.lengthH)

        label_starsL.grid(row=self.window_pack_row, column=0)
        label_starsH.grid(row=self.window_pack_row, column=2)
        entry_starsL.grid(row=self.window_pack_row, column=1)
        entry_starsH.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

        label_arL.grid(row=self.window_pack_row, column=0)
        label_arH.grid(row=self.window_pack_row, column=2)
        entry_arL.grid(row=self.window_pack_row, column=1)
        entry_arH.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

        label_hpL.grid(row=self.window_pack_row, column=0)
        label_hpH.grid(row=self.window_pack_row, column=2)
        entry_hpL.grid(row=self.window_pack_row, column=1)
        entry_hpH.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

        label_odL.grid(row=self.window_pack_row, column=0)
        label_odH.grid(row=self.window_pack_row, column=2)
        entry_odL.grid(row=self.window_pack_row, column=1)
        entry_odH.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

        label_csL.grid(row=self.window_pack_row, column=0)
        label_csH.grid(row=self.window_pack_row, column=2)
        entry_csL.grid(row=self.window_pack_row, column=1)
        entry_csH.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

        label_bpmL.grid(row=self.window_pack_row, column=0)
        label_bpmH.grid(row=self.window_pack_row, column=2)
        entry_bpmL.grid(row=self.window_pack_row, column=1)
        entry_bpmH.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

        label_lengthL.grid(row=self.window_pack_row, column=0)
        label_lengthH.grid(row=self.window_pack_row, column=2)
        entry_lengthL.grid(row=self.window_pack_row, column=1)
        entry_lengthH.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

    def pack_ok(self) -> None:
        def oka(event):
            self.window.destroy()

        ok = Button(self.window, text="ok", width=13)
        ok.grid(row=self.window_pack_row, column=2)

        ok.bind('<Button-1>', oka)

    def call_window(self) -> None:
        self.pack_ok()
        self.window.mainloop()


class osusearch(InputWindow):
    def __init__(self) -> None:
        super(osusearch, self).__init__()


# TODO: 整合搜刮铺面
class Sayobot(InputWindow):
    def __init__(self) -> None:
        super(Sayobot, self).__init__()

        self.pack_dlType()
        self.pack_mapType()
        self.pack_subType()
        self.pack_mode()
        self.pack_status()

    def pack_dlType(self) -> None:
        self.dlType = IntVar()
        self.dlType.set(1)

        dlTypeSelect1 = Radiobutton(
            self.window,
            variable=self.dlType,
            value=1,
            text="full"
        )
        dlTypeSelect1.grid(row=self.window_pack_row, column=0)

        dlTypeSelect2 = Radiobutton(
            self.window,
            variable=self.dlType,
            value=2,
            text="novideo"
        )
        dlTypeSelect2.grid(row=self.window_pack_row, column=1)

        dlTypeSelect3 = Radiobutton(
            self.window,
            variable=self.dlType,
            value=3,
            text="mini"
        )
        dlTypeSelect3.grid(row=self.window_pack_row, column=2)
        self.window_pack_row += 1

    def pack_mapType(self) -> None:
        self.mapType = IntVar()
        self.mapType.set(4)

        mapTypeSelect1 = Radiobutton(
            self.window,
            variable=self.mapType,
            value=1,
            text='hot'
        )
        mapTypeSelect1.grid(row=self.window_pack_row, column=0)

        mapTypeSelect2 = Radiobutton(
            self.window,
            variable=self.mapType,
            value=2,
            text='new'
        )
        mapTypeSelect2.grid(row=self.window_pack_row, column=1)

        mapTypeSelect3 = Radiobutton(
            self.window,
            variable=self.mapType,
            value=3,
            text='packs'
        )
        mapTypeSelect3.grid(row=self.window_pack_row, column=2)

        mapTypeSelect4 = Radiobutton(
            self.window,
            variable=self.mapType,
            value=4,
            text='search'
        )
        mapTypeSelect4.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

    def pack_subType(self) -> None:
        self.subType = IntVar()
        self.subType.set(1)

        subTypeSelect1 = Radiobutton(
            self.window,
            variable=self.subType,
            value=1,
            text='title/titleU'
        )
        subTypeSelect1.grid(row=self.window_pack_row, column=0)

        subTypeSelect2 = Radiobutton(
            self.window,
            variable=self.subType,
            value=2,
            text='artist/artistU'
        )
        subTypeSelect2.grid(row=self.window_pack_row, column=1)

        subTypeSelect3 = Radiobutton(
            self.window,
            variable=self.subType,
            value=4,
            text='creator'
        )
        subTypeSelect3.grid(row=self.window_pack_row, column=2)

        subTypeSelect4 = Radiobutton(
            self.window,
            variable=self.subType,
            value=8,
            text='version'
        )
        subTypeSelect4.grid(row=self.window_pack_row, column=3)

        subTypeSelect5 = Radiobutton(
            self.window,
            variable=self.subType,
            value=16,
            text='tags'
        )
        subTypeSelect5.grid(row=self.window_pack_row, column=4)

        subTypeSelect6 = Radiobutton(
            self.window,
            variable=self.subType,
            value=32,
            text='source'
        )
        subTypeSelect6.grid(row=self.window_pack_row, column=5)
        self.window_pack_row += 1

    def pack_mode(self) -> None:
        self.mode = IntVar()
        self.mode.set(1)

        modeSelect1 = Radiobutton(
            self.window,
            variable=self.mode,
            value=1,
            text='std'
        )
        modeSelect1.grid(row=self.window_pack_row, column=0)

        modeSelect2 = Radiobutton(
            self.window,
            variable=self.mode,
            value=2,
            text='taiko'
        )
        modeSelect2.grid(row=self.window_pack_row, column=1)

        modeSelect3 = Radiobutton(
            self.window,
            variable=self.mode,
            value=4,
            text='ctb'
        )
        modeSelect3.grid(row=self.window_pack_row, column=2)

        modeSelect4 = Radiobutton(
            self.window,
            variable=self.mode,
            value=8,
            text='mania'
        )
        modeSelect4.grid(row=self.window_pack_row, column=3)
        self.window_pack_row += 1

    def pack_status(self) -> None:
        self.status = IntVar()
        self.status.set(1)

        statusSelect1 = Radiobutton(
            self.window,
            variable=self.status,
            value=1,
            text='Ranked & Approved'
        )
        statusSelect1.grid(row=self.window_pack_row, column=0)

        statusSelect2 = Radiobutton(
            self.window,
            variable=self.status,
            value=2,
            text='Qualified'
        )
        statusSelect2.grid(row=self.window_pack_row, column=1)

        statusSelect3 = Radiobutton(
            self.window,
            variable=self.status,
            value=4,
            text='Loved'
        )
        statusSelect3.grid(row=self.window_pack_row, column=2)

        statusSelect4 = Radiobutton(
            self.window,
            variable=self.status,
            value=8,
            text='Pending & WIP'
        )
        statusSelect4.grid(row=self.window_pack_row, column=3)

        statusSelect5 = Radiobutton(
            self.window,
            variable=self.status,
            value=16,
            text='Graveyard'
        )
        statusSelect5.grid(row=self.window_pack_row, column=4)
        self.window_pack_row += 1

    def data_handler(self) -> None:
        self.postdata = {
            'offset': 0,
            'cmd': 'beatmaplist',
        }

        match self.dlType.get():
            case 1: self.dlType = "full"
            case 2: self.dlType = "novideo"
            case 3: self.dlType = "mini"

        match int(self.mapType.get()):
            case 1: self.postdata["type"] = "hot"
            case 2: self.postdata["type"] = "now"
            case 3: self.postdata["type"] = "packs"
            case 4: self.postdata["type"] = "search"

        if int(self.mapType.get()) == 4:
            self.postdata["subType"] = int(self.mapType.get())
            self.postdata["mode"] = int(self.mode.get())
            self.postdata["class"] = int(self.status.get())
            self.postdata["stars"] = [
                float(self.starsL.get()), float(self.starsH.get())]
            self.postdata["ar"] = [
                float(self.arL.get()), float(self.arH.get())]
            self.postdata["od"] = [
                float(self.odL.get()), float(self.odH.get())]
            self.postdata["cs"] = [
                float(self.csL.get()), float(self.csH.get())]
            self.postdata["hp"] = [
                float(self.hpL.get()), float(self.hpH.get())]
            self.postdata["bpm"] = [
                float(self.bpmL.get()), float(self.bpmH.get())]
            self.postdata["length"] = [
                float(self.lengthL.get()), float(self.lengthH.get())]

        if self.keyword.get() != '':
            self.postdata["keyword"] = self.keyword.get()

    @ retry
    def call_sayo(self) -> None:
        self.call_window()
        self.data_handler()

    def getmaps(self, bm: list, dlcount: int, postdata: dict) -> tuple:
        logger.info("获取铺面列表...")
        url = "https://api.sayobot.cn/?post"
        while dlcount >= 300:
            offset = postdata["offset"]

            logger.info(f"当前铺面列表获取偏移: {offset}")
            logger.info(f"当前需要下载的量: {dlcount}")

            postdata["limit"] = 300
            logger.info(f"向小夜请求300铺面...")
            resp = requests.post(url, data=dumps(
                postdata), verify=False).json()

            num = len(resp["data"])
            if num < 300:
                for i in resp["data"]:
                    beatmap = bmset(i["title"], i["artist"], i["creator"], i["sid"])
                    bm.append(beatmap)

                logger.warning(f"小夜返回的图不够了!请求{dlcount},返回{num}")
                return bm, False

            for i in resp["data"]:
                beatmap = bmset(i["title"], i["artist"], i["creator"], i["sid"])
                bm.append(beatmap)

            postdata["offset"] = resp["endid"]
            dlcount -= 300
        else:
            offset = postdata["offset"]

            logger.info(f"当前铺面列表获取偏移: {offset}")
            logger.info(f"当前需要下载的量: {dlcount}")

            postdata["limit"] = dlcount
            logger.info(f"向小夜请求{dlcount}铺面...")
            resp = requests.post(url, data=dumps(
                postdata), verify=False).json()

            num = len(resp["data"])
            if num < dlcount:
                for i in resp["data"]:
                    beatmap = bmset(i["title"], i["artist"], i["creator"], i["sid"])
                    bm.append(beatmap)
                logger.warning(f"小夜返回的图不够了!请求{dlcount},返回{num}")
                return bm, False
            else:
                for i in resp["data"]:
                    beatmap = bmset(i["title"], i["artist"], i["creator"], i["sid"])
                    bm.append(beatmap)
            postdata["offset"] = resp["endid"]
        logger.info("获取铺面列表完成")
        return bm, postdata

    def scrape_beatmaps(self):
        bm = []
        total = int(self.dlCount.get())
        exist_maps = get_existing_beatmaps()
        logger.info(f"目前已存在{len(exist_maps)}套铺面")

        bm_dl_ed = get_mp_dl_ed()

        while len(bm) < total:
            bm:list[bmset]
            bm, pd = self.getmaps(bm, int(self.dlCount.get()), self.postdata)

            n = 0
            map_to_del = []
            for i in bm:
                if i.sid in exist_maps:
                    logger.info(f"该铺面已存在: {i}")
                    map_to_del.append(n)  # 添加的是索引
                n += 1

            n = 0
            for i in bm:
                if i.sid in bm_dl_ed:
                    logger.info(f"该铺面已用该下载器下载过: {i}")
                    map_to_del.append(n)
                n += 1

            map_to_del = list(set(map_to_del))

            map_to_del.sort(reverse=True)  # 反向排序，从最后删，这样前边的索引就不会变了
            for i in map_to_del:
                bm.pop(i)

            if not pd:
                break

        return bm


def main_sayo() -> None:
    window = Sayobot()

    window.call_sayo()
    logger.info(f"要下载的数量: {window.dlCount} ,要post的请求如下:\n{window.postdata}")
    sleep(1)

    bm = window.scrape_beatmaps()
    sids = [i.sid for i in bm]
    logger.info(f"要下载的铺面如下:\n{sids}")
    sleep(1)

    try:
        mkdir("download")
    except:
        pass

    try:
        mkdir("data")
    except:
        pass

    logger.info("避免再次下载，添加sid至data文件夹下的sids_have_downloaded.txt ...")
    with open("data/sids_have_downloaded.txt", "a") as f:
        for i in sids:
            f.write(str(f"{i}\n"))

    for i in bm:
        # bm = map_detial(i)
        title, artist, creator = i.title, i.artist, i.mapper
        logger.info(f"正在下载{creator}作图的{artist}-{title}")
        url = f"https://dl.sayobot.cn/beatmaps/download/{window.dlType}/{i.sid}"
        fn = ILLEGAL_CHARS.sub("_", f"{i.sid} {artist}-{title}.osz")
        savepath = f"{songs_dir_get()}\\{fn}"
        logger.info(f"下载复制到路径: {savepath}")
        # downloadfile(url, f"download\\{savepath}")
        downloadfile(url, f"download\\{fn}")
        copy(f"download\\{fn}", savepath)
        remove(f"download\\{fn}")
        sleep(1)

    messagebox.showinfo(title="ok", message="下载完毕")
    logger.info("程序运行完毕")


def main() -> None:
    main_sayo()


if __name__ == '__main__':
    logconfig()
    main()
