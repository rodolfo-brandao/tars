'''A custom "TypedDict" structure for a movie file.'''

from typing import TypedDict

MovieFile = TypedDict(
    'MovieFile', {
        'file_url': str,
        'quality': str,
        'type': str,
        'seeds': int,
        'peers': int,
        'size': str
    }
)
