'''A custom "TypedDict" structure for movies.'''

from typing import List, TypedDict
from utils.typed_dicts.movie_file_dict import MovieFile

Movie = TypedDict(
    'Movie', {
        'title': str,
        'url': str,
        'poster_url': str,
        'imdb_rating': float,
        'runtime': int,
        'files': List[MovieFile]
    }
)
