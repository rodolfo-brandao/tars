# TARS

![MIT License](https://img.shields.io/github/license/rodolfo-brandao/tars)
![Python version](https://img.shields.io/badge/python-3.9.6-blue)

## Overview
My own [Discord](https://discord.com/) bot, named after the sarcastic robot from the movie Interstellar, created to explore movies on the internet, in addition to allowing me to put my knowledge in Python into practice.

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

This bot requires 2 packages to run:

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [requests](https://pypi.org/project/requests/)

These can be installed through the `requirements.txt` file by running the following [pip](https://pip.pypa.io/en/stable/) command:

```bash
$ pip install -r requirements.txt
```

### 4. Run
After installing the packages, simply run the bot with:

```bash
$ python3 src/main.py
```

## Commands
The bot command prefix is the character `?`

- [x] `?info`<br>Lists all bot commands and what they do.<br><br>
- [x] `?ping`<br>Shows the current bot latency in milliseconds.<br><br>
- [x] `?search <movie_name> | <imdb_code>`<br>Searches for movie occurences based on the name or IMDb code.

#### Disclaimer
I have little knowledge about Python, the intention of creating a project like this was motivated by learning more about the language. So don't expect to find the best organization, patterns or conventions here.
