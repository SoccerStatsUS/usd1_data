#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Scaryice lineups only.


# Need to reformat the text dramatically so I canclean up this code.

# Need to redo a bunch of DC United Goal entries from around 2003 and 2004.  Format is Adu (34;85), which is not useable...

# Load data from scaryice's lineup files.

# Lineup errors!

# (u'Kansas City Wizards', datetime.datetime(1998, 4, 8, 0, 0)) parsing double sub wrong.
# (u'Kansas City Wizards', datetime.datetime(2002, 8, 28, 0, 0))
# (u'Kansas City Wizards', datetime.datetime(2007, 4, 18, 0, 0))
# (u'Los Angeles Galaxy', datetime.datetime(1996, 5, 5, 0, 0)) parsing double sub wrong.

# (u'Los Angeles Galaxy', datetime.datetime(2007, 8, 18, 0, 0)) # parsing double sub wrong.
# (u'Los Angeles Galaxy', datetime.datetime(2010, 7, 4, 0, 0)) [own goal] probably just give up on these?
# (u'FC Dallas', datetime.datetime(1996, 10, 2, 0, 0)) Gerell Elliot
# (u'FC Dallas', datetime.datetime(2002, 9, 1, 0, 0)) [formatting]
# (u'FC Dallas', datetime.datetime(2004, 7, 20, 0, 0)) u'Ronnie O\u2019Brien
# (u'FC Dallas', datetime.datetime(2007, 10, 3, 0, 0)) # parsing double sub wrong.
# (u'Chicago Fire', datetime.datetime(2001, 8, 29, 0, 0)) parsing double sub wrong.
# (u'D.C. United', datetime.datetime(2005, 9, 22, 0, 0)) u'Christian G\xf3mez
# (u'D.C. United', datetime.datetime(2007, 2, 21, 0, 0)) No sub times.
# (u'Columbus Crew', datetime.datetime(1996, 8, 10, 0, 0)) parsing double sub wrong.
# (u'New England Revolution', datetime.datetime(2009, 7, 15, 0, 0)) Janauskas missing!
# (u'Miami Fusion', datetime.datetime(2000, 7, 25, 0, 0)) parsing triple sub wrong.
# (u'Houston Dynamo', datetime.datetime(2010, 7, 21, 0, 0)) parsing double sub wrong.
# (u'New York Red Bulls', datetime.datetime(2000, 8, 6, 0, 0)) parsing double sub wrong.
# (u'Tampa Bay Mutiny', datetime.datetime(1996, 9, 7, 0, 0)) # subs formatted wrong.
# (u'Tampa Bay Mutiny', datetime.datetime(1999, 6, 30, 0, 0)) parsing double sub wrong.
# (u'Colorado Rapids', datetime.datetime(1996, 7, 7, 0, 0)) u'Scott enedetti






from collections import defaultdict
import datetime
import os
import re
import sys




get_date = lambda s: datetime.datetime.strptime (s, "%Y-%m-%d")

LINEUPS_DIR = "/home/chris/www/soccerdata/data/games/domestic/country/usa/mls"


# scaryice specific team mappings.
team_map = {
    # these should not be here.
    'Chicago': 'Chicago Fire',
    'Colorado': 'Colorado Rapids',
    'Columbus': 'Columbus Crew',

    'Dallas': 'FC Dallas',
    'Houston': 'Houston Dynamo',
    'Kansas City': 'Kansas City Wizards',
    'Tampa Bay': 'Tampa Bay Mutiny',
    'Toronto': 'Toronto FC',
    'Miami': 'Miami Fusion',
    'New England': 'New England Revolution',
    'New York': 'New York Red Bulls',
    'Philadelphia': 'Philadelphia Union',
    'San Jose': 'San Jose Earthquakes',
    'Seattle': 'Seattle Sounders',
    'Portland': 'Portland Timbers',
    'Los Angeles': 'Los Angeles Galaxy',
    'Salt Lake': 'Real Salt Lake',    


    'Richmond': 'Richmond Kickers',
    'Montreal': 'Montreal Impact',
    'CP Baltimore': 'Crystal Palace Baltimore',
    'Harrisburg': 'Harrisburg City Islanders',
    'Stanislaus Utd': 'Stanislaus United Cruisers',
    'Hampton Roads': 'Virginia Beach Mariners',
    'Mid Michigan': 'Michigan Bucks',
    'Fresno': 'Fresno Fuego',
    'Western Mass': 'Western Mass Pioneers',
    'Wilmington': 'Wilmington Hammerheads',
    'Long Island': 'Long Island Rough Riders',
    'Hershey': 'Hershey Wildcats',
    'Virginia Beach': 'Virginia Beach Mariners',
    'Charleston': 'Charleston Battery',
    'Ocean City': 'Ocean City Barons',
    

    'Jacksonville': 'Jacksonville Cyclones',
    'Central Coast': 'Central Coast Roadrunners',
    'Cleveland': 'Cleveland City Stars',
    'Tennessee': 'Tennessee',
    'Atlanta': 'Atlanta Silverbacks',
    'Carolina': 'Carolina Dynamo',
    'Charlotte': 'Charlotte Eagles',
    'New Jersey': 'New Jersey Stallions',
    'Milwaukee': 'Milwaukee Rampage',
    (2003, 'Milwaukee'): 'Milwaukee Wave United',
}
    

# file_mapping = {
#     "CHI": u'Chicago Fire',
#     "CHV": u'Chivas USA',
#     "COL": u'Colorado Rapids',
#     "CLB": u'Columbus Crew',
#     "DC": u'D.C. United',
#     "DAL": u'FC Dallas',
#     "HOU": u'Houston Dynamo',
#     "KC": u'Kansas City Wizards',
#     "LA": u'Los Angeles Galaxy',
#     "MIA": u'Miami Fusion',
#     "NE": u'New England Revolution',
#     "NY": u'New York Red Bulls',
#     "PHI": u'Philadelphia Union',
#     "RSL": u'Real Salt Lake',
#     "SJ": u'San Jose Earthquakes',
#     "SEA": u'Seattle Sounders',
#     "TB": u'Tampa Bay Mutiny',
#     "TOR": u'Toronto FC',
#     }    

file_mapping = {
    "CHI": 'Chicago Fire',
    "CHV": 'Chivas USA',
    "COL": 'Colorado Rapids',
    "CLB": 'Columbus Crew',
    "DC": 'D.C. United',
    "DAL": 'FC Dallas',
    "HOU": 'Houston Dynamo',
    "KC": 'Kansas City Wizards',
    "LA": 'Los Angeles Galaxy',
    "MIA": 'Miami Fusion',
    "NE": 'New England Revolution',
    "NY": 'New York Red Bulls',
    "PHI": 'Philadelphia Union',
    "RSL": 'Real Salt Lake',
    "SJ": 'San Jose Earthquakes',
    "SEA": 'Seattle Sounders',
    "TB": 'Tampa Bay Mutiny',
    "TOR": 'Toronto FC',
    }    

def get_competition(name):

    d = {
        'CAN': 'Canadian Championship',
        'C-Int': 'Copa Interamericana',
        'CC': 'CONCACAF Champions Cup',
        'CL': 'CONCACAF Champions League',
        'CM': 'Copa Merconorte',
        'CS': 'Copa Sudamericana',
        'CW': 'CONCACAF Cup Winners\' Cup',
        'GC': 'Giants Cup',
        'OC-': 'U.S. Open Cup',
        'P-': 'MLS Cup Playoffs',
        'SL': 'Super Liga',
        }

    for k, v in d.items():
        if name.startswith(k):
            return v

    if name in ('22/OC-QF', '23/OC-QF'):
        return 'Major League Soccer'

    else:
        int(name) # make sure this is an integer (representing a round).
        return 'Major League Soccer'

    
def make_lineup_dict():
    """
    Create a dict ampping team and date to lineups.
    """
    # For getting correct goal names.
    lineups = load_all_lineups_scaryice()
    d = {}
    for e in lineups:
        key = (e['team'], e['date'])
        if key in d:
            d[key].append(e['name'])
        else:
            d[key] = [e['name']]
    return d




def load_all_games_scaryice():
    l = []
    for key in file_mapping.keys():
        fn = "%s.csv" % key
        l.extend(get_scores(fn))

    return l
    


def load_all_goals_scaryice():
    l = []
    for key in file_mapping.keys():
        fn = "%s.csv" % key
        l.extend(get_goals(fn))

    lineups = make_lineup_dict()
    goals = correct_goal_names(l, lineups)
    return goals



def load_all_lineups_scaryice():
    l = []
    for key in file_mapping.keys():
        fn = "%s.csv" % key
        l.extend(get_lineups(fn))

    return l


# This needs to have a list of all lineups to work properly.
# Key should be of the form (goal['team'], goal['date'])
def correct_goal_names(goal_list, lineup_dict):
    """
    Try to map from Kirovski to Jovan Kirovski
    based on lineups.
    For scaryice goal data.
    """

    # Problems:
    # (u'Colorado Rapids', datetime.datetime(1996, 9, 15, 0, 0))
    # Actually a bunch more Rapids Sean/Chris Henderson issues.

    
    # Match goal names to lineup names.
    # These will both be repaired later.
    last_mapping = {
        'Allnutt': 'Allnut',
        'Saborío': 'Saborio',
        'O’Brien': 'O\'Brien',
        'O’Rourke': 'O\'Rourke',
        'Aguiliera': 'Aguilera',
        'Sawatsky': 'Sawatzky',
        'Peguero': 'Peguero Jean Philippe',
        'Peguero Jean Philippe': 'Peguero Jean Philippe',
        'DeRosario': 'De Rosario',
        'Ben-Dayan': 'Ben Dayan',
        #'Nunez': 'Núñez', # good for Ramon Nunez, not necessarily other nunezes.
        #'Sanchez': 'Sánchez',

        }
    # Simon Elliott/Elliot

    # Easiest way to handle this.
    name_mapping = {
        'Burciaga': 'Jose Burciaga',
        'Burciaga Jr.': 'Jose Burciaga',
        'Preki': 'Preki',
        'Zoltan': 'Zoltan Hercegfalvi',
        'Wondolowski': 'Chris Wondolowski', # Steve Wondolowski never scored.
        'J.P. Garcia': 'Juan Pablo Garcia',
        'Saborio': 'Alvaro Saborio',
        'Pineda Chacon': 'Alex Pineda Chacon',
        'Angel': 'Juan Pablo Angel',
        'Diaz Arce': 'Raul Diaz Arce',
        'Welton': 'Welton Melo',
        'Husidic': 'Baggio Husidic',
        'Saborío': 'Alvaro Saborio',
        'Machon': 'Martin Machon',
        }


    def get_match(key, first, last):
        """
        Uses a game key to try to retrieve a name from the lineup dict.
        """
        if last in last_mapping:
            last = last_mapping[last]

        players = lineup_dict[key]

        # Need to correct this in lineups, but can't figure out why it's persisting.
        # Remove when fixed.
        # Or alternatively could just do it when importing to main lineups?
        players = [e.strip() for e in players]

        matches = [e for e in players if e.startswith(first) and e.endswith(last)]

        if len(matches) == 0:

            # Interfering with other dicts below.
            no_matches = {
                'Gomez': 'Gómez',
                'Gutierrez': 'Gutiérrez',
                'Gonzalez': 'González',
                'Suarez': 'Suárez',
                'Landin': 'Landín',
                'Perez': 'Pérez',
                'Alvarez': 'Álvarez',
                'Chavez': 'Chávez',
                'Ruiz': 'Ruíz',
                'W Sánchez': 'Sanchez',
                'Elliot': 'Elliott',
                }

            if last in no_matches:
                return get_match(key, first, no_matches[last])

            if last == 'Own Goal':
                return last


            print("No matches for %s %s on key %s" % (first, last, key))
            return ''
        elif len(matches) > 1:
            # Gonna handle this later.
            #if set(matches) == set([u'Sean Henderson', u'Chris Henderson']):
            #    return 'Henderson'

            print("Too many matches for %s %s %s" % (first, last, matches))
            return ''
        else:
            return matches[0]
            
    l = []
    for goal in goal_list:
        key = (goal['team'], goal['date'])
        
        try:
            name = goal['goal']
        except:
            import pdb; pdb.set_trace()

        if name in name_mapping:
            real_name = name_mapping[name]

        else:
            if "," in name:
                last, first = name.split(",")
            elif '.' in name and not name.endswith('.'):
                try:
                    first, last = name.split('.')
                except:
                    import pdb; pdb.set_trace()
            else:
                first = ''
                last = name

            first = first.replace(".", '')

            real_name = get_match(key, first.strip(), last.strip())

        d = goal.copy()
        if real_name:
            d['goal'] = real_name
        l.append(d)

    return l
        


def get_scores(fn):
    """
    Get scores from scaryice's lineups table for a given file.
    """

    # OH NO! Make the scores work correctly.
    # huh?

    def process_line(line):
        if not line.strip():
            return {}

        if line.startswith('*'):
            return {}

        items = line.strip().split("\t")
        
        match_type, date_string, location, opponent, score, result, _, goals, lineups = items

        date = get_date(date_string)

        opponent = opponent.strip()
        t = (date.year, opponent)
        if t in team_map:
            print("Mapping opponent from %s to %s" % (opponent, team_map.get(t)))
            opponent = team_map.get(t)
        else:
            opponent = team_map.get(opponent, opponent)



        scores = [int(e) for e in score.split('-')]

        if result == 'D':
            team_score = opponent_score = scores[0]

        elif result == 'W':
            team_score = max(scores)
            opponent_score = min(scores)
            
        elif result == 'L':
            team_score = min(scores)
            opponent_score = max(scores)
        
        else:
            import pdb; pdb.set_trace()
        
        if location == 'H':
            home_team = team_name
            home_score = team_score
            away_team = opponent
            away_score = opponent_score
        elif location == 'A':
            away_team = team_name
            away_score = team_score
            home_team = opponent
            home_score = opponent_score
        elif location == 'N':
            # Not sure how to handle these.
            home_team = team_name
            home_score = opponent_score
            away_team = opponent
            away_score = team_score
        else:
            raise

        home_team = team_map.get(home_team, home_team)
        away_team = team_map.get(away_team, away_team)


        competition = get_competition(match_type)

        # Only use scaryice MLS regular season scores.
        # Everything else is too complicated / not good enough.

        if competition == 'Major League Soccer':
            return {
                'competition': competition,
                'date': date,
                #'season': unicode(date.year),
                'season': str(date.year),

                'team1': home_team,
                'team2': away_team,
                'team1_score': home_score,
                'team2_score': away_score,
                'home_team': home_team,
                'sources': ['MLS Lineup Database'],
                }
        else:
            return {}

    p = os.path.join(LINEUPS_DIR, fn)
         
    team_name = file_mapping[fn.replace(".csv", '')]
    scores = [process_line(line) for line in open(p).readlines()]

    return [e for e in scores if e]





def get_goals(filename):
    """
    Return goal data from a given file.
    """
    

    def process_line(line):
        pline = line.strip()

        if not pline:
            return []

        if pline.startswith('*'):
            return []

        items = pline.split("\t")
        match_type, date_string, location, opponent, score, result, _, goals, lineups = items
        date = get_date(date_string)

        def process_goal(e):
            e = e.strip()

            if not e:
                return {}

            competition = get_competition(match_type)
            if competition != 'Major League Soccer':
                return {}

            # Handle different goal formats.

            # e.g. Kosecki (Razov) 76; Kotschau (unassisted) 87'
            match = re.search("(?P<name>.*?)\s+(\d+\s+)?\(.*?\)\s+(?P<minute>\d+)", e)

            # Handle "Preki (3)" et al.
            # Currently handling "Preki (47+ pen) here, by lopping off \) from re.
            # should separate.
            if not match:
                match = re.search("(?P<name>.*?)\s+(\d+\s+)?\((?P<minute>\d+)", e)

            # Handle "Okafor 16" et al.
            if not match:
                match = re.search("(?P<name>.*?)\s+(\d+\s+)?(?P<minute>\d+)", e)


            # Need to work on own goal processing...
            # What's the deal with (forfeit?)
            non_goals = [
                #'Own Goal',
                #"o.g.",
                #'og',
                #'own goal',
                '(forfeit)',
                ]

            for ng in non_goals:
                if e.startswith(ng):
                    import pdb; pdb.set_trace()
                    return {}

            player = match.groups()[0]
            minute = int(match.groups()[2])

            player = player.strip()
            if player in [
                'Own Goal',
                'Own goal',
                "o.g.",
                'og',
                'own goal',
                ]:
                player = 'Own Goal'

            return {
                'competition': competition,
                'team': team_map.get(team_name, team_name),
                'date': date,
                #'season': unicode(date.year),
                'season': str(date.year),
                'goal': player.strip(),
                'minute': minute,
                'assists': []
                }


        l = [process_goal(e) for e in goals.split(';')]
        return [e for e in l if e]

    p = os.path.join(LINEUPS_DIR, filename)
    team_name = file_mapping[filename.replace(".csv", '')]

    l = []
    for line in open(p).readlines():
        l.extend(process_line(line))

    return l




def get_lineups(filename):

    def preprocess_line(lineup_text):
        """
        """

        # I should change these in the data.
        replacements = [
            ('Colin Clark (Herculez Gomez 46) Nicolas Hernandez (Roberto Brown 59)',
             'Colin Clark (Herculez Gomez 46), Nicolas Hernandez (Roberto Brown 59)'),
            ('Tom McManus (sent off 89 from bench) (Herculez Gomez 65)',
             'Tom McManus (Herculez Gomez 65)',),
            ('Ramiro Corrales (sent off 85th minute from bench) (Arturo Alvarez 62)',
             'Ramiro Corrales (Arturo Alvarez 62)'),

            # Bad game 2002-8-28
            ('Francisco Gómez (Chris Brown, m.62)', 'Francisco Gómez (Chris Brown 62)'),
            ('Igor Simutenkov (Davy Arnaud, m.46)', 'Igor Simutenkov (Davy Arnaud 46)'),
            ('Ronnie O’Brien (Bobby Rhine 80)', 'Ronnie O\'Brien (Bobby Rhine 80)'),
            ('Christian Gómez (John Wilson 61)', 'Christian Gomez (John Wilson 61)'), 
            ('Scott enedetti', 'Scott Benedetti'),
            ('Luciano Emilio (sent off 64 on bench) (Jaime Moreno 63)', 
             'Luciano Emilio (Jaime Moreno 63)'),
            ('Giuseppe Galderisi (subs: Nelson Vargas, Evans Wise)', 'Giuseppe Galderisi'),
            ('Jason Kreis (Note: Lubos Kubik sent off 74 from bench)', 'Jason Kreis'),
            ]

        s = lineup_text.strip()
        for src, dst in replacements:
            s = s.replace(src, dst)

            
        # Replace (John Wilson 80, Joe Vide 85) 
        # with easier to parse (John Wilson 80)(Joe Vide 85)
        paren_level = 0
        s2 = ''
        for char in s:
            if char == '(':
                paren_level += 1
            if char == ')':
                paren_level -= 1

            if paren_level > 0 and char == ',':
                s2 += ')('
            else:
                s2 += char

        return s2

            
    def process_line(line):
        pline = preprocess_line(line)
        if not pline:
            return []

        if pline.startswith('*'):
            return []

        def preprocess_lineups(lineups):
            r = [
                (';', ','), 
                (':', ','), 
                ('.', ''),
                ('(sent off after final whistle)', ''),
                ('sent off in shootout', ''),
                ('sent off during shootout', ''),
                ('(Note Lubos Kubik sent off 74 from bench)', ''),
                ('(Capt.)', ''),
                ('(Capt)', ''),
                ]

            s = lineups
            for src, dst in r:
                s = s.replace(src, dst)
            return s

        def process_lineups(l):
            competition = get_competition(match_type)
            return LineupProcessor(team_name, date, competition, goals_for, goals_against).consume_rows(l)
                
        items = pline.strip().split("\t")
        try:
            match_type, date_string, location, opponent, score, result, _, goals, lineups = items
        except:
            import pdb; pdb.set_trace()


        competition = get_competition(match_type)
        if competition != 'Major League Soccer':
            return []

        date = get_date(date_string)

        plineups = preprocess_lineups(lineups)
        # Produce starter/sub groups
        groups = [e for e in plineups.strip().split(",") if e]

        goals_for, goals_against = [int(e) for e in score.split('-')]

        return process_lineups(groups)
        

    p = os.path.join(LINEUPS_DIR, filename)
    t = file_mapping[filename.replace(".csv", '')]
    team_name = team_map.get(t, t)

    l = []
    for line in open(p).readlines():
        l.extend(process_line(line))

    return [e for e in l if e]




class LineupProcessor(object):
    """
    Fancy class to process lineups.
    """


    def __init__(self, team, date, competition, goals_for, goals_against):
        self.team = team
        self.date = date
        self.competition = competition
        self.goals_for = goals_for
        self.goals_against = goals_against

        self.lineups = []

        self.previous_row = ""

    def consume_row(self, row):
        # This is an item that has been split by a comma.
        # Fix the data!
        open_parens = row.count("(")
        closed_parens = row.count(")")

        if open_parens == 0 and closed_parens == 0:
            return [{
                'name': row.strip(),
                'on': 0,
                'off': 90,
                }]

        if open_parens == 1 and closed_parens == 0:
            self.previous_row = row
            text = ''

            
        elif open_parens == 0 and closed_parens == 1:
            text = self.previous_row + row


        else:
            text = row

        

        m = re.search("(.*?)\((.*?)(\d+'?)\s*\+?\??\)", text)
        if m:
            self.previous_row = ''
            starter, sub, minute = [e.strip() for e in m.groups()]
            return [{
                    'name': starter,
                    'on': 0,
                    'off': minute,
                    },
                    {
                    'name': sub,
                    'on': minute,
                    'off': 90,
                    }]

        m = re.search("(.*?)\((\d+)(.*?)\)", text)
        if m:
            self.previous_row = ''
            starter, minute, sub = [e.strip() for e in m.groups()]
            return [{
                    'name': starter,
                    'on': 0,
                    'off': minute,
                    },
                    {
                    'name': sub,
                    'on': minute,
                    'off': 90,
                    }]

        m = re.search("(.*?)\((.*?)\?\?\?\)", text)
        if m:
            self.previous_row = ''
            starter, sub = [e.strip() for e in m.groups()]
            return [{
                    'name': starter,
                    'on': 0,
                    'off': '?',
                    },
                    {
                    'name': sub,
                    'on': '?',
                    'off': 90,
                    }]

        m = re.search("(.*?)\((.*?)(\d+'?)\+?\)\s*\((.*?)(\d+)\+?\)", text)
        if m:
            starter, sub1, minute1, sub2, minute2 = [e.strip() for e in m.groups()]
            return [{
                    'name': starter,
                    'on': 0,
                    'off': minute1,
                    },
                    {
                    'name': sub1,
                    'on': minute1,
                    'off': minute2,
                    },
                    {
                    'name': sub2,
                    'on': minute2,
                    'off': 90,
                    }]

        
        m = re.search("(.*?)\((.*?)\)", text)
        if m:
            starter, sub = m.groups()
            return [{
                    'name': starter,
                    'on': 0,
                    'off': None,
                    },
                    {
                    'name': sub,
                    'on': None,
                    'off': 90,
                    }]

        
        import pdb; pdb.set_trace()
        x = 5
        print("failed to process %s " % text)
        return []

                


            
    def consume_rows(self, rows):
        l = []
        for i, row in enumerate(rows, start=1):
            lineups = self.consume_row(row)
            for lineup in lineups:
                lineup['name'] = lineup['name'].strip().replace(")(", "")
                lineup.update({
                    'team': team_map.get(self.team, self.team),
                    'date': self.date,
                    #'season': unicode(self.date.year),
                    'season': str(self.date.year),
                    'competition': self.competition,
                    'order': i,
                    'goals_for': self.goals_for,
                    'goals_against': self.goals_against,
                    })
            l.extend(lineups)
        return l
                        

if __name__ == "__main__":
    print(load_all_lineups_scaryice())

            
        
            


    

