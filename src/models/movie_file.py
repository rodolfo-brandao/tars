class MovieFile:
    """Model class to represent a movie file."""

    def __init__(self, file_url: str, quality: str, file_type: str,
                 seeds: int, peers: int, size: str) -> None:
        self.file_url = file_url
        self.quality = quality
        self.file_type = file_type
        self.seeds = seeds
        self.peers = peers
        self.size = size
