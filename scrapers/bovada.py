# custom module imports
import match

# import library packages
from datetime import datetime as dt
import requests
import sys
import logging


class Bovada(object):

    def __init__(self):
        self.api_url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/%s/%s'
        self.logger = logging.getLogger(__name__)
        self.lgs = {
            'football': 'nfl',
            'baseball': 'mlb'
        }


    def request_json(self, sport):
        url = self.api_url % (sport, self.lgs[sport])
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.json()

    # isolate moneyline odds
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

        # handle various spellings and abbreviations
        if home == 'St. Louis Cardinals':
            home = 'Saint Louis Cardinals'
        if away == 'St. Louis Cardinals':
            away = 'Saint Louis Cardinals'

        # extract outcomes from moneyline block in json
        outcomes = self.get_outcomes(event['displayGroups'][0]['markets'])
        hodds = -sys.maxsize - 1
        aodds = -sys.maxsize - 1
        # update moneylines if they exist
        if outcomes is not None:
            for team in outcomes:
                # print(team)
                if team['description'] == home:
                    hodds = team['price']['american']
                if team['description'] == away:
                    aodds = team['price']['american']

        # bpth odds are pulled from bovada
        hodds_site = aodds_site = 'bovada.lv'
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
            if ev['type'] == 'GAMEEVENT':
                m = self.extract_match(ev)
                matches[m.key] = m

        return matches
