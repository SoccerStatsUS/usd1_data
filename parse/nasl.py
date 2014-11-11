# Process game data for the original NASL.
# Need to simplify, export, and remove this.

import datetime
import os
import re

from utils import get_id

from usd1_data.settings import ROOT_DIR

nasl_games_filename = os.path.join(ROOT_DIR, 'usd1_data/data/games/league/jose/nasl')
nasl0_games_filename = os.path.join(ROOT_DIR, 'usd1_data/data/games/league/jose/npsl')

NASL_ROSTERS_DIR = os.path.join(ROOT_DIR, 'usd1_data/data/rosters/nasl')
NASL_STATS_DIR = os.path.join(ROOT_DIR, 'soccerdata/data/stats/d2')

# Merge into alias.
foreign_map = {
    'Varzim': 'Varzim S.C.',
    'varzim': 'Varzim S.C.',
    'Hertha': 'Hertha BSC',
    'hertha': 'Hertha BSC',
    'Bangu': 'Bangu AC',
    'bangu': 'Bangu AC',
    'apollon': 'Apollon Limassol',
    'Apollon': 'Apollon Limassol',
    'lanerossi': 'Vicenza Calcio',
    'Lanerossi': 'Vicenza Calcio',
    'Monterrey': 'CF Monterrey',
    'Vera Cruz': 'Veracruz',
    'Coventry': 'Coventry City FC',
    'hapoel': 'Hapoel Tel Aviv F.C.',
    'Hapoel': 'Hapoel Tel Aviv F.C.',
    'Hearts': 'Heart of Midlothian F.C.',
}


# These should take place in normalize.
# Not in this part at all.
simple_map = {
    'Baltimore': 'Baltimore Bays',
    'Calgary': 'Calgary Boomers',
    'California': 'California Surf',
    'Cleveland': 'Cleveland Stokers',
    'Dallas': 'Dallas Tornado',
    'Edmonton': 'Edmonton Drillers',
    'Golden Bay': 'Golden Bay Earthquakes',
    'Kansas City': 'Kansas City Spurs',
    'Tampa Bay': 'Tampa Bay Rowdies',
    'Seattle': 'Seattle Sounders',
    'Portland': 'Portland Timbers',
    'Rochester': 'Rochester Lancers',
    'Jacksonville': 'Jacksonville Tea Men',
    'Tulsa': 'Tulsa Roughnecks',
    'Fort Lauderdale': 'Fort Lauderdale Strikers',

    'Hartford': 'Hartford Bicentennials',
    'Connecticut': 'Connecticut Bicentennials',
    'Colorado': 'Colorado Caribous',
    'San Jose': 'San Jose Earthquakes',
    'Team America': 'Team America',
    'St. Louis': 'St. Louis Stars',
    'Las Vegas': 'Las Vegas Quicksilvers',
    'New England': 'New England Tea Men',
    'San Antonio': 'San Antonio Thunder',
    'Denver': 'Denver Dynamos',
    'Team Hawaii': 'Team Hawaii',
    
    
}




# Map of ambiguous names, these apply to multiple teams, but
# should be preempted by the season_map.
ambig_map = {
    'Boston': 'Boston Minutemen',
    'Detroit': 'Detroit Express',
    'Houston': 'Houston Hurricane',
    'Los Angeles': 'Los Angeles Aztecs',
    'New York': 'New York Cosmos',
    'Toronto': 'Toronto Blizzard',
    'Vancouver': 'Vancouver Whitecaps',
    'Washington': 'Washington Diplomats',
    'San Diego': 'San Diego Sockers',
    'Chicago': 'Chicago Sting',
    'Montreal': 'Montreal Manic',
    'Memphis': 'Memphis Rogues',
    'Minnesota': 'Minnesota Kicks',
    'Miami': 'Miami Toros',
    'Philadelphia': 'Philadelphia Atoms',
    'Atlanta': 'Atlanta Chiefs',
    }
simple_map.update(ambig_map)



season_map = {
    (1967, 'Chicago'): 'Chicago Spurs',
    (1967, 'Los Angeles'): 'Los Angeles Toros',
    (1967, 'New York'): 'New York Generals',
    (1967, 'Oakland'): 'Oakland Clippers',
    (1967, 'Philadelphia'): 'Philadelphia Spartans',
    (1967, 'Pittsburgh'): 'Pittsburgh Phantoms',
    (1967, 'Toronto'): 'Toronto Falcons',
    (1968, 'Chicago'): 'Chicago Mustangs',
    (1968, 'Boston'): 'Boston Beacons',
    (1968, 'Detroit'): 'Detroit Cougars',
    (1968, 'Houston'): 'Houston Stars',
    (1968, 'Los Angeles'): 'Los Angeles Wolves',
    (1968, 'New York'): 'New York Generals',
    (1968, 'Oakland'): 'Oakland Clippers',
    (1968, 'San Diego'): 'San Diego Toros',
    (1968, 'Atlanta'): 'Atlanta Chiefs',
    (1968, 'Toronto'): 'Toronto Falcons',
    (1968, 'Vancouver'): 'Vancouver Royals',
    (1968, 'Washington'): 'Washington Whips',
    (1969, 'Atlanta'): 'Atlanta Chiefs',
    (1970, 'Atlanta'): 'Atlanta Chiefs',
    (1970, 'Washington'): 'Washington Darts',
    (1971, 'Washington'): 'Washington Darts',
    (1971, 'Atlanta'): 'Atlanta Chiefs',
    (1972, 'Miami'): 'Miami Gatos',
    (1972, 'Atlanta'): 'Atlanta Chiefs',
    (1974, 'Baltimore'): 'Baltimore Comets',
    (1975, 'Baltimore'): 'Baltimore Comets',
    (1976, 'San Diego'): 'San Diego Jaws',

    (1971, 'Montreal'): 'Montreal Olympique',
    (1972, 'Montreal'): 'Montreal Olympique',
    (1973, 'Montreal'): 'Montreal Olympique',
    (1978, 'Oakland'): 'Oakland Stompers',
    (1978, 'Philadelphia'): 'Philadelphia Fury',
    (1979, 'Philadelphia'): 'Philadelphia Fury',
    (1980, 'Philadelphia'): 'Philadelphia Fury',
    (1981, 'Washington'): 'Washington Diplomats',
    (1984, 'Minnesota'): 'Minnesota Strikers',
    }


# Put this in competition aliases?
competition_map = {
    'NASL': ('North American Soccer League', None),
    'NASL Playoffs': ('North American Soccer League', 'Playoffs'),
    'USA': ('United Soccer Association', None),
    'NPSL': ('National Professional Soccer League', None),
    'NPSL Playoffs': ('National Professional Soccer League', 'Playoffs'),
    }


def load_rosters():
    # For converting Colin Jose name abbreviations into actual names.
    d = {}
    season = None

    f = open(NASL_ROSTERS_DIR)
    for line in f:
        if not line.strip():
            continue

        if line.startswith('Competition'):
            continue

        if line.startswith('Season:'):
            season = line.split("Season:")[1].strip()
        elif line.startswith("*"):
            pass
        else:
            team, players = line.split(':')
            player_list = [e.strip() for e in players.split(',')]
            d[(season, team)] = player_list

    return d


def player_from_abbreviation(code, roster):
    mapping = 'abcdefghijklmnopqrstuvwxyz1234'
    i = mapping.find(code)
    return roster[i]


# This is for the New NASL!!!
# This should be split off into a separate file!!!
def process_stats():
    """
    Process modern NASL stats taken from nasl.com
    """



    lst = []
    for fn in ('2011', '2012'):
        p = os.path.join(NASL_STATS_DIR, fn)
        f = open(p)
        for line in f:

            fields = line.split("  ") # 2 spaces
            fields = [e.strip() for e in fields if e.strip()]

            if fn == '2011':
                name, team, goals, assists, shots, yc, rc, minutes = fields
                sog = None
            else:
                try:
                    name, team, goals, assists, shots, sog, yc, rc, minutes = fields
                except:
                    print(line)
                    continue

                sog = int(sog)

            name = name.split(")")[1].strip()
            lst.append({
                    'competition': "North American Soccer League (2011-)",
                    'season': fn,
                    'name': name,
                    'team': team,
                    'position': '',
                    'goals': int(goals),
                    'assists': int(assists),
                    'shots': int(shots),
                    'shots_on_goal': sog,
                    'yellow_cards': int(yc),
                    'red_cards': int(rc),
                    'minutes': int(minutes),
                    })
                
    return lst


def get_full_name(name, season):
    """
    Figure out the full team name based on the season.
    """
    if name in foreign_map:
        return foreign_map[name]

    # For teams with unambiguous names (e.g. Dallas, San Jose, Golden Bay.
    key = (int(season), name)
    if key in season_map:
        return season_map[key]

    if name in simple_map:
        return simple_map[name]

        
    print("(NASL) failed to get name for %s" % name)
    return name
    

def process_nasl_games():
    return process_games(nasl_games_filename, ';')[0]

def process_nasl_goals():
    return process_games(nasl_games_filename, ';')[1]

def process_nasl_lineups():
    return process_games(nasl_games_filename, ';')[2]

def process_npsl_games():
    return process_games(nasl0_games_filename, ';')[0]

def process_npsl_goals():
    return process_games(nasl0_games_filename, ';')[1]



def process_games(fn, delimiter):
    f = open(fn)
    
    game_list = []
    goal_list = []
    appearance_list = []
    gp = GameProcessor(delimiter)
    for line in f:
        g = gp.consume_row(line)
        if g:
            game_data, goals, appearances = g
            game_list.append(game_data)
            goal_list.extend(goals)
            appearance_list.extend(appearances)
    return game_list, goal_list, appearance_list



class GameProcessor(object):
    def __init__(self, delimiter):
        self.year = None
        self.month = None
        self.day = None

        self.delimiter = delimiter

        self.rosters = load_rosters()


    def consume_row(self, row):
        fields = row.split(self.delimiter)

        if len(fields) == 11:
            competition, season, team, month, day, opponent, location, score, flags, goals, attendance = [e.strip() for e in fields]
            players = []
        elif len(fields) == 12:
            competition, season, team, month, day, opponent, location, score, flags, goals, attendance, players = [e.strip() for e in fields]
        else:
            import pdb; pdb.set_trace()

        # Skipping minigame for now.
        if day in ('M', 'SO', 'OT', 'SO-M'):
            return {}

        # Not played.
        if score == 'np':
            return {}
  
        # Process day before month.
        if day.strip():
            try:
                day = int(day)
            except:
                import pdb; pdb.set_trace()

            # Adjust month if we fall into a new month.
            if self.day is not None:
                if day < self.day:
                    self.month += 1

            self.day = day

        if month.strip():
            self.month = int(month)

        self.year = int(season)

        try:
            d = datetime.datetime(self.year, self.month, self.day)
        except:
            import pdb; pdb.set_trace()

        team_score,  opponent_score = [int(e) for e in score.split(',')]

        competition, stage = competition_map[competition]

        team = get_full_name(team, season)
        opponent = get_full_name(opponent, season)
            
        if location == 'h':
            home_team = team
            home_score = team_score
            away_team = opponent
            away_score = opponent_score
        else:
            home_team = opponent
            home_score = opponent_score
            away_team = team
            away_score = team_score

        if not attendance.strip():
            attendance = None
        else:
            try:
                attendance = int(attendance)
            except:
                import pdb; pdb.set_trace()


        shootout_winner = None
        if flags.strip() == '*':
            if home_score > away_score:
                shootout_winner = home_team
            elif home_score < away_score:
                shootout_winner = away_team
            else:
                import pdb; pdb.set_trace()

            home_score = away_score = min(home_score, away_score)

        gid = get_id()

        game_data = {
            'gid': gid,
            'competition': competition,
            'stage': stage,
            'season': season,
            'date': d,
            'team1': home_team,
            'team2': away_team,
            'team1_score': home_score,
            'team2_score': away_score,
            'home_team': home_team,
            'attendance': attendance,
            'shootout_winner': shootout_winner,
            'source': 'NASL - A Complete Record of the North American Soccer League',

            }

        goal_list = []


        for goal in goals.split(','):
            m = re.match("(.*?) (\d)", goal)
            if m:
                goal, count = m.groups()
                count = int(count)
            elif goal.strip():
                count = 1
            else:
                # Empty results.
                count = 0


            for e in range(count):
                goal_list.append({
                        'gid': gid,
                        'team': team,
                        'season': season,
                        'competition': competition,
                        'date': d,
                        'goal': goal,
                        'minute': None,
                        'assists': []
                        })

        appearance_list = []

        if '*' in players:
            off = None
        else:
            off = 90


        # No duplicates
        #if len(players) != len(set(players)):
        #    import pdb; pdb.set_trace()

        for appearance_code in players:
            if appearance_code == '*':
                appearance_list[-1]['on'] = None
            else:
                roster = self.rosters[(season, team)]
                try:
                    name = player_from_abbreviation(appearance_code, roster)
                except:
                    print(season, team)
                    print(d)
                    print(appearance_code)
                    raise

                appearance_list.append({
                        'gid': gid,
                        'name': name,
                        'on': 0,
                        'off': off,
                        'team': team,
                        'competition': competition,
                        'date': d,
                        'season': season,
                        #'goals_for': goals_for,
                        #'goals_against': goals_against,
                        #'order': None,
                        })
            

        return game_data, goal_list, appearance_list



if __name__ == "__main__":
    print(process_games())
