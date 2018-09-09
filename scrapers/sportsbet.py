# custom imports
import match

# library imports
from datetime import datetime as dt
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
import json
import sys
import logging


class Sportsbet(object):

    def __init__(self):
        self.base_url = 'https://www.sportsbetting.ag/sportsbook/%s/%s'
        self.logger = logging.getLogger(__name__)
        self.lgs = {
            'football': 'nfl',
            'baseball': 'mlb'
        }


    def request_html(self, sport):
        url = self.base_url % (sport, self.lgs[sport])
        r = requests.get(url)

        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logging.exception('Error attempting to contact %s', r.url)
            sys.exit(1)

        return r.content


    def extract_match(self, tbody):
        day_month_year = tbody.find_previous_sibling('tbody', class_='date expanded').text.split(' - ')[0].strip()
        time = tbody.find('td', class_='col_time').text.strip()
        date_string = day_month_year + ' ' + time
        # convert to datetime object and adjust timezone
        date = dt.strptime(date_string, '%A, %b %d, %Y %I:%M %p') - timedelta(hours = 1)

        away_data = tbody.find('tr', class_='firstline')
        home_data = tbody.find('tr', class_='otherline')

        home = home_data.find('td', class_='col_teamname').contents[0]
        away = away_data.find('td', class_='col_teamname').contents[0]

        # not ideal but will do for now
        if home.strip() == 'St. Louis Cardinals':
            home = 'Saint Louis Cardinals'
        if away.strip() == 'St. Louis Cardinals':
            away = 'Saint Louis Cardinals'

        hodds = home_data.find('td', class_='moneylineodds').string
        aodds = away_data.find('td', class_='moneylineodds').string

        hodds = (-sys.maxsize - 1) if hodds is None else hodds
        aodds = (-sys.maxsize - 1) if aodds is None else aodds

        site = 'sportsbetting.ag'
        m = match.Match(home, away, hodds, aodds, site, site, date)

        return m


    def get_matches(self, sport):
        html = self.request_html(sport)
        soup = BeautifulSoup(html, 'html.parser')
        events = soup.find('table', class_='league').find_all('tbody', class_='event')
        matches = {}
        for ev in events:
            m = self.extract_match(ev)
            matches[m.key] = m

        return matches
