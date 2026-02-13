# United States Division 1 Soccer Data

Data repository for [soccerstats.us](http://www.soccerstats.us), an open source soccer statistics database and website.

## Leagues

- American League of Professional Football (1894)
- American Soccer League (1921–1933)
- Eastern Soccer League
- North American Soccer League (1968–1984)
- Major League Soccer (1996–)

## Data

Game results, standings, rosters, player statistics, salaries, transactions, and injury reports stored as flat text files under `data/`.

### Format Examples

**Games** (`data/games/<league>/<year>`):
```
Competition: Major League Soccer
Season: 1996

04/06/1996; San Jose Earthquakes; 1-0; DC United; 31683
```

**Rosters** (`data/rosters/<league>/<year>`):
```
Competition: Premier League
Season: 2008-2009

Team: Arsenal
Key: player

Manuel Almunia
Bacary Sagna
Kolo Toure
William Gallas
...
```

## Processing Code

Parsing and processing code is at [soccerstatsus/parse](http://github.com/soccerstatsus/parse).

## Contact

Email chris@soccerstats.us or [contact](http://www.soccerstats.us/contact)
