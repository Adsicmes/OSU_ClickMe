class bmset:
    """
    铺面集
    """

    def __init__(self, title: str, artist: str, mapper: str, sid: int):
        self.title: str = title
        self.artist: str = artist
        self.mapper: str = mapper
        self.sid: int = sid
