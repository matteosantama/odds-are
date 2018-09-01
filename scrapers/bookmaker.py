# custom module imports
import match

# library imports
from bs4 import BeautifulSoup
import requests
import sys


# global variables
league_to_sport = {
    'nfl': 'football',
}


class Bookmaker(object):


    def __init__(self):
        self.base_url = 'https://www.bookmaker.eu/live-lines/%s/%s'


    def request_html(self, league):
        url = self.base_url % (league_to_sport[league], league)
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        r = requests.get(url, headers=header)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print 'Error attempting to contact %s' % r.url
            print e
            print 'Exiting...'
            sys.exit(1)

        return r.content


    def extract_match(self, html):
        # html parsing strings
        search_filter = {'data-wager-type':'ml'}
        hfilter = 'myb-sportbook__row-first-team'
        afilter = 'myb-sportbook__row-second-team'
        home_html = html.find('div', hfilter).find('button', attrs=search_filter)
        away_html = html.find('div', afilter).find('button', attrs=search_filter)


    def get_matches(self, league):
        # raw_html returns a string of the html
        raw_html = self.request_html(league)
        soup = BeautifulSoup(raw_html, 'html.parser')
        dates = soup.find_all('ul')
        for d in dates:
            print d
