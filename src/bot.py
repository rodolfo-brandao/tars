"""The bot itself. This module is responsible for centralizing
all events and commands, besides of communicating with API handlers."""


import os
import time
import discord
from dotenv import load_dotenv
from typing import List, Optional
from discord.ext import commands
from discord.ext.commands import Context
from handler import MovieHandler, Movie


load_dotenv()
YTS_API_TOKEN: Optional[str] = os.getenv("YTS_API_TOKEN")
YTS_API_BASE_URL: Optional[str] = os.getenv("YTS_API_BASE_URL")


intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready() -> None:
    """
    Logs when the bot is running.
    """

    print(f'{bot.user} is running!')


@bot.command(help='Shows the bot latency.')
async def ping(ctx: Context) -> None:
    """
    Sends a message with the bot's current latency in milliseconds.

    :param ctx: Represents the context in which a command is being invoked under.
    :type ctx: Context
    """

    await ctx.send(f"Pong! :ping_pong:\nThe current latency is {round(bot.latency * 1000)}ms")


@bot.command(name='info', help="Custom helper command to display all avaliable commands.")
async def display_commands(ctx: Context) -> None:
    """
    Sends a message showing all the bot's avaliable commands.

    :param ctx: Represents the context in which a command is being invoked under.
    :type ctx: Context
    """

    await ctx.send(embed=build_helper_embed())


@bot.command(name='search', help='Searches for movie occurences.')
async def search_movies(ctx, *args) -> None:
    """
    Searchs for movie occurences based on the given arguments.

    :param ctx: Represents the context in which a command is being invoked under.
    :type ctx: Context

    :param *args: The arguments to be used as query in the handler, such as movie title or IMDb code.
    :type *args: Any
    """

    term = " ".join(args).lower()

    if len(term) <= 3:
        await ctx.send("This term seems too short :thinking:\n"
                       "How about searching using an IMDb code or a longer movie title?")
    else:
        movie_handler = MovieHandler(base_url=YTS_API_BASE_URL or "")
        api_result = movie_handler.search_movies(term=term)

        if api_result.status_code != 200:
            await ctx.send(api_result.error_message)
        elif api_result.status_code == 200 and len(api_result.response) == 0:
            await ctx.send("Sorry. I couldn't find any movie with that title or IMDb code :confused:")
        else:
            embeds = build_search_embeds(movies=api_result.response)

            for embed in embeds[:10]:
                await ctx.send(embed=embed)
                time.sleep(1)

            await ctx.send("That's all :popcorn:")


def run() -> None:
    """
    Simply runs the bot.
    This function should be called in the "main.py" file.
    """

    bot.run(token=YTS_API_TOKEN or "")


def build_search_embeds(movies: List[Movie]) -> List[discord.Embed]:
    """
    Builds the discord embed objects for the "search" command.

    :param movies: The list containing all movies found in the search.
    :type movies: List[Movie]

    :return: A list of discord embeds.
    :rtype: List[Embed]
    """

    embeds: List[discord.Embed] = []
    for movie in movies:
        embed = discord.Embed(
            title=movie.title.upper(),
            url=movie.url,
            description=None,
            color=0x008000  # green
        )

        embed.set_thumbnail(url=movie.poster_url)

        for movie_file in movie.files:
            embed.add_field(
                name=f"{movie_file.type.upper()} {movie_file.quality} ({movie_file.size})",
                value=f":link: [Download]({movie_file.url})",
                inline=False
            )

        embeds.append(embed)
    return embeds


def build_helper_embed() -> discord.Embed:
    """
    Builds the discord embed object for the "help" command.

    :return: A single discord embed object.
    :rtype: Embed
    """

    embed = discord.Embed(
        title='Commands',
        description="These are all the commands I can run :point_down:",
        color=0xFF7F50  # coral
    )

    embed.add_field(
        name='?ping',
        value='Shows the current latency of the BOT.',
        inline=False
    )

    embed.add_field(
        name='?search <movie_title> | <imdb_code>',
        value='Searches for movie occurences (max 10) based on the given title or IMDb code.',
        inline=False
    )

    return embed
