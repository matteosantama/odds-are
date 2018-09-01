# custom module imports
import match

# import library packages
from datetime import datetime as dt
import requests
import sys


# global variables
league_to_sport = {
    'nfl': 'football',
}


class Bovada(object):


    def __init__(self):
        self.api_url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/%s/%s'


    def request_json(self, league):
        url = self.api_url % (league_to_sport[league], league)
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print 'Error attempting to contact %s' % r.url
            print e
            print 'Exiting...'
            sys.exit(1)

        return r.json()


    def get_outcomes(self, markets):
        for m in markets:
            if m['description'] == 'Moneyline':
                return m['outcomes']
        return None


    def extract_match(self, event):
        # parse home and away teams
        competitors = event['competitors']
        home = competitors[0]['name'] if competitors[0]['home'] else competitors[1]['name']
        away = competitors[1]['name'] if competitors[0]['home'] else competitors[1]['name']

        # extract outcomes from moneyline block in json
        outcomes = self.get_outcomes(event['displayGroups'][0]['markets'])

        # handle the case where moneyline odds are not provided
        if len(outcomes) == 0:
            hodds = -sys.maxint - 1
            aodds = -sys.maxint - 1
        elif home is outcomes[0]['description']:
            hodds = outcomes[0]['price']['american']
            aodds = outcomes[1]['price']['american']
        else:
            aodds = outcomes[0]['price']['american']
            hodds = outcomes[1]['price']['american']

        # bpth odds are pulled from bovada
        hodds_site = aodds_site = 'bovada'
        # construct datetime object. divide by 1000 to fix time
        time = dt.fromtimestamp(event['startTime']/1000)
        m = match.Match(home, away, hodds, aodds, hodds_site, aodds_site, time)

        return m


    def get_matches(self, sport):
        json = self.request_json(sport)
        # isolate the useful part of the json response
        events = json[0]['events']
        matches = {}
        for ev in events:
            m = self.extract_match(ev)
            matches[m.key] = m

        return matches
