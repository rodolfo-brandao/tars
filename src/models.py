from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ApiResult:
    status_code: int
    response: Optional[Any]
    error_message: Optional[str]


@dataclass
class MovieFile:
    url: str
    quality: str
    type: str
    seeds: int
    peers: int
    size: str


@dataclass
class Movie:
    title: str
    url: str
    poster_url: str
    files: List[MovieFile]
