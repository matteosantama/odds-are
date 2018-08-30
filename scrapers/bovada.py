# custom module imports
import match

# import library packages
from datetime import datetime as dt
import requests


# global variables
league_to_sport = {
    'nfl': 'football',
    'nba': 'basketball',
    'mlb': 'baseball'
}


class Bovada(object):

    def __init__(self):
        self.api_url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/%s/%s'

    def request_json(self, league):
        url = self.api_url % (league_to_sport[league], league)
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException:
            print 'Error attempting to contact %s' % r.url
            print 'Exiting...'
            sys.exit(1)

        return r.json()


    def parse_json(self, data):
        matches = []
        for event in data:
            # parse home and away teams
            competitors = event['competitors']
            home = competitors[0]['name'] if competitors[0]['home'] else competitors[1]['name']
            away = competitors[1]['name'] if competitors[0]['home'] else competitors[1]['name']
            # pick out odds in american format
            outcomes = event['displayGroups'][0]['markets'][1]['outcomes']
            if home is outcomes[0]['description']:
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
            matches.append(m)

        return matches


    def get_matches(self, sport):
        json = self.request_json(sport)
        # isolate the useful part of the json response
        events = json[0]['events']
        # parse the json and construct a list of upcoming Match objects
        upcoming = self.parse_json(events)
        return upcoming
