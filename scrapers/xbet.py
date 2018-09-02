# custom module imports
import match

# library imports
from bs4 import BeautifulSoup
import requests
import sys
import logging

# global variables
league_to_sport = {
    'nfl': 'football',
}

class Xbet(object):


    def __init__(self):
        self.base_url = 'https://xbet.ag/sportsbook/%s/'
        self.logger = logging.getLogger(__name__)

    def request_html(self, league):
        url = self.base_url % league
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def extract_match(self, html):
        # html parsing filters
        search_filter = {'data-wager-type':'ml'}
        afilter = 'myb-sportbook__row-first-team'
        hfilter = 'myb-sportbook__row-second-team'
        hhtml = html.find('div', hfilter).find('button', attrs=search_filter)
        ahtml = html.find('div', afilter).find('button', attrs=search_filter)
        xb = 'xbet.ag'
        m = match.Match(hhtml['data-team'], ahtml['data-team'], hhtml['data-odds'], ahtml['data-odds'], xb, xb)
        # return an individual match
        return m


    def get_matches(self, league):
        # raw_html returns a string of the html
        raw_html = self.request_html(league)
        soup = BeautifulSoup(raw_html, 'html.parser')
        dates = soup.find_all('div', class_='myb-sportbook__sportbook-game-module')
        matches = {}
        for d in dates:
            m = self.extract_match(d)
            matches[m.key] = m
        # return a dictionary of matches from xbet keyed by their m.key
        return matches
