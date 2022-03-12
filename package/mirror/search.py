from json import dumps
from tkinter.ttk import Combobox
from tkinter.ttk import Separator
from tkinter import *
from time import sleep
import requests
from package.beatmapClass import bmset
from loguru import logger


class InputWindow:
    """
    输入参数界面的父类  必有的参数
    """

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


class Osusearch(InputWindow):
    """
    osusearch搜索源的类
    """

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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
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

            dlcount -= (new - old)
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
            l = []
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
            l = []
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
            l = []
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
    """
    sayobot搜索源的类
    """

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
            case 1:
                self.postdata["type"] = "hot"
            case 2:
                self.postdata["type"] = "now"
            case 3:
                self.postdata["type"] = "packs"
            case 4:
                self.postdata["type"] = "search"

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
