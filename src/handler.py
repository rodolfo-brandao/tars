"""
Handles all HTTP requests needed for the BOT.
"""


import os
from typing import Any, List
import requests as r
from dotenv import load_dotenv
from src.models import ApiResult, MovieFile, Movie


load_dotenv()
MOVIES_API_BASE_URL = os.getenv(key="MOVIES_API_BASE_URL")


def search_movies(term: str) -> ApiResult:
    """
    Searches for movie occurrences matching on: title or IMDb code.

    :param term: The term to be used as query param in the request.
    :type term: str

    :return: Essential information regarding the HTTP response.
    :rtype: ApiResult

    :raise Timeout: The request took more than 1min to execute.
    """

    api_result = ApiResult(
        status_code=200,
        response=None,
        error_message=None
    )
    url = f"{MOVIES_API_BASE_URL}/list_movies.json?query_term={term}"

    try:
        response = r.get(
            url=url,
            timeout=60  # seconds
        )

        if response.status_code == 200:
            response_json = response.json()

            if response_json["data"]["movie_count"] >= 1:
                api_result.response = _map_movies(response_json)
            else:
                api_result.response = []
        else:
            print("Status Code:", response.status_code)
            api_result.status_code = response.status_code
            api_result.error_message = "Oops. Looks like something went wrong when" \
            " sending the request :grimacing:"
    except r.exceptions.Timeout:
        api_result.status_code = 408
        api_result.error_message = "Oops. The request timed out :alarm_clock:"
    return api_result


def _map_movies(response: Any) -> List[Movie]:
    """
    Performs a mapping of all records from the API response
    into `Movie` objects.

    :param response: The API response object.
    :type response: Any

    :return: A list with all movies from the API response.
    :rtype: List[Movie]
    """

    movies: List[Movie] = []
    for item in response["data"]["movies"]:
        movie = Movie(
            title=item["title_long"],
            url=item["url"],
            poster_url=item["medium_cover_image"],
            files=[]
        )

        for file in item["torrents"]:
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
