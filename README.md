# TARS

![License: MIT](https://img.shields.io/badge/License-MIT-3DA639?logo=opensourceinitiative&logoColor=white)
![Python version](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![uv version](https://img.shields.io/badge/uv-0.11.16-DE5FE9?logo=uv&logoColor=white)
[![Pylint](https://github.com/rodolfo-brandao/tars/actions/workflows/pylint.yml/badge.svg)](https://github.com/rodolfo-brandao/cinematica/actions/workflows/pylint.yml)

My own [Discord](https://discord.com/) bot, named after the sarcastic robot from Interstellar, made for me and my friends to help us discover movies online.

## Initial Setup

### Requirements

- [Python 3.14](https://www.python.org/downloads/release/python-3140/)
- [uv](https://docs.astral.sh/uv/)

### Setup

1. Clone this repository & navigate to its root folder:
```bash
git clone https://github.com/rodolfo-brandao/tars.git && \
cd tars
```

2. Create `.venv` & activate it:
```bash
uv venv .venv && \
source .venv/bin/activate
```

3. Install all dependencies in the current `.venv`:
```bash
uv sync
```

4. Run the bot:
```bash
python -m src.main
```

## Commands

- [x] `?info`<br>Lists all bot commands and what they do.<br><br>
- [x] `?ping`<br>Shows the current bot latency (ms).<br><br>
- [x] `?search <movie_title> | <imdb_code>`<br>Searches for movie occurrences (max 10) based on the given title or IMDb code (`tt` --prefixed string).
