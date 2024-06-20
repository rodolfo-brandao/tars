'''Represents the Discord bot, being responsible for centralizing
its events and commands, besides of communicating with API handlers.'''

from typing import List
import time
import json
import discord
from discord.ext import commands
from handlers.movie_handler import MovieHandler
from utils.typed_dicts.movie_dict import Movie

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
    '''Command to send a message showing the bot's current latency in milliseconds.

    Parameters
    ----------
    ctx : Any
        The Discord API context for the bot.'''

    await ctx.send(f'Pong! :ping_pong:\nThe current latency is {round(bot.latency * 1000)}ms')


@bot.command(name='info', help='Custom "help" command to display all avaliable commands')
async def display_commands(ctx) -> None:
    '''Command to send a message showing all bot's avaliable commands.
    Parameters
    ----------
    ctx : Any
        The Discord API context for the bot.'''

    await ctx.send(embed=__build_help_command_embed())


@bot.command(name='search', help='Searches for movie occurences.')
async def search_movies(ctx, *args) -> None:
    '''Command to search for movie occurences based on the given arguments.

    Parameters
    ----------
    ctx : Any
        The Discord API context for the bot.

    *args : [Any]
        The arguments to be used as query in the handler.
        It is expected to be one of: movie title, actor name, director name or IMDb code.'''

    term = ' '.join(args).lower()

    if len(term) <= 3:
        await ctx.send('This term seems very short :thinking:\n'
                       'How about searching with a longer name or IMDb code?')
    else:
        movie_handler = MovieHandler(base_url=settings['thirdPartyApiBaseUrl'])
        api_result = movie_handler.search_movies(term=term)

        if api_result.get_status_code() != 200:
            await ctx.send(api_result.get_error_message())
        elif api_result.get_status_code() == 200 and len(api_result.get_response()) == 0:
            await ctx.send("Sorry. I couldn't find any movie with that name/IMDb code :confused:")
        else:
            embeds = __build_search_command_embeds(
                movies=api_result.get_response())

            for embed in embeds[:10]:
                await ctx.send(embed=embed)
                __delay(seconds=1)

            await ctx.send("That's all :popcorn:")


def run() -> None:
    '''Simply runs the bot.
    This function should be called in the "main.py" file.'''

    bot.run(token=settings['token'])


def __build_search_command_embeds(movies: List[Movie]) -> List[discord.Embed]:
    embeds: List[discord.Embed] = []

    for movie in movies:
        description = f'**IMDb Rating**: {movie["imdb_rating"]} | **Runtime**: {movie["runtime"]}'
        green_hex_code = 0x008000

        embed = discord.Embed(
            title=f'{movie["title"]}',
            url=f'{movie["url"]}',
            description=description,
            color=green_hex_code
        )

        embed.set_thumbnail(url=movie['poster_url'])

        for movie_file in movie['files']:
            value = f'**Quality**: {movie_file["quality"]}'\
                f' | **Type**: {movie_file["type"]}'\
                f' | **Seeds**/**Peers**: {movie_file["seeds"]}/{movie_file["peers"]}'\
                f' | **Size**: {movie_file["size"]} '

            embed.add_field(
                name=movie_file['file_url'], value=value, inline=False)

        embeds.append(embed)
    return embeds


def __build_help_command_embed() -> discord.Embed:
    coral_hex_code = 0xFF7F50

    embed = discord.Embed(
        title='Commands',
        description="These are all the commands I can run :point_down:",
        color=coral_hex_code
    )

    embed.add_field(
        name='?ping',
        value='Shows the current latency of the BOT.',
        inline=False
    )

    embed.add_field(
        name='?search <movie_name> | <imdb_code>',
        value='Lists movie occurences based on the given name or IMDb code (max 10).',
        inline=False
    )

    return embed


def __delay(seconds: float) -> None:
    time.sleep(seconds)
