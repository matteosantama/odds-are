# custom imports
import match

# library imports
import requests
import json
import sys


league_to_sport = {
    'NFL': 'Football'
}


class Heritage(object):


    def __init__(self):
        self.base_url = 'https://web1.heritagesports.eu/hstw/v2/search/eventsBySportSubSport?periodNumber=0&sport=%s&subSport=%s'


    def request_html(self, league):
        # takes an UPPER version of league as the parameter
        header = {
            'Host': 'web1.heritagesports.eu',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU3NzI3NDE0LTM5ZTQtNDM1YS04NzA0LTE1MGQxZTJlNDIwNyIsInN0YXRpY0xpbmVzIjpmYWxzZSwic3RvcmUiOiJSZWdMbyIsImFnZW50IjoiWFRPUEEiLCJzcG9ydEJvb2tJZCI6MSwiY3VzdG9tZXIiOiIxMDk2NjMiLCJpYXQiOjE1MzU4MzY1OTB9.ie-PWTQnsXQv82ygW4n0ecS8Beq-x51awV_-VsTgbiE',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        url = self.base_url % (league_to_sport[league], league)
        r = requests.get(url, headers=header)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print 'Error attempting to contact %s' % r.url
            print e
            print 'Exiting...'
            sys.exit(1)

        return r.json()


    def moneyline_outcomes(self, json):
        for market in json['markets']:
            if market['marketType'] == 'Moneyline':
                return market['outcomes']
        return [None]


    def extract_match(self, json):
        visitor = json['participants'][0]['id']
        home = json['participants'][1]['id']

        outcomes = self.moneyline_outcomes(json)
        for oc in outcomes:
            if oc is None:
                hodds = vodds = -sys.maxint - 1
            elif oc['outcome'] == home:
                hodds = oc['price']
            elif oc['outcome'] == visitor:
                vodds = oc['price']

        site = 'heritage.eu'
        m = match.Match(home, visitor, hodds, vodds, site, site)

        return m


    def get_matches(self, league):
        events = self.request_html(league.upper())['Events']
        matches = {}
        for ev in events:
            if len(ev['markets']) > 0:
                m = self.extract_match(ev)
                matches[m.key] = m

        return matches
