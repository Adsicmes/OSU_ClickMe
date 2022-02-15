'''
Author: Adsicmes
Date: 2022-02-03 10:16:47
LastEditTime: 2022-02-10 00:43:19
LastEditors: Adsicmes
Description: 对osu批量指定参数下载新的铺面
FilePath: \OSU!_IF....ClickMe!\downloadNewMap.py
My Mail: adsicmes@foxmail.com
suggest_en: If you have some suggestions, welcome to send it to my mail.
suggest_zh: 如果你对代码有好的建议，欢迎发送到我的邮箱.
'''
from json import dumps
from logging import exception
from re import T, compile
from sys import stdout
from tkinter.ttk import Combobox
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
from tkinter.ttk import Separator
from configparser import ConfigParser


__version__ = 2.0
__searchMirror__ = ['sayobot', 'osusearch']
__downloadMirror__ = ['sayobot', 'chimu', 'kitsu', 'beatconnect']  # chimu：血猫 chimu.moe

"""
添加：osusearch搜索源，更加详细的参数设定 url: https://osusearch.com/search/
添加: 血猫下载源，防止sayo炸掉
TODO: 记住选项
"""

ILLEGAL_CHARS = compile(r"[\<\>:\"\/\\\|\?*]")  # 非法字符


class bmset:
    def __init__(self, title: str, artist: str, mapper: str, sid: int):
        self.title: str = title
        self.artist: str = artist
        self.mapper: str = mapper
        self.sid: int = sid

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

def newdir() -> None:
    for i in ['download', 'data']:
        try:
            mkdir(i)
        except:
            pass


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


def downloadfile(url: str, save_path: str) -> None | bool:
    with closing(requests.get(url, stream=True, verify=False)) as response:
        if response.status_code == 200:
            response = response
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总大小
            progress = ProgressBar(save_path, total=content_size,
                                unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
            with open(save_path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
        else:
            return response.status_code

def initSelection() -> tuple[str, str]:
    window = Tk()
    window.title("select")
    try:
        with open(r'data/selection.ini', 'r') as f:
            config = ConfigParser()
            config.read_file(f)
            conf = config['selection']
    except IOError:
        try:
            with open(r'data/selection.ini', 'w') as f:
                f.write("[selection]\n"
                        "search=sayobot\n"
                        "download=sayobot")
        except exception as e:
            logger.error(e)
    except Exception as e:
        logger.error(e)

    searchLabel = Label(window, text="Search源选择", height=3)
    searchLabel.grid(row=0, column=0)

    search = IntVar()
    search.set(1)
    searchSelect1 = Radiobutton(
        window,
        variable=search,
        value=1,
        text="sayobot",
        height=3
        )
    searchSelect1.grid(row=1, column=0)
    searchSelect2 = Radiobutton(
        window,
        variable=search,
        value=2,
        text="osusearch",
        height=3
    )
    searchSelect2.grid(row=1, column=1)


    searchLabel = Label(window, text="Download源选择", height=3)
    searchLabel.grid(row=2, column=0)

    download = IntVar()
    download.set(1)
    downloadSelect1 = Radiobutton(
        window,
        variable=download,
        value=1,
        text="sayobot",
        height=3
    )
    downloadSelect1.grid(row=3, column=0)
    downloadSelect2 = Radiobutton(
        window,
        variable=download,
        value=2,
        text="kitsu",
        height=3
    )
    downloadSelect2.grid(row=3, column=1)
    downloadSelect3 = Radiobutton(
        window,
        variable=download,
        value=3,
        text="Beatconnect"
    )
    downloadSelect3.grid(row=3, column=2)
    downloadSelect4 = Radiobutton(
        window,
        variable=download,
        value=4,
        text="Chimu(Bloodcat)"
    )
    downloadSelect4.grid(row=3, column=3)


    def oka(event):
        window.destroy()

    ok = Button(window, text="ok", width=13)
    ok.grid(row=4, column=2)

    ok.bind('<Button-1>', oka)
    window.mainloop()

    match search.get():
        case 1:search = 'sayobot'
        case 2:search = 'osusearch'

    match download.get():
        case 1:download = 'sayobot'
        case 2:download = 'kitsu'
        case 3:download = 'beatconnect'
        case 4:download = 'chimu'

    return search, download

class InputWindow:
    def __init__(self) -> None:
        self.window_pack_row = 0
        self.window = Tk()
        self.window.title("Download Params Input")

    def pack_dl(self) -> None:
        self.dlCount = StringVar()
        self.dlCount.set("50")
        label_dlCount = Label(self.window, text="下载量")
        entry_dlCount = Entry(self.window, textvariable=self.dlCount)
        label_dlCount.grid(row=self.window_pack_row, column=0)
        entry_dlCount.grid(row=self.window_pack_row, column=1)
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
        # self.starsL.set("0")

        self.starsH = StringVar()
        # self.starsH.set("10")

        self.arL = StringVar()
        # self.arL.set("0")

        self.arH = StringVar()
        # self.arH.set("10")

        self.hpL = StringVar()
        # self.hpL.set("0")

        self.hpH = StringVar()
        # self.hpH.set("10")

        self.odL = StringVar()
        # self.odL.set("0")

        self.odH = StringVar()
        # self.odH.set("10")

        self.csL = StringVar()
        # self.csL.set("0")

        self.csH = StringVar()
        # self.csH.set("10")

        self.bpmL = StringVar()
        # self.bpmL.set("0")

        self.bpmH = StringVar()
        # self.bpmH.set("9999")

        self.lengthL = StringVar()
        # self.lengthL.set("0")

        self.lengthH = StringVar()
        # self.lengthH.set("3600")

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


"""
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

query_order=difficulty&

star=(0.00,8.60)&
ar=(5.50,10.00)&
cs=(3.50,10.00)&
hp=(0.00,7.60)&

offset=0
"""

def scrape_beatmaps(self):
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

class Osusearch(InputWindow):
    def __init__(self) -> None:
        super(Osusearch, self).__init__()
        Sayobot.pack_dlType(self)
        super().pack_dl()
        self.pack_search()
        super().pack_diff()
        self.pack_others()

        sep = Separator(self.window)
        sep.grid(row=self.window_pack_row, column=0,
                 padx=10, pady=10, columnspan=5)
        self.window_pack_row += 1

        self.pack_mode()
        self.pack_date()
        self.pack_status()
        self.pack_orders()

        sep = Separator(self.window)
        sep.grid(row=self.window_pack_row, column=0,
                 padx=10, pady=10, columnspan=5)
        self.window_pack_row += 1

        self.pack_genres()
        self.pack_languages()

    def pack_search(self) -> None:
        self.title = StringVar()
        label_title = Label(self.window, text="↓↓↓ Song title ↓↓↓")
        entry_title = Entry(self.window, textvariable=self.title)

        self.artist = StringVar()
        label_artist = Label(self.window, text="↓↓↓ Song artist ↓↓↓")
        entry_artist = Entry(self.window, textvariable=self.artist)

        self.source = StringVar()
        label_source = Label(self.window, text="↓↓↓ Song source ↓↓↓")
        entry_source = Entry(self.window, textvariable=self.source)

        self.mapper = StringVar()
        label_mapper = Label(self.window, text="↓↓↓ Song mapper ↓↓↓")
        entry_mapper = Entry(self.window, textvariable=self.mapper)

        self.diffname = StringVar()
        label_diffname = Label(self.window, text="↓↓↓ Difficulty name ↓↓↓")
        entry_diffname = Entry(self.window, textvariable=self.diffname)

        label_title.grid(row=self.window_pack_row, column=0)
        label_artist.grid(row=self.window_pack_row, column=1)
        label_source.grid(row=self.window_pack_row, column=2)
        label_mapper.grid(row=self.window_pack_row, column=3)
        label_diffname.grid(row=self.window_pack_row, column=4)
        self.window_pack_row += 1
        entry_title.grid(row=self.window_pack_row, column=0)
        entry_artist.grid(row=self.window_pack_row, column=1)
        entry_source.grid(row=self.window_pack_row, column=2)
        entry_mapper.grid(row=self.window_pack_row, column=3)
        entry_diffname.grid(row=self.window_pack_row, column=4)
        self.window_pack_row += 1

    def pack_mode(self) -> None:
        self.standard = IntVar()
        standardSelection = Checkbutton(
            self.window, text="std", variable=self.standard, onvalue=1, offvalue=0)
        standardSelection.grid(row=self.window_pack_row, column=0)

        self.mania = IntVar()
        maniaSelection = Checkbutton(
            self.window, text="mania", variable=self.mania, onvalue=1, offvalue=0)
        maniaSelection.grid(row=self.window_pack_row, column=1)

        self.taiko = IntVar()
        taikoSelection = Checkbutton(
            self.window, text="taiko", variable=self.taiko, onvalue=1, offvalue=0)
        taikoSelection.grid(row=self.window_pack_row, column=2)

        self.ctb = IntVar()
        ctbSelection = Checkbutton(
            self.window, text="ctb", variable=self.ctb, onvalue=1, offvalue=0)
        ctbSelection.grid(row=self.window_pack_row, column=3)

        self.window_pack_row += 1

    def pack_status(self) -> None:
        self.ranked = IntVar()
        rankedSelection = Checkbutton(
            self.window, text="Ranked", variable=self.ranked, onvalue=1, offvalue=0)
        rankedSelection.grid(row=self.window_pack_row, column=0)

        self.loved = IntVar()
        lovedSelection = Checkbutton(
            self.window, text="loved", variable=self.loved, onvalue=1, offvalue=0)
        lovedSelection.grid(row=self.window_pack_row, column=1)

        self.qualified = IntVar()
        qualifiedSelection = Checkbutton(
            self.window, text="qualified", variable=self.qualified, onvalue=1, offvalue=0)
        qualifiedSelection.grid(row=self.window_pack_row, column=2)

        self.unranked = IntVar()
        unrankedSelection = Checkbutton(
            self.window, text="unranked", variable=self.unranked, onvalue=1, offvalue=0)
        unrankedSelection.grid(row=self.window_pack_row, column=3)

        self.window_pack_row += 1

    def pack_genres(self) -> None:
        self.anime = IntVar()
        animeSelection = Checkbutton(
            self.window, text="anime", variable=self.anime, onvalue=1, offvalue=0)
        animeSelection.grid(row=self.window_pack_row, column=0)

        self.videogame = IntVar()
        videogameSelection = Checkbutton(
            self.window, text="videogame", variable=self.videogame, onvalue=1, offvalue=0)
        videogameSelection.grid(row=self.window_pack_row, column=1)

        self.novelty = IntVar()
        noveltySelection = Checkbutton(
            self.window, text="novelty", variable=self.novelty, onvalue=1, offvalue=0)
        noveltySelection.grid(row=self.window_pack_row, column=2)

        self.electronic = IntVar()
        electronicSelection = Checkbutton(
            self.window, text="electronic", variable=self.electronic, onvalue=1, offvalue=0)
        electronicSelection.grid(row=self.window_pack_row, column=3)

        self.pop = IntVar()
        popSelection = Checkbutton(
            self.window, text="pop", variable=self.pop, onvalue=1, offvalue=0)
        popSelection.grid(row=self.window_pack_row, column=4)

        self.window_pack_row += 1

        self.rock = IntVar()
        rockSelection = Checkbutton(
            self.window, text="rock", variable=self.rock, onvalue=1, offvalue=0)
        rockSelection.grid(row=self.window_pack_row, column=0)

        self.hiphop = IntVar()
        hiphopSelection = Checkbutton(
            self.window, text="hip hop", variable=self.hiphop, onvalue=1, offvalue=0)
        hiphopSelection.grid(row=self.window_pack_row, column=1)

        self.other_genre = IntVar()
        other_genreSelection = Checkbutton(
            self.window, text="other", variable=self.other_genre, onvalue=1, offvalue=0)
        other_genreSelection.grid(row=self.window_pack_row, column=2)

        self.any_genre = IntVar()
        any_genreSelection = Checkbutton(
            self.window, text="any", variable=self.any_genre, onvalue=1, offvalue=0)
        any_genreSelection.grid(row=self.window_pack_row, column=3)

        self.window_pack_row += 1

        sep = Separator(self.window)
        sep.grid(row=self.window_pack_row, column=0,
                 padx=10, pady=10, columnspan=5)

        self.window_pack_row += 1

    def pack_languages(self) -> None:
        self.japanese = IntVar()
        japaneseSelection = Checkbutton(
            self.window, text="Japanese", variable=self.japanese, onvalue=1, offvalue=0)
        japaneseSelection.grid(row=self.window_pack_row, column=0)

        self.instrumental = IntVar()
        instrumentalSelection = Checkbutton(
            self.window, text="Instrumental", variable=self.japanese, onvalue=1, offvalue=0)
        instrumentalSelection.grid(row=self.window_pack_row, column=1)

        self.english = IntVar()
        englishSelection = Checkbutton(
            self.window, text="English", variable=self.english, onvalue=1, offvalue=0)
        englishSelection.grid(row=self.window_pack_row, column=2)

        self.korean = IntVar()
        koreanSelection = Checkbutton(
            self.window, text="Korean", variable=self.korean, onvalue=1, offvalue=0)
        koreanSelection.grid(row=self.window_pack_row, column=3)

        self.chinese = IntVar()
        chineseSelection = Checkbutton(
            self.window, text="Chinese", variable=self.chinese, onvalue=1, offvalue=0)
        chineseSelection.grid(row=self.window_pack_row, column=4)

        self.window_pack_row += 1

        self.german = IntVar()
        germanSelection = Checkbutton(
            self.window, text="German", variable=self.german, onvalue=1, offvalue=0)
        germanSelection.grid(row=self.window_pack_row, column=0)

        self.spanish = IntVar()
        spanishSelection = Checkbutton(
            self.window, text="Spanish", variable=self.spanish, onvalue=1, offvalue=0
        )
        spanishSelection.grid(row=self.window_pack_row, column=1)

        self.italian = IntVar()
        italianSelection = Checkbutton(
            self.window, text="Italian", variable=self.italian, onvalue=1, offvalue=0
        )
        italianSelection.grid(row=self.window_pack_row, column=2)

        self.french = IntVar()
        frenchSelection = Checkbutton(
            self.window, text="French", variable=self.french, onvalue=1, offvalue=0
        )
        frenchSelection.grid(row=self.window_pack_row, column=3)

        self.other_language = IntVar()
        other_languageSelection = Checkbutton(
            self.window, text="Other", variable=self.other_language, onvalue=1, offvalue=0
        )
        other_languageSelection.grid(row=self.window_pack_row, column=4)

        self.window_pack_row += 1

        self.any_language = IntVar()
        any_languageSelection = Checkbutton(
            self.window, text="Any", variable=self.any_language, onvalue=1, offvalue=0
        )
        any_languageSelection.grid(row=self.window_pack_row, column=0)

        self.window_pack_row += 1

        sep = Separator(self.window)
        sep.grid(row=self.window_pack_row, column=0,
                 padx=10, pady=10, columnspan=5)

        self.window_pack_row += 1

    def pack_date(self) -> None:
        self.date_start = StringVar()
        label_date_start = Label(self.window, text="Start date")
        entry_date_start = Entry(self.window, textvariable=self.date_start)
        label_date_start.grid(row=self.window_pack_row, column=0)
        entry_date_start.grid(row=self.window_pack_row, column=1)

        self.date_end = StringVar()
        label_date_end = Label(self.window, text="End date")
        entry_date_end = Entry(self.window, textvariable=self.date_end)
        label_date_end.grid(row=self.window_pack_row, column=2)
        entry_date_end.grid(row=self.window_pack_row, column=3)

        label_date_info = Label(self.window, text="← eg:2020-1-30 格式必须相同")
        label_date_info.grid(row=self.window_pack_row, column=4)

        self.window_pack_row += 1

    def pack_others(self) -> None:
        self.favorites_min = StringVar()
        label_favorites_min = Label(self.window, text="最小Favorites")
        entry_favorites_min = Entry(
            self.window, textvariable=self.favorites_min)
        label_favorites_min.grid(row=self.window_pack_row, column=0)
        entry_favorites_min.grid(row=self.window_pack_row, column=1)

        self.favorites_max = StringVar()
        label_favorites_max = Label(self.window, text="最大Favorites")
        entry_favorites_max = Entry(
            self.window, textvariable=self.favorites_max)
        label_favorites_max.grid(row=self.window_pack_row, column=2)
        entry_favorites_max.grid(row=self.window_pack_row, column=3)

        self.window_pack_row += 1

        self.play_count_min = StringVar()
        label_play_count_min = Label(self.window, text="最小PlayCount")
        entry_play_count_min = Entry(
            self.window, textvariable=self.play_count_min)
        label_play_count_min.grid(row=self.window_pack_row, column=0)
        entry_play_count_min.grid(row=self.window_pack_row, column=1)

        self.play_count_max = StringVar()
        label_play_count_max = Label(self.window, text="最大PlayCount")
        entry_play_count_max = Entry(
            self.window, textvariable=self.play_count_max)
        label_play_count_max.grid(row=self.window_pack_row, column=2)
        entry_play_count_max.grid(row=self.window_pack_row, column=3)

        self.window_pack_row += 1

    def pack_orders(self) -> None:
        self.orders = StringVar()
        label_orders = Label(self.window, text="获取的排序方式")
        label_orders.grid(row=self.window_pack_row, column=0)

        combobox_orders = Combobox(self.window, textvariable=self.orders)
        combobox_orders["value"] = ('date', 'star', 'favorites', 'length', 'play_count',
                                    'difficulty_ar', 'difficulty_od', 'difficulty_cs', 'difficulty_hp', 'bpm')
        combobox_orders.current(0)
        combobox_orders.grid(row=self.window_pack_row, column=1)

        self.reverse = IntVar()
        reverseSelection = Checkbutton(
            self.window, text="reverse", variable=self.reverse, onvalue=1, offvalue=0)
        reverseSelection.grid(row=self.window_pack_row, column=2)

        self.premium = IntVar()
        premiumSelection = Checkbutton(
            self.window, text="Premium mappers only", variable=self.premium, onvalue=1, offvalue=0)
        premiumSelection.grid(row=self.window_pack_row, column=3)

        self.window_pack_row += 1

    def getmaps(self, bm: list, dlcount: int, param: dict) -> tuple:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
                   'Referer': 'https://osusearch.com/'}
        logger.info("获取铺面列表...")
        url = "https://osusearch.com/query/"
        while dlcount >= 18:
            old = len(bm)
            offset = param["offset"]

            logger.info(f"当前铺面列表获取偏移: {offset}")
            logger.info(f"当前仍需下载的量: {dlcount}")

            logger.info(f"向osusearch请求18铺面...")
            resp = requests.get(url, headers=headers, params=param, verify=False)
            resp = resp.json()

            num = len(resp["beatmaps"])
            if num < 18:
                for i in resp["beatmaps"]:
                    beatmap = bmset(i["title"], i["artist"],
                                    i["mapper"], i["beatmapset"])
                    bm.append(beatmap)

# statuses=Ranked,Loved&modes=Standard&date_start=2012-01-01&date_end=2012-12-31&star=(6.00,10.00)&offset=0

                logger.warning(f"osusearch返回的图不够了!请求18,返回{num}")
                sleep(1)
                return bm, False

            for i in resp["beatmaps"]:
                beatmap = bmset(i["title"], i["artist"],
                                i["mapper"], i["beatmapset"])
                bm.append(beatmap)

            param["offset"] += 1

            bm = list(set(bm))
            new = len(bm)

            dlcount -= (new-old)
            sleep(1)
        else:
            if dlcount == 0:
                logger.info("获取铺面列表完成")
                return bm, False

            offset = param["offset"]
            logger.info(f"当前铺面列表获取偏移: {offset}")
            logger.info(f"当前需要下载的量: {dlcount}")

            logger.info(f"向osusearch请求{dlcount}铺面...")
            resp = requests.get(url, headers=headers, params=param, verify=False).json()

            num = len(resp["beatmaps"])
            if num < dlcount:
                for i in resp["beatmaps"]:
                    beatmap = bmset(i["title"], i["artist"],
                                    i["mapper"], i["beatmapset"])
                    bm.append(beatmap)
                logger.warning(f"osusearch返回的图不够了!请求{dlcount},返回{num}")
                sleep(1)
                return bm, False
            else:
                for j in range(dlcount):
                    i = resp["beatmaps"][j]
                    beatmap = bmset(i["title"], i["artist"],
                                    i["mapper"], i["beatmapset"])
                    bm.append(beatmap)
            param["offset"] += 1
        logger.info("获取铺面列表完成")
        sleep(1)
        return bm, param

    def data_handler(self) -> None:
        self.postdata = {
            'offset': 0,
            'title': self.title.get(),
            'artist': self.artist.get(),
            'source': self.source.get(),
            'mapper': self.mapper.get(),
            'diff_name': self.diffname.get(),
            'date_start': self.date_start.get(),
            'date_end': self.date_end.get(),
            # 'min_length': float(self.lengthL.get()),
            # 'max_length': float(self.lengthH.get()),
            # 'min_bpm': float(self.bpmL.get()),
            # 'max_bpm': float(self.bpmH.get()),
            # 'min_favorites': int(self.favorites_min.get()),
            # 'max_favorites': int(self.favorites_max.get()),
            # 'min_play_count': int(self.play_count_min.get()),
            # 'max_play_count': int(self.play_count_max.get())
        }

        for i in [
            ['min_length', 'lengthL'],
            ['max_length', 'lengthH'],
            ['min_bpm', 'bpmL'],
            ['max_bpm', 'bpmH'],
            ['min_favorites', 'favorites_min'],
            ['max_favorites', 'favorites_max'],
            ['min_play_count', 'play_count_min'],
            ['max_play_count', 'play_count_max']
            ]:
            if eval(f'self.{i[1]}.get()') == '':
                continue
            else:
                self.postdata[i[0]] = eval(f'int(self.{i[1]}.get())')

        for i in [
            ['star', 'stars'],
            ['ar', 'ar'],
            ['od', 'od'],
            ['cs', 'cs'],
            ['hp', 'hp']
            ]:
            low = eval(f'self.{i[1]}L.get()')
            high = eval(f'self.{i[1]}H.get()')

            if low == '' and high == '':
                continue
            if low == '':
                low = 0
            if high == '':
                high = 10
            self.postdata[i[0]] = f'({low}, {high})'

        def genres() -> str:
            l = []
            for i in [[self.anime.get(), 'Anime'],
                      [self.novelty.get(), 'Novelty'],
                      [self.electronic.get(), 'Electronic'],
                      [self.pop.get(), 'Pop'],
                      [self.rock.get(), 'Rock'],
                      [self.videogame.get(), 'Video%20Game'],
                      [self.hiphop.get(), 'Hip%20hop'],
                      [self.other_genre.get(), 'Other'],
                      [self.any_genre.get(), 'Any']
                      ]:
                if i[0] == 1:
                    l.append(i[1])

            s = ''
            for i in l:
                s += i
                s += ','
            s = s[:-1]
            return s
        self.postdata['genres'] = genres()

        def languages() -> str:
            l=[]
            for i in [[self.japanese.get(), 'Japanese'], 
                      [self.instrumental.get(), 'Instrumental'], 
                      [self.english.get(), 'English'], 
                      [self.korean.get(), 'Korean'], 
                      [self.chinese.get(), 'Chinese'], 
                      [self.german.get(), 'German'], 
                      [self.spanish.get(), 'Spanish'], 
                      [self.italian.get(), 'Italian'],
                      [self.french.get(), 'French'],
                      ]:
                if i[0] == 1:
                    l.append(i[1])
            
            s = ''
            for i in l:
                s += i
                s += ','
            s = s[:-1]
            return s
        self.postdata['languages'] = languages()

        def map_status() -> str:
            l=[]
            for i in [[self.ranked.get(), 'Ranked'],
                      [self.loved.get(), 'Loved'],
                      [self.qualified.get(), 'Qualified'],
                      [self.unranked.get(), 'Unranked']]:
                if i[0] == 1:
                    l.append(i[1])
            s = ''
            for i in l:
                s += i
                s += ','
            s = s[:-1]
            return s
        self.postdata['statuses'] = map_status()

        def map_mode() -> str:
            l=[]
            for i in [[self.standard.get(), 'Standard'],
                      [self.mania.get(), 'Mania'],
                      [self.taiko.get(), 'Taiko'],
                      [self.ctb.get(), 'CtB']]:
                if i[0] == 1:
                    l.append(i[1])
            s = ''
            for i in l:
                s += i
                s += ','
            s = s[:-1]
            return s
        self.postdata['modes'] = map_mode()

        key_to_del = []
        for key, value in self.postdata.items():
            if value == '' or value == None or value == [] or value == ():
                key_to_del.append(key)
        for i in key_to_del:
            del self.postdata[i]

    # @retry
    def call_out(self) -> None:
        self.call_window()
        self.data_handler()

class Sayobot(InputWindow):
    def __init__(self) -> None:
        super(Sayobot, self).__init__()

        super().pack_dl()
        self.pack_search()
        self.pack_subType()
        super().pack_diff()
        self.pack_dlType()
        self.pack_mapType()
        self.pack_mode()
        self.pack_status()

    def pack_search(self) -> None:
        self.keyword = StringVar()
        label_keyword = Label(self.window, text="搜索关键字")
        entry_keyword = Entry(self.window, textvariable=self.keyword)
        label_keyword.grid(row=self.window_pack_row, column=0)
        entry_keyword.grid(row=self.window_pack_row, column=1)
        self.window_pack_row += 1

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

        match int(self.mapType.get()):
            case 1: self.postdata["type"] = "hot"
            case 2: self.postdata["type"] = "now"
            case 3: self.postdata["type"] = "packs"
            case 4: self.postdata["type"] = "search"

        if int(self.mapType.get()) == 4:
            self.postdata["subType"] = int(self.mapType.get())
            self.postdata["mode"] = int(self.mode.get())
            self.postdata["class"] = int(self.status.get())
            
            for i in [
            ['stars', 'stars'],
            ['ar', 'ar'],
            ['od', 'od'],
            ['cs', 'cs'],
            ['hp', 'hp'],
            ['bpm', 'bpm'],
            ['length', 'length']
            ]:
                low = eval(f'self.{i[1]}L.get()')
                high = eval(f'self.{i[1]}H.get()')

                if low == '' and high == '':
                    continue
                if low == '':
                    low = 0
                if high == '':
                    high = 9999
                self.postdata[i[0]] = f'({low}, {high})'
            
            # self.postdata["stars"] = [
            #     float(self.starsL.get()), float(self.starsH.get())]
            # self.postdata["ar"] = [
            #     float(self.arL.get()), float(self.arH.get())]
            # self.postdata["od"] = [
            #     float(self.odL.get()), float(self.odH.get())]
            # self.postdata["cs"] = [
            #     float(self.csL.get()), float(self.csH.get())]
            # self.postdata["hp"] = [
            #     float(self.hpL.get()), float(self.hpH.get())]
            # self.postdata["bpm"] = [
            #     float(self.bpmL.get()), float(self.bpmH.get())]
            # self.postdata["length"] = [
            #     float(self.lengthL.get()), float(self.lengthH.get())]

        if self.keyword.get() != '':
            self.postdata["keyword"] = self.keyword.get()

    # @retry
    def call_out(self) -> None:
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
                    beatmap = bmset(i["title"], i["artist"],
                                    i["creator"], i["sid"])
                    bm.append(beatmap)

                logger.warning(f"小夜返回的图不够了!请求{dlcount},返回{num}")
                return bm, False

            for i in resp["data"]:
                beatmap = bmset(i["title"], i["artist"],
                                i["creator"], i["sid"])
                bm.append(beatmap)

            postdata["offset"] = resp["endid"]
            dlcount -= 300
        else:
            if dlcount == 0:
                logger.info("获取铺面列表完成")
                return bm, False
            
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
                    beatmap = bmset(i["title"], i["artist"],
                                    i["creator"], i["sid"])
                    bm.append(beatmap)
                logger.warning(f"小夜返回的图不够了!请求{dlcount},返回{num}")
                return bm, False
            else:
                for i in resp["data"]:
                    beatmap = bmset(i["title"], i["artist"],
                                    i["creator"], i["sid"])
                    bm.append(beatmap)
            postdata["offset"] = resp["endid"]
        logger.info("获取铺面列表完成")
        return bm, postdata


def download_sayobot(dlType, sid, filename, savepath):
    url = f"https://dl.sayobot.cn/beatmaps/download/{dlType}/{sid}"
    downloadfile(url, f"download\\{filename}")
    copy(f"download\\{filename}", savepath)
    remove(f"download\\{filename}")

def download_kitsu(dlType, sid, filename, savepath):
    dlType
    url = f"https://kitsu.moe/d/{sid}"
    downloadfile(url, f"download\\{filename}")
    copy(f"download\\{filename}", savepath)
    remove(f"download\\{filename}")

def download_beatconnect(dlType, sid, filename, savepath):
    dlType
    url = f"https://beatconnect.io/b/{sid}"
    downloadfile(url, f"download\\{filename}")
    copy(f"download\\{filename}", savepath)
    remove(f"download\\{filename}")

def download_chimu(dlType, sid, filename, savepath):
    match dlType:
        case 'full': dlType = 1
        case 'novideo': dlType = 0
        case 'mini': dlType = 0
    url = f"https://api.chimu.moe/v1/download/{sid}?n={dlType}"
    downloadfile(url, f"download\\{filename}")
    copy(f"download\\{filename}", savepath)
    remove(f"download\\{filename}")

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
            case 1: dlType = "full"
            case 2: dlType = "novideo"
            case 3: dlType = "mini"
    elif type(window.dlType) == str:
        dlType = window.dlType
    else:
        dlType = 'full'

    match dlType:
        case 1: dlType = 'full'
        case 2: dlType = 'novideo'
        case 3: dlType = 'mini'

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
