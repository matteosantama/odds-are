from datetime import datetime
import hashlib


class Match(object):


    def __init__(self, home_team, away_team, home_odds, away_odds,
                hodds_site, aodds_site, time):
        # constructor expects a date object for the time
        sanitized_home = home_team.title().strip()
        sanitized_away = away_team.title().strip()
        self.home_team = sanitized_home
        self.away_team = sanitized_away
        self.home_odds = 100 if home_odds == 'EVEN' else int(home_odds)
        self.away_odds = 100 if away_odds == 'EVEN' else int(away_odds)
        self.hodds_site = hodds_site
        self.aodds_site = aodds_site
        self.game_time = time
        self.key = self.create_key(sanitized_home, sanitized_away, time)


    def __str__(self):
        pdate = self.game_time.strftime('%-m/%-d %-I:%M%p')
        return_str = '%s %s (%s) on %s at %s (%s) on %s'
        return return_str % (pdate, self.away_team, self.away_odds, self.aodds_site, self.home_team, self.home_odds, self.hodds_site)


    def __eq__(self, obj):
        return instance(obj, Match) and obj.key == self.key


    def create_key(self, home, away, date):
        # the key is created by hashing the string
        # 'home team' + 'away team' + 'day' + 'month' + 'year'
        string = home + away + str(date.day) + str(date.month) + str(date.year)
        byts = (home + away).encode()
        hash = hashlib.md5(byts)
        return hash.hexdigest()
