# ohtuvarasto

[![CI](https://github.com/akikleemola/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/akikleemola/ohtuvarasto/actions)

[![codecov](https://codecov.io/github/akikleemola/ohtuvarasto/graph/badge.svg?token=RYYRJY5QYH)](https://codecov.io/github/akikleemola/ohtuvarasto)


Yksinkertainen suomenkielinen Flask-verkkosovellus varastojen hallintaan.

## Riippuvuudet

Sovellus käyttää Pythonia ja projektin riippuvuudet hallitaan [uv](https://docs.astral.sh/uv/)-työkalulla.
Asenna riippuvuudet projektin juurihakemistossa:

```bash
uv sync
```

## Käynnistäminen

Käynnistä web-sovellus:

```bash
uv run python src/app.py
```

Avaa selaimessa osoite <http://127.0.0.1:5000>.

## Testaus

Aja kaikki testit:

```bash
uv run pytest
```
