from configparser import ConfigParser

from logging import exception
from loguru import logger
from tkinter import *


def initSelection() -> tuple[str, str]:
    """
    下载前的选择界面
    Returns:
        搜索源,下载源的str
    """
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
        case 1:
            search = 'sayobot'
        case 2:
            search = 'osusearch'

    match download.get():
        case 1:
            download = 'sayobot'
        case 2:
            download = 'kitsu'
        case 3:
            download = 'beatconnect'
        case 4:
            download = 'chimu'

    return search, download
