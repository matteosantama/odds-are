# custom module imports
from scrapers import bovada
from scrapers import xbet
from scrapers import bookmaker
from match import Match


# define constants
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


def main():
    # TODO: refactor as seperate Driver class

    bovscr = bovada.Bovada()
    xbetscr = xbet.Xbet()
    bmscr = bookmaker.Bookmaker()

    # retrieve a dict of upcoming Match objects with Bovada odds
    # matches keyed by match_id
    bov_matches = bovscr.get_matches(LEAGUE)
    xbet_matches = xbetscr.get_matches(LEAGUE)
    bm_matches = bmscr.get_matches(LEAGUE)

    # compare scraped odds and update matches
    update_odds(bov_matches, xbet_matches)
    update_odds(bov_matches, bm_matches)

    print '\n'

    for b in bov_matches:
        print bov_matches[b]

    print '\n'

    for x in xbet_matches:
        print xbet_matches[x]

    print '\n'

    for bm in bm_matches:
        print bm_matches[bm]


if __name__ == '__main__':
    main()
