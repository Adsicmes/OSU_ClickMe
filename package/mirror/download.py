
from shutil import copy
from os import remove
from package.download import downloadfile

def download_sayobot(dlType, sid, filename, savepath):
    """
    下载铺面
    Args:
        dlType: full novideo mini
        sid:
        filename:
        savepath:

    Returns:

    """
    url = f"https://dl.sayobot.cn/beatmaps/download/{dlType}/{sid}"
    downloadfile(url, f"download\\{filename}")
    copy(f"download\\{filename}", savepath)
    remove(f"download\\{filename}")


def download_kitsu(dlType, sid, filename, savepath):
    """
    下载铺面
    Args:
        dlType: 默认完整
        sid:
        filename:
        savepath:

    Returns:

    """
    dlType
    url = f"https://kitsu.moe/d/{sid}"
    downloadfile(url, f"download\\{filename}")
    copy(f"download\\{filename}", savepath)
    remove(f"download\\{filename}")


def download_beatconnect(dlType, sid, filename, savepath):
    """
    下载铺面
    Args:
        dlType: 默认完整
        sid:
        filename:
        savepath:

    Returns:

    """
    dlType
    url = f"https://beatconnect.io/b/{sid}"
    downloadfile(url, f"download\\{filename}")
    try:
        copy(f"download\\{filename}", savepath)
        remove(f"download\\{filename}")
    except FileNotFoundError:
        pass  # TODO: 添加备用源 改结构


def download_chimu(dlType, sid, filename, savepath):
    """
    下载铺面
    Args:
        dlType: 1-full 0-novideo
        sid:
        filename:
        savepath:

    Returns:

    """
    match dlType:
        case 'full':
            dlType = 1
        case 'novideo':
            dlType = 0
        case 'mini':
            dlType = 0
    url = f"https://api.chimu.moe/v1/download/{sid}?n={dlType}"
    downloadfile(url, f"download\\{filename}")
    copy(f"download\\{filename}", savepath)
    remove(f"download\\{filename}")
