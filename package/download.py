import requests
from retrying import retry
from contextlib import closing


class ProgressBar(object):
    """
    进度显示
    """

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
                             self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size, self.unit)
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


@retry(stop_max_attempt_number=3)
def downloadfile(url: str, save_path: str) -> None:
    """
    分块下载文件，显示进度
    带有retry修饰 3次尝试后停止
    Args:
        url: 目标链接
        save_path: 保存位置

    Returns:
        无
    """
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

