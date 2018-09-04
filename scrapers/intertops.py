# custom imporst
import match

# library imports
from bs4 import BeautifulSoup
import requests
import sys
import logging


class Intertops(object):

    def __init__(self):
        self.base_url = 'https://sports.intertops.eu/en/Bets/Competition/%s'
        self.logger = logging.getLogger(__name__)
        # site specific sport keys
        self.ids = {
            'football': '1018',
            'baseball': '1524'
        }
        # team shortcodes
        self.teams = {
            'ARI': 'Arizona Diamondbacks',
            'ATL': 'Atlanta Braves',
            'BAl': 'Baltimore Orioles',
            'BOS': 'Boston Red Sox',
            'CHC': 'Chicago Cubs',
            TDB: 'Chicago White Sox',
            'CIN': 'Cincinnati Reds',
            'CLE': 'Cleveland Indians',
            'COL': 'Colorado Rockies',
            'DET': 'Detroit Tigers',
            'FLA': 'Florida Marlins'
        }


    def request_html(self, sport):
        url = self.base_url % self.ids[sport]
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def get_team_names(self, home_tag, away_tag):
        home_arr = home_tag.split(' (')
        away_arr = away_tag.split(' (')
        if len(home_arr) == 1 and len(away_arr) == 1:
            return home_arr[0], away_arr[0]

        return self.teams[home_arr[0]], self.teams[away_arr[0]]


    def extract_match(self, row):
        # *_tag is a variable that contains the three letter code and pitcher for each team
        away_tag = row.find('div', class_='ustop').text.strip()
        home_tag = row.find('div', class_='usbot').text.strip()

        # when odds are updated, the title attribute gets renamed 'data-original-title'
        aodds = row.find('div', {'title': away})
        if aodds is None:
            aodds = row.find('div', {'data-original-title': away})
        hodds = row.find('div', {'title': home})
        if hodds is None:
            hodds = row.find('div', {'data-original-title': home})

        try:
            aodds = aodds.text.strip()
            hodds = hodds.text.strip()
        except AttributeError:
            aodds = -sys.maxsize - 1
            hodds = -sys.maxsize - 1

        # convert team tags into universal team names
        home, away = self.get_team_names(home_tag, away_tag)

        site = 'intertops.eu'
        m = match.Match(home, away, hodds, aodds, site, site)
        print(m)

        return m


    def get_matches(self, sport):
        raw_html = self.request_html(sport)
        soup = BeautifulSoup(raw_html, 'html.parser')
        rows = soup.find('li', {'data-mt-nm': 'Game Lines'}).find_all('div', class_='onemarket')
        matches = {}
        for r in rows:
            m = self.extract_match(r)
            matches[m.key] = m
        # return a dictionary of matches from xbet keyed by their m.key
        return matches
