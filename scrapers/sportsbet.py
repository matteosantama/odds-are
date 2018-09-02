# custom imports
import match

# library imports
from bs4 import BeautifulSoup
import requests
import json
import sys
import logging


league_to_sport = {
    'NFL': 'Football'
}


class Sportsbet(object):

    def __init__(self):
        self.url = 'https://www.sportsbetting.ag/sportsbook/Line/RetrieveLineData'
        self.logger = logging.getLogger(__name__)


    def request_html(self, league):
        # with requests.Session() as s:
            # post = s.post('https://www.sportsbetting.ag/sportsbook')
        payload = {
            'param.SortOption': 'D',
            'param.PrdNo': '0',
            'param.Type': 'H2H',
            'param.RequestType': 'Normal',
            'param.H2HParam.Lv1': league_to_sport[league],
            'param.H2HParam.Lv2': league
        }
        r = requests.post(self.url, data=payload)

        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def extract_match(self, tbody):
        away_data = tbody.find('tr', class_='firstline')
        home_data = tbody.find('tr', class_='otherline')

        home = home_data.find('td', class_='col_teamname').text
        away = away_data.find('td', class_='col_teamname').text

        hodds = home_data.find('td', class_='moneylineodds').string
        aodds = away_data.find('td', class_='moneylineodds').string

        hodds = (-sys.maxsize - 1) if hodds is None else hodds
        aodds = (-sys.maxsize - 1) if aodds is None else aodds

        site = 'sportsbetting.ag'
        m = match.Match(home, away, hodds, aodds, site, site)
        return m

    def get_matches(self, league):
        html = self.request_html(league.upper())
        soup = BeautifulSoup(html, 'html.parser')
        events = soup.find('table', class_='league').find_all('tbody', class_='event')
        matches = {}
        for ev in events:
            m = self.extract_match(ev)
            matches[m.key] = m

        return matches
