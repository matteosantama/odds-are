from datetime import datetime
import hashlib


class Match(object):


    def __init__(self, home_team, away_team, home_odds, away_odds,
                hodds_site, aodds_site, time = None):
        # constructor expects a date object for the time
        sanitized_home = home_team.title().strip()
        sanitized_away = away_team.title().strip()
        self.home_team = sanitized_home
        self.away_team = sanitized_away
        self.home_odds = int(home_odds)
        self.away_odds = int(away_odds)
        self.hodds_site = hodds_site
        self.aodds_site = aodds_site
        self.game_time = time
        self.key = self.create_key(sanitized_home, sanitized_away)


    def __str__(self):
        if self.game_time is not None:
            pdate = self.game_time.strftime('%-m/%-d %-I:%M%p')
            return_str = '%s (%s) is playing at %s (%s) on %s'
            return return_str % (self.away_team, self.away_odds, self.home_team, self.home_odds, pdate)
        else:
            return_str = '%s (%s) is playing at %s (%s)'
            return return_str % (self.away_team, self.away_odds, self.home_team, self.home_odds)


    def __eq__(self, obj):
        return instance(obj, Match) and obj.key == self.key


    def create_key(self, home, away):
        # the key created by this function only depends on the two
        # teams playing, so it is only guaranteed unqiue in a given week
        byts = (home + away).encode()
        hash = hashlib.md5(byts)
        return hash.hexdigest()
