# custom module imports
import match

# library imports
from bs4 import BeautifulSoup
import requests
import sys
import logging


class Xbet(object):

    def __init__(self):
        self.base_url = 'https://xbet.ag/sportsbook/%s/'
        self.logger = logging.getLogger(__name__)
        self.lgs = {
            'football': 'nfl',
            'baseball': 'mlb'
        }
        self.teams = {
            'sfo giants': 'San Francisco Giants',
            'col rockies': 'Colorado Rockies',
            'sdg padres': 'San Diego Padres',
            'ari diamondbacks': 'Arizona Diamonbacks',
            'ny mets': 'New York Mets',
            'la dodgers': 'Los Angeles Dodgers',
            'ny yankees': 'New York Yankees',
            'oak athletics': 'Oakland Athletics',
            'bal orioles': 'Baltimore Orioles',
            'sea mariners': 'Seattle Mariners',
            'was nationals': 'Washington National',
            'stl cardinals': 'Saint Louis Cardinals',
            'chi cubs': 'Chicago Cubs',
            'mil brewers': 'Milwaukee Brewers',
            'la angels': 'Los Angeles Angels',
            'tex rangers': 'Texas Rangers',
            'min twins': 'Minnesota Twins',
            'hou astros': 'Houston Astros',
            'chi white sox': 'Chicago White Sox',
            'det tigers': 'Detroit Tigers',
            'cle indians': 'Cleveland Indians',
            'tor blue jays': 'Toronto Blue Jays',
            'atl braves': 'Atlanta Braves',
            'cin reds': 'Cincinatti Reds',
            'bos red sox': 'Boston Red Sox',
            'tb rays': 'Tampa Bay Rays',
            'kc royals': 'Kansas City Royals'
            'phi phillies': 'Philadelphia Phillies',
            'mia marlins': 'Miami Marlins',
            'pit pirates': 'Pittsburgh Pirates'
        }


    def request_html(self, sport):
        url = self.base_url % self.lgs[sport]
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def extract_match(self, html, sport):
        # html parsing filters
        search_filter = {'data-wager-type':'ml'}
        afilter = 'myb-sportbook__row-first-team'
        hfilter = 'myb-sportbook__row-second-team'

        hhtml = html.find('div', hfilter).find('button', attrs=search_filter)
        ahtml = html.find('div', afilter).find('button', attrs=search_filter)

        # lookup team in dictionary if sport is baseball
        home = self.teams[hhtml['data-team'].lower()] if sport == 'baseball' else hhtml['data-team']
        away = self.teams[ahtml['data-team'].lower()] if sport == 'baseball' else ahtml['data-team']

        site = 'xbet.ag'

        m = match.Match(home, away, hhtml['data-odds'], ahtml['data-odds'], site, site)
        # return an individual match
        return m


    def get_matches(self, sport):
        # raw_html returns a string of the html
        raw_html = self.request_html(sport)
        soup = BeautifulSoup(raw_html, 'html.parser')
        dates = soup.find_all('div', class_='myb-sportbook__sportbook-game-module')
        matches = {}
        for d in dates:
            m = self.extract_match(d, sport)
            matches[m.key] = m
        # return a dictionary of matches from xbet keyed by their m.key
        return matches
