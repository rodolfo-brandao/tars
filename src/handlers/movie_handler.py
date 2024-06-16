from typing import List
import requests as r
from models.movie import Movie
from models.movie_file import MovieFile


class MovieHandler:
    '''Class to handle all API requests related to movies.'''

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.movies: List[Movie] = []
        self.__default_request_timeout_in_seconds = 100

    def search_movies(self, term: str) -> List[Movie]:
        '''Searches for movie occurences matching on:
        movie title, actor name, director name or IMDb code.

        Parameters
        ----------
        term : str
            The term to be used as a query in the request.

        Returns
        -------
        list[Movie]
            A list of type 'Movie' containing all occurrences of
            the movies along with their respective files.

        Exceptions
        ----------
        request.exceptions.Timeout
        '''

        try:
            response = r.get(
                url=f'{self.base_url}/list_movies.json?query_term={term}',
                timeout=self.__default_request_timeout_in_seconds)

            if response.status_code == 200:
                response_obj = response.json()

                if response_obj['data']['movie_count'] >= 1:
                    for item in response_obj['data']['movies']:
                        movie = Movie(
                            title=self.__safe_get(item, 'title_long'),
                            imdb_rating=self.__safe_get(item, 'rating'),
                            runtime=f'{self.__safe_get(item, "runtime")}min'
                        )

                        for file in item['torrents']:
                            movie.files.append(MovieFile(
                                file_url=self.__safe_get(file, 'url'),
                                quality=self.__safe_get(file, 'quality'),
                                file_type=self.__safe_get(file, 'type'),
                                seeds=self.__safe_get(file, 'seeds'),
                                peers=self.__safe_get(file, 'peers'),
                                size=self.__safe_get(file, 'size')
                            ))

                        self.movies.append(movie)
        except r.exceptions.Timeout:
            print('Request "search movies" timed out.')

        return self.movies

    def __safe_get(self, arg: dict, key: str):
        '''Safely tries to get the value of the key from a dictionary.
        If the key doesn't exist, returns 'None'.'''

        return arg.get(key) or None
