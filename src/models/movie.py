from typing import List
from models.movie_file import MovieFile

class Movie:
    """Model class to represent a movie."""

    def __init__(self, title: str, imdb_rating: float, runtime: int) -> None:
        self.title = title
        self.imdb_rating = imdb_rating
        self.runtime = runtime
        self.files: List[MovieFile] = []
