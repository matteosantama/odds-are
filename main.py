# custom module imports
from scrapers import bovada
from scrapers import xbet
from scrapers import bookmaker
from match import Match


# define constants
LEAGUE = 'nfl'


def main():
    bovscr = bovada.Bovada()
    xbetscr = xbet.Xbet()

    # retrieve a dict of upcoming Match objects with Bovada odds
    # matches keyed by match_id
    bov_matches = bovscr.get_matches(LEAGUE)
    xbet_matches = xbetscr.get_matches(LEAGUE)


    for xb in xbet_matches:
        if xb in bov_matches:
            print 'yes'
        else:
            print 'no'

    # for k,v in bov_matches.iteritems():
    #     print 'HOME: %s AWAY: %s KEY: %s' % (v.home_team, v.away_team, k)
    #
    # print 'BREAK'
    #
    # for k,v in xbet_matches.iteritems():
    #     print 'HOME: %s AWAY: %s KEY: %s' % (v.home_team, v.away_team, k)


if __name__ == '__main__':
    main()
