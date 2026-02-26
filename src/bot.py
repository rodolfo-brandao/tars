"""
The bot itself. This module is responsible for centralizing all events
and commands, besides of communicating with the API handler.
"""


import os
import time
from typing import List, Optional
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context
from src.models import Movie
from src.handler import search_movies


load_dotenv()
DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready() -> None:
    """
    Logs when the bot is running.
    """

    print(f"{bot.user} is running!")


@bot.command(help="Shows the bot latency.")
async def ping(ctx: Context) -> None:
    """
    Sends a message with the bot's current latency in milliseconds.

    :param ctx: Represents the context in which a command is being invoked under.
    :type ctx: Context
    """

    await ctx.send(f"Pong! :ping_pong:\nThe current latency is {round(bot.latency * 1000)}ms")


@bot.command(name="info", help="Custom helper command to display all available commands.")
async def display_commands(ctx: Context) -> None:
    """
    Sends a message showing all the bot's available commands.

    :param ctx: Represents the context in which a command is being invoked under.
    :type ctx: Context
    """

    await ctx.send(embed=_build_info_embed())


@bot.command(name="search", help="Searches for movie occurrences.")
async def search_movies_command(ctx: Context, *args) -> None:
    """
    Searches for movie occurrences based on the given arguments.

    :param ctx: Represents the context in which a command is being invoked under.
    :type ctx: Context

    :param *args: The arguments to be used as query in the handler,
    such as movie title or IMDb code.
    :type *args: Any
    """

    term = " ".join(args).lower()

    if len(term) <= 3:
        await ctx.send("This term seems too short :thinking:\n"
                       "How about searching using an IMDb code or a longer movie title?")
    else:
        api_result = search_movies(term=term)

        if api_result.status_code != 200:
            await ctx.send(api_result.error_message)
        elif api_result.status_code == 200 and not api_result.response:
            await ctx.send(
                content="Sorry. I couldn't find any movie with that title or IMDb code :confused:"
            )
        else:
            embeds = _build_search_embeds(movies=api_result.response)  # type: ignore
            for embed in embeds[:10]:
                await ctx.send(embed=embed)
                time.sleep(1)

            await ctx.send("That's all :popcorn:")


def run() -> None:
    """
    Simply runs the bot.
    This function should be called in the `main.py` file.
    """

    bot.run(token=DISCORD_TOKEN or "")


def _build_search_embeds(movies: List[Movie]) -> List[discord.Embed]:
    """
    Builds the discord embed objects for the `?search` command.

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


def _build_info_embed() -> discord.Embed:
    """
    Builds the discord embed object for the `?info` command.

    :return: A single discord embed object.
    :rtype: Embed
    """

    embed = discord.Embed(
        title="Commands",
        description="These are all the commands I can run :point_down:",
        color=0xFF7F50  # coral
    )

    embed.add_field(
        name="?ping",
        value="Shows the current latency of the BOT.",
        inline=False
    )

    embed.add_field(
        name="?search <movie_title> | <imdb_code>",
        value="Searches for movie occurrences (max 10) based on the given title or IMDb code.",
        inline=False
    )

    return embed
