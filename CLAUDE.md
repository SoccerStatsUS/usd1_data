# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**usd1_data** is a flat-file soccer statistics database for United States Division 1 leagues, serving as the data backend for [soccerstats.us](http://www.soccerstats.us). Processing code lives in a separate repo: [soccerstatsus/parse](http://github.com/soccerstatsus/parse).

## Leagues Covered

- ALPF (American League of Professional Football, 1894)
- ASL (American Soccer League, 1921–1933)
- NASL (North American Soccer League, 1968–1984)
- MLS (Major League Soccer, 1996–present)
- Eastern Soccer League

## Architecture

There is no build system, package manager, or test suite. The repo is a combination of:

1. **`data/`** — Flat text files organized by data type and league, manually curated and committed via git. Subdirectories: `games/`, `standings/`, `rosters/`, `stats/`, `salaries/`, `transactions/`, `injury/`.
2. **`parse/`** — Python modules for parsing the data files. Key modules:
   - `mlsdb.py` — MLS game results, goals, lineups; includes team name mapping dictionaries
   - `lineupdb.py` — Detailed lineup/substitution parsing
   - `nasl.py` — NASL data processing with franchise mappings
   - `asl.py` — ASL data processing with historical team name normalization
3. **`settings.py`** — Host-dependent `ROOT_DIR` configuration (maps hostname to local soccer data path).

## Data File Format

All data files use a custom text format with metadata headers followed by delimited records.

**Game results** (`data/games/<league>/<year>`):
```
Competition: Major League Soccer
Season: 1996

04/06/1996; San Jose Earthquakes; 1-0; DC United; 31683
```
Fields: `date; home_team; score; away_team; attendance`

**Rosters** (`data/rosters/<league>/<year>`):
```
Team: Atlanta United
Key: name; number; position; roster_status; player_category; note
```

**Standings** (`data/standings/<league>`):
```
Key: position; team; games; wins; losses; ties; goals_for; goals_against; goal_difference; points
```

**Salaries** (`data/salaries/mls.csv`): Tab-delimited CSV with columns `year, team, last_name, first_name, position, base_salary, total_compensation`.

**Transactions** (`data/transactions/<league>/date/<year>`): Semicolon-delimited with `Key:` header.

**Injuries** (`data/injury/<league>/<year>`): `date; player; injury; timeline` followed by `Source:` lines.

## Key Conventions

- Team names vary historically; parsers maintain mapping dictionaries to normalize them (see `team_names` dicts in `parse/mlsdb.py`, `parse/nasl.py`, `parse/asl.py`).
- Data files use semicolons (`;`) as field delimiters, not commas (exception: `mls.csv` uses tabs).
- Metadata headers (`Competition:`, `Season:`, `Key:`, `Team:`, `BlockSource:`, `Source:`) appear at the top of data blocks.
- Python code is Python 2/3 compatible.
