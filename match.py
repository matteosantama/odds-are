from datetime import datetime

class Match(object):

    def __init__(self, home_team, away_team, home_odds, away_odds, hodds_site, aodds_site, time):
        # constructor expects a date object for the time
        self.home_team = home_team
        self.away_team = away_team
        self.home_odds = home_odds
        self.away_odds = away_odds 
        self.hodds_site = hodds_site
        self.aodds_site = aodds_site
        self.game_time = time


    def __str__(self):
        pdate = self.game_time.strftime('%-m/%-d %-I:%M%p')
        return '%s (%s) is playing at %s (%s) on %s' % (self.away_team, self.away_odds, self.home_team, self.home_odds, pdate)
