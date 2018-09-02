# custom imporst
import match

# library imports
from bs4 import BeautifulSoup
import requests
import sys
import logging


class Intertops(object):


    def __init__(self):
        self.base_url = 'https://sports.intertops.eu/en/Bets/Competition/1018'
        self.logger = logging.getLogger(__name__)

    def request_html(self):
        url = self.base_url
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def extract_match(self, row):
        away = row.find('div', class_='ustop').text.strip()
        home = row.find('div', class_='usbot').text.strip()

        aodds = row.find('div', {'title': away})
        hodds = row.find('div', {'title': home})
        try:
            aodds = aodds.text.strip()
            hodds = hodds.text.strip()
        except AttributeError:
            aodds = -sys.maxsize - 1
            hodds = -sys.maxsize - 1

        site = 'intertops.eu'
        m = match.Match(home, away, hodds, aodds, site, site)

        return m


    def get_matches(self, league):
        raw_html = self.request_html()
        soup = BeautifulSoup(raw_html, 'html.parser')
        rows = soup.find_all('div', class_='onemarket')
        matches = {}
        for r in rows:
            m = self.extract_match(r)
            matches[m.key] = m
        # return a dictionary of matches from xbet keyed by their m.key
        return matches
