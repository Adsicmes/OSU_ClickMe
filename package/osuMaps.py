from package.osu_db import OsuDB
from package.osu_db import create_db as osu_db_export
from package.osuDir import osuDirGet as osu_dir_get
from loguru import logger


def get_existing_beatmaps() -> list:
    """
    获取现在osu已经存在的铺面
    Returns: 已经存在铺面的sid列表
    """
    logger.info("导出osu!.db...该过程耗时长短取决于你的电脑性能和osu!.db的大小...")
    osu_dir = osu_dir_get()
    logger.info(f"获取到osu的目录为{osu_dir}")
    osu_db_export(f"{osu_dir}\\osu!.db", "osudb_cache.db")
    database = OsuDB("osudb_cache.db")
    logger.info("获取osu目前已经存在的铺面sid...")
    bmset = database.allBeatmapset()
    return bmset


def get_mp_dl_ed() -> list:
    """
    从配置文件里读取已经下载过的铺面
    Returns:已经下载过的铺面的sid列表
    """
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
