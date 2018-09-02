# custom module imports
import match

# library imports
from bs4 import BeautifulSoup
import requests
import sys
import math
import logging


# global variables
league_to_sport = {
    'nfl': 'football',
}


class Bookmaker(object):

    def __init__(self):
        self.base_url = 'https://www.bookmaker.eu/live-lines/%s/%s'
        self.logger = logging.getLogger(__name__)


    def request_html(self, league):
        url = self.base_url % (league_to_sport[league], league)
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        r = requests.get(url, headers=header)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def extract_match(self, html):
        visitor_html = html.find('div', class_='vTeam')
        home_html = html.find('div', class_='hTeam')

        visitor = next(visitor_html.find('div', class_='team').h3.stripped_strings)
        vodds = visitor_html.find('div', class_='money').span.span
        if vodds is not None:
            vodds = int(vodds.text)
        else:
            vodds = -sys.maxsize - 1

        home = next(home_html.find('div', class_='team').h3.stripped_strings)
        hodds = home_html.find('div', class_='money').span.span
        if hodds is not None:
            hodds = int(hodds.text)
        else:
            hodds = -sys.maxsize - 1

        site = 'bookmaker.eu'
        m = match.Match(home, visitor, hodds, vodds, site, site)
        return m


    def get_matches(self, league):
        # raw_html returns a string of the html
        raw_html = self.request_html(league)
        soup = BeautifulSoup(raw_html, 'html.parser')
        matchups = soup.find_all('div', class_='matchup')
        matches = {}
        for mu in matchups:
            odds = mu.ul.find('li', class_='odds')
            m = self.extract_match(odds)
            matches[m.key] = m
        return matches
