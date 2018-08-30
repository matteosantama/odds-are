# custom module imports
from scrapers import bovada
from scrapers import intertops
from match import Match

# import library packages


def main():
    bovscr = bovada.Bovada()

    # retrieve a list of upcoming Match objects with Bovada odds
    # acceptable parameters include 'nfl', 'nba', 'mlb'
    upcoming_matches = bovscr.get_matches('nfl')
    for um in upcoming_matches:
        print um

if __name__ == '__main__':
    main()
