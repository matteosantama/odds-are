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


if __name__ == '__main__':
    main()
