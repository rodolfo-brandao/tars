from typing import List
import requests as r
from utils.api_result import ApiResult
from utils.typed_dicts.movie_dict import Movie
from utils.typed_dicts.movie_file_dict import MovieFile


class MovieHandler:
    '''Class to handle all API requests related to movies.'''

    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url
        self.movies: List[Movie] = []
        self.__default_request_timeout_in_seconds = 60

    def search_movies(self, term: str) -> ApiResult:
        '''Searches for movie occurences matching on:
        movie title, actor name, director name or IMDb code.

        Parameters
        ----------
        term : str
            The term to be used as a query in the request.

        Returns
        -------
        ApiResult
            An instance of 'ApiResult' class containing all occurrences
            of the movies along with their respective files.

        Exceptions
        ----------
        request.exceptions.Timeout
            For when a request takes more than 60s to execute.
        '''

        api_result = ApiResult()
        url = f'{self.__base_url}/list_movies.json?query_term={term}'

        try:
            response = r.get(
                url=url, timeout=self.__default_request_timeout_in_seconds)

            if response.status_code == 200:
                response_json = response.json()

                if response_json['data']['movie_count'] >= 1:
                    api_result.set_response(
                        self.__map_movies_response(response_json))
                else:
                    api_result.set_response([])
            else:
                print('Status Code:', response.status_code)
                api_result.set_status_code(response.status_code)
                api_result.set_error_message(
                    'Oops. Looks like something went wrong when making the request :grimacing:')
        except r.exceptions.Timeout:
            api_result.set_status_code(408)
            api_result.set_error_message(
                'Oops. The request timed out :yawning_face:')
            print(f'Status Code: 408\nGET to "{url}" timed out.')

        return api_result

    def __map_movies_response(self, response) -> List[Movie]:
        movies: List[Movie] = []
        for item in response['data']['movies']:
            movie = Movie(
                title=self.__safe_get(item, 'title_long'),
                url=self.__safe_get(item, 'url'),
                poster_url=self.__safe_get(
                    item, 'medium_cover_image'),
                imdb_rating=self.__safe_get(item, 'rating'),
                runtime=f'{self.__safe_get(item, "runtime")}min',
                files=[]
            )

            for file in item['torrents']:
                movie['files'].append(MovieFile(
                    file_url=self.__safe_get(file, 'url'),
                    quality=self.__safe_get(file, 'quality'),
                    type=self.__safe_get(file, 'type'),
                    seeds=self.__safe_get(file, 'seeds'),
                    peers=self.__safe_get(file, 'peers'),
                    size=self.__safe_get(file, 'size')
                ))

            movies.append(movie)
        return movies

    def __safe_get(self, arg: dict, key: str):
        return arg.get(key) or None
