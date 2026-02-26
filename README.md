# TARS

[![License: MIT](https://img.shields.io/badge/License-MIT-white.svg)](https://github.com/rodolfo-brandao/tars/blob/main/LICENSE)
![Python version](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
[![Pylint](https://github.com/rodolfo-brandao/tars/actions/workflows/pylint.yml/badge.svg)](https://github.com/rodolfo-brandao/cinematica/actions/workflows/pylint.yml)
![Last GitHub commit](https://img.shields.io/github/last-commit/rodolfo-brandao/tars?logo=git&logoColor=red&color=red)

My own [Discord](https://discord.com/) bot, named after the sarcastic robot from Interstellar.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/rodolfo-brandao/tars.git
```

```bash
cd tars
```

2. Create `.venv` and install dependencies:
```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
pip freeze > requirements.txt
```

3. Run the bot (.venv):
```bash
python -m src.main
```

## Commands

- [x] `?info`<br>Lists all bot commands and what they do.<br><br>
- [x] `?ping`<br>Shows the current bot latency in milliseconds.<br><br>
- [x] `?search <movie_title> | <imdb_code>`<br>Searches for movie occurrences (max 10) based on the title or IMDb code.
