# custom module imports
from scrapers import bovada
from scrapers import xbet
from scrapers import bookmaker
from scrapers import intertops
from scrapers import heritage
from match import Match
from emailer import Emailer


LEAGUE = 'nfl'


def update_odds(primary, secondary):
    for key, match in secondary.iteritems():
        if key not in primary:
            print 'ERROR: Could not find match'
            print match
        else:
            if match.home_odds > primary[key].home_odds:
                print 'Found better odds for %s on %s' % (match.home_team, match.hodds_site)
            if match.away_odds > primary[key].away_odds:
                print 'Found better odds for %s on %s' % (match.away_team, match.aodds_site)


def find_profit_opps(matches):
    opps = []
    for k, v in matches.iteritems():
        if v.home_odds + v.away_odds > 0:
            opps.append(v)
    return opps


def main():
    print 'Analyzing upcoming matches...'

    # init all scraper classes
    bov = bovada.Bovada()
    xbt = xbet.Xbet()
    bkmkr = bookmaker.Bookmaker()
    inter = intertops.Intertops()
    heri = heritage.Heritage()

    # init emailer class
    mailer = Emailer()

    # use bovada as baseline odds
    matches = bov.get_matches(LEAGUE)

    # retrieve xbet data and update for better odds
    new_odds = xbt.get_matches(LEAGUE)
    update_odds(matches, new_odds)

    # retrieve bookmaker data and update for better odds
    new_odds = bkmkr.get_matches(LEAGUE)
    update_odds(matches, new_odds)

    # retrieve intertops data and update for better odds
    new_odds = inter.get_matches(LEAGUE)
    update_odds(matches, new_odds)

    # retrieve heritage data and update for better off
    new_odds = heri.get_matches(LEAGUE)
    update_odds(matches, new_odds)


    # return a list of matches with sure profit opportunities
    opps = find_profit_opps(matches)
    for o in opps:
        print o
    print 'Execution complete'


if __name__ == '__main__':
    main()
