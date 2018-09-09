# custom imporst
import match

# library imports
from datetime import datetime as dt
from datetime import timezone
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
            'BAL': 'Baltimore Orioles',
            'BOS': 'Boston Red Sox',
            'CHC': 'Chicago Cubs',
            'CWS': 'Chicago White Sox',
            'CIN': 'Cincinnati Reds',
            'CLE': 'Cleveland Indians',
            'COL': 'Colorado Rockies',
            'DET': 'Detroit Tigers',
            'FLA': 'Florida Marlins',
            'HOU': 'Houston Astros',
            'KAN': 'Kansas City Royals',
            'LAA': 'Los Angeles Angels',
            'LOS': 'Los Angeles Dodgers',
            'MIL': 'Milwaukee Brewers',
            'MIN': 'Minnesota Twins',
            'NYM': 'New York Mets',
            'NYY': 'New York Yankees',
            'OAK': 'Oakland Athletics',
            'PHI': 'Philadelphia Phillies',
            'PIT': 'Pittsburgh Pirates',
            'SDG': 'San Diego Padres',
            'SFO': 'San Francisco Giants',
            'SEA': 'Seattle Mariners',
            'STL': 'Saint Louis Cardinals',
            'TPB': 'Tampa Bay Rays',
            'TEX': 'Texas Rangers',
            'TOR': 'Toronto Blue Jays',
            'WAS': 'Washington Nationals'
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


    def parse_date(self, row):
        span = row.find('span', class_='eventdatetime')
        date_string = span['title'] if span['title'] is not None else span['data-original-title']
        date = dt.strptime(date_string, '%m/%d/%Y<br/>%I:%M %p')
        # convert from utc to local timezone
        return date.replace(tzinfo=timezone.utc).astimezone(tz=None)


    def extract_match(self, row):
        # *_tag is a variable that contains the three letter code and pitcher for each team
        away_tag = row.find('div', class_='ustop').text.strip()
        home_tag = row.find('div', class_='usbot').text.strip()

        # when odds are updated, the title attribute gets renamed 'data-original-title'
        aodds = row.find('div', {'title': away_tag})
        if aodds is None:
            aodds = row.find('div', {'data-original-title': away_tag})
        hodds = row.find('div', {'title': home_tag})
        if hodds is None:
            hodds = row.find('div', {'data-original-title': home_tag})

        try:
            aodds = aodds.text.strip()
            hodds = hodds.text.strip()
        except AttributeError:
            aodds = -sys.maxsize - 1
            hodds = -sys.maxsize - 1

        # convert team tags into universal team names
        home, away = self.get_team_names(home_tag, away_tag)

        date = self.parse_date(row)
        site = 'intertops.eu'
        m = match.Match(home, away, hodds, aodds, site, site, date)

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
