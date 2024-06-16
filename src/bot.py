'''This .py file represents the Discord bot, being responsible
for centralizing its events and commands, besides of
communicating with API handlers.'''

from typing import List
import time
import json
import discord
from discord.ext import commands
from handlers.movie_handler import MovieHandler
from models.movie import Movie

settings: dict = {}
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

with open(file='json/settings.json', encoding='UTF-8', mode='r') as file:
    settings = json.load(fp=file)
    file.close()


@bot.event
async def on_ready() -> None:
    '''Logs when the bot is running.'''

    print(f'{bot.user} is running!')


@bot.command(help='Shows the bot latency.')
async def ping(ctx) -> None:
    '''Bot command to send a message showing the bot's current latency in milliseconds.

    Parameters
    ----------
    ctx : Any
        The Discord API context for the bot.'''

    await ctx.send(f'Pong!\nThe current latency is {round(bot.latency * 1000)}ms')


@bot.command(name='search', help='Searches for movie occurences.')
async def search_movies(ctx, *args) -> None:
    '''Bot command to search for movie occurences based on the given term.

    Parameters
    ----------
    ctx : Any
        The Discord API context for the bot.

    *args
        The arguments to be used as query in the handler.
        It is expected to be one of: movie title, actor name, director name or IMDb code.'''

    term = ' '.join(args).lower()
    __movie_handler = MovieHandler(base_url=settings['thirdPartyApiBaseUrl'])
    movies = __movie_handler.search_movies(term=term)

    await ctx.send('Here are the movies that I found')

    messages = __build_search_command_message(movies=movies)

    for message in messages:
        await ctx.send(message)
        __delay(1.5)

    await ctx.send('...\nDone!')


def run() -> None:
    '''Simply runs the bot.
    This function should be called in the "main.py" file.'''

    bot.run(token=settings['token'])


def __build_search_command_message(movies: List[Movie]) -> List[str]:
    messages: List[str] = []
    movie_count: int = 0

    for movie in movies:
        movie_count += 1
        details = f'...\n{movie_count} - **Title**: *{movie.title}*'\
            f'  |  **IMDb Rating**: {movie.imdb_rating}' \
            f'  |  **Runtime**: {movie.runtime}\n'

        file_options: List[str] = []
        for movie_file in movie.files:
            file_options.append(
                f'> URL: {movie_file.file_url}\n'
                f'> **Quality**: {movie_file.quality}'
                f'  |  **Type**: {movie_file.file_type}'
                f'  |  **Seeds**/**Peers**: {movie_file.seeds}/{movie_file.peers}'
                f'  |  **Size**: {movie_file.size}'
            )

        details += '\n\n'.join(file_options)
        messages.append(details)

    return messages


def __delay(seconds: float) -> None:
    time.sleep(seconds)
