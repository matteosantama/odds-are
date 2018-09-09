# custom module imports
import match

# library imports
from bs4 import BeautifulSoup
import requests
import sys
import math
import logging
from datetime import datetime as dt
from datetime import timedelta


class Bookmaker(object):

    def __init__(self):
        self.base_url = 'https://www.bookmaker.eu/live-lines/%s/%s'
        self.logger = logging.getLogger(__name__)
        self.lgs = {
            'football': 'nfl',
            'baseball': 'major-league-baseball'
        }


    def request_html(self, sport):
        url = self.base_url % (sport, self.lgs[sport])
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        r = requests.get(url, headers=header)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def parse_date(self, html):
        time = html.find_previous_sibling().text.strip()
        date_header = html.find_parent('div', class_='externalLinesPage').find('div', class_='linesSubhead').text
        # check if the game is in the following year
        yr = (dt.today().year + 1) if (dt.today().year == 12 and date_header[-7:-4] == 'Jan') else dt.today().year
        # construct date string in the following format: '%b %d %I:%M %p %Y'
        date_string = date_header[-7:] + time + ' ' + str(yr)
        date = dt.strptime(date_string, '%b %d %I:%M %p %Y') + timedelta(hours = 2)

        return date


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

        date = self.parse_date(html)
        site = 'bookmaker.eu'

        m = match.Match(home, visitor, hodds, vodds, site, site, date)
        return m


    def get_matches(self, sport):
        # raw_html returns a string of the html
        raw_html = self.request_html(sport)
        soup = BeautifulSoup(raw_html, 'html.parser')
        matchups = soup.find_all('div', class_='matchup')
        matches = {}
        for mu in matchups:
            odds = mu.ul.find('li', class_='odds')
            m = self.extract_match(odds)
            matches[m.key] = m
        return matches
