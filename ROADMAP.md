# ROADMAP.md — Development Roadmap

Open work only; completed items are removed as they land (see git history).

---

## MLS standings integrity

- [ ] **Goal columns are wrong for 2017 and 2019 in `data/standings/mls`.** Neither
  season balances: 2019 sums to 1222 GF vs 1226 GA, 2017 to 1110 vs 1112. Both
  blocks faithfully transcribe their `BlockSource:` Wikipedia tables, so the
  source itself is what's wrong. Cross-checked against
  `mlssoccer_data/parsed/mls.jsonl` (official MLS stats API), which balances
  exactly for every season 2017–2026.

  For 2019 the W/L/T columns agree everywhere — only goals are off, and only in
  the Western Conference. File → API:

      Seattle Sounders FC     GF 51 → 52
      Real Salt Lake          GF 45 → 46
      Minnesota United FC     GA 42 → 43
      LA Galaxy               56/55 → 58/59
      Portland Timbers        49/48 → 52/49
      FC Dallas               GF 48 → 54
      San Jose Earthquakes    51/52 → 52/55
      Colorado Rapids         57/60 → 58/63
      Houston Dynamo          45/57 → 49/59
      Vancouver Whitecaps FC  GA 58 → 59

  FC Dallas is the clearest: the API's 34 Dallas match scores sum to 54, not 48.
  For 2017 the API is missing one match (Vancouver–San Jose), so it can't
  arbitrate the whole season, but Chicago Fire (62/48 vs 61/47) and Real Salt
  Lake (48/56 vs 49/55) differ on matches it does have.

  Open questions: whether to override a block's stated `BlockSource:` with the
  API, and whether the same drift exists in seasons that happen to balance.

- [ ] **`data/standings/mls_reserve` has five unresolved arithmetic failures.**
  2008 Houston (26 points vs 3W+T = 29); 2011 New York Red Bulls (9 vs 8);
  2011 Sporting K.C. (GD −3 vs GF−GA +7); 2011 Vancouver (GD −5 vs −4);
  2012 FC Dallas (18 vs 19). Season totals don't balance for 2005, 2008, 2011
  or 2012. No source recorded for any of these blocks.

- [ ] **`Key:` persists across season blocks with no guard.** A block written in a
  different column order parses silently into the wrong fields — this is what
  put 2000 and 2001 into the database with losses and ties swapped.

## MLS game files

Lower priority than the standings above; noted while cross-checking.

- [ ] `data/games/mls/2011` includes 5/18/2011 Vancouver 1-1 Toronto, which is the
  Canadian Championship final first leg, not an MLS match. It gives both clubs
  35 games.
- [ ] `data/games/mls/2005` has roughly three results that contradict the
  (source-verified) standings. Derived records come out RSL 7-20-5 and Chivas
  5-21-6 against their actual 5-22-5 and 4-22-6, with Dallas and Colorado
  carrying the offsetting errors.
- [ ] `data/games/mls/2013` and `2014` carry `np` placeholder rows in the score
  field (three and five respectively).
- [ ] `data/games/mls/2015` through `2019` are substantially incomplete — 2017 has
  only a couple of matches per team.
- [ ] Team names in the game files aren't normalized the way the standings files
  are: `Sporting KC` alongside `Sporting Kansas City`, a `FC Dallsa` typo,
  stadium names sitting in a team column (`BBVA Stadium`, `Nippert Stadium`),
  and a mangled `Houston Dynamo: 2-1`.
