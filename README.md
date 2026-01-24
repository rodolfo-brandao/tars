# TARS

![MIT License](https://img.shields.io/github/license/rodolfo-brandao/tars)
![Python version](https://img.shields.io/badge/python-3.9.6-blue)

My own [Discord](https://discord.com/) bot, named after the sarcastic robot from Interstellar.

## Setup

### 1. Clone the Repository
```bash
$ git clone https://github.com/rodolfo-brandao/tars.git
```

### 2. Navigate to the Project Folder

```bash
$ cd tars
```

### 3. Install the Dependencies

The following packages are required in order to run this bot:

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://pypi.org/project/requests/)

These can be installed through `requirements.txt` file by running:

```bash
$ python3 -m pip install -r requirements.txt
```

### 4. Run
Finally, just run the bot with:

```bash
$ python3 src/main.py
```

## Commands
These are the available commands:

- [x] `?info`<br>Lists all bot commands and what they do.<br><br>
- [x] `?ping`<br>Shows the current bot latency in milliseconds.<br><br>
- [x] `?search <movie_title> | <imdb_code>`<br>Searches for movie occurences (max 10) based on the title or IMDb code.
