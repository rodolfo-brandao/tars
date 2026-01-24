import requests as r
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ApiResult:
    status_code: int
    response: Any
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


class MovieHandler:
    """
    Handles all HTTP requests from the YTS API.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.movies: List[Movie] = []
        self.default_request_timeout_in_seconds = 60

    def search_movies(self, term: str) -> ApiResult:
        """
        Searches for movie occurences matching on: title or IMDb code.

        :param term: The term to be used as a query in the request.
        :type term: str

        :return: Essential information regarding the HTTP response from the YTS API.
        :rtype: ApiResult

        :raise Timeout: The request took more than 60s to execute.
        """

        api_result = ApiResult(
            status_code=200,
            response=None,
            error_message=None
        )
        url = f"{self.base_url}/list_movies.json?query_term={term}"

        try:
            response = r.get(
                url=url,
                timeout=self.default_request_timeout_in_seconds
            )

            if response.status_code == 200:
                response_json = response.json()

                if response_json['data']['movie_count'] >= 1:
                    api_result.response = self.map_movies(response_json)
                else:
                    api_result.response = []
            else:
                print('Status Code:', response.status_code)
                api_result.status_code = response.status_code
                api_result.error_message = "Oops. Looks like something went wrong when sending the request :grimacing:"
        except r.exceptions.Timeout:
            api_result.status_code = 408
            api_result.error_message = "Oops. The request timed out :alarm_clock:"
            print(f'Status Code: 408\nGET resquest to "{url}" timed out.')
        return api_result

    def map_movies(self, response: Any) -> List[Movie]:
        """
        Performs a mapping of all movies in the API response.

        :param response: The API response object.
        :type response: Any

        :return: A list with all movies from the API response.
        :rtype: List[Movie]
        """

        movies: List[Movie] = []
        for item in response['data']['movies']:
            movie = Movie(
                title=item["title_long"],
                url=item["url"],
                poster_url=item["medium_cover_image"],
                files=[]
            )

            for file in item['torrents']:
                movie.files.append(MovieFile(
                    url=file["url"],
                    quality=file["quality"],
                    type=file["type"],
                    seeds=file["seeds"],
                    peers=file["peers"],
                    size=file["size"]
                ))

            movies.append(movie)
        return movies
