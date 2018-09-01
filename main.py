# custom module imports
from scrapers import bovada
from scrapers import xbet
from scrapers import bookmaker
from scrapers import intertops
from scrapers import heritage
from match import Match


# define constants
LEAGUE = 'nfl'


def print_matches(bovada_matches, xbet_matches, bm_matches):
    for b in bov_matches:
        print bov_matches[b]

    print '\n'

    for x in xbet_matches:
        print xbet_matches[x]

    print '\n'

    for bm in bm_matches:
        print bm_matches[bm]


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


def find_profit(matches):
    for k, v in matches.iteritems():
        if v.home_odds + v.away_odds > 0:
            print 'Found profit opportunity'
            v.print_with_site()


def main():
    print 'Analyzing upcoming matches...'

    bovscr = bovada.Bovada()
    xbetscr = xbet.Xbet()
    bmscr = bookmaker.Bookmaker()
    interscr = intertops.Intertops()
    herscr = heritage.Heritage()

    # retrieve a dict of upcoming Match objects with Bovada odds
    # matches keyed by match_id
    bov_matches = bovscr.get_matches(LEAGUE)
    xbet_matches = xbetscr.get_matches(LEAGUE)
    bm_matches = bmscr.get_matches(LEAGUE)
    it_matches = interscr.get_matches(LEAGUE)
    her_matches = herscr.get_matches(LEAGUE)

    # compare scraped odds and update matches
    update_odds(bov_matches, xbet_matches)
    update_odds(bov_matches, bm_matches)
    update_odds(bov_matches, it_matches)
    update_odds(bov_matches, her_matches)
    find_profit(bov_matches)
    print 'Execution complete'


if __name__ == '__main__':
    main()
