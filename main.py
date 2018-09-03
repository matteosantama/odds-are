# custom module imports
from scrapers import bovada
from scrapers import xbet
from scrapers import bookmaker
from scrapers import intertops
from scrapers import sportsbet
from match import Match
from emailer import Emailer

# library imports
import logging


LEAGUE = 'nfl'
PROF = 'Sure Profit Opportunities'
MUS = 'Upcoming Matchups'

# init and configure logger object
logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s:%(levelname)s: %(message)s'
DATEFMT = '%m/%d/%Y %I:%M:%S%p'
FILENAME = 'output.log'
logging.basicConfig(filename=FILENAME, filemode='w', format=FORMAT, datefmt=DATEFMT, level=logging.INFO)


def update_odds(primary, secondary):
    for key, match in secondary.items():
        if key not in primary:
            logger.error('Could not find match for: %s', str(match))
        else:
            if match.home_odds > primary[key].home_odds:
                logger.info('Found better odds for %s on %s', match.home_team, match.hodds_site)
                primary[key].home_odds = match.home_odds
                primary[key].hodds_site = match.hodds_site
            if match.away_odds > primary[key].away_odds:
                logger.info('Found better odds for %s on %s', match.home_team, match.hodds_site)
                primary[key].away_odds = match.away_odds
                primary[key].aodds_site = match.aodds_site


def find_profit_opps(matches):
    opps = []
    for k, v in matches.items():
        if v.home_odds + v.away_odds > 0:
            opps.append(v)
    return opps


def upcoming(matches):
    upco = []
    for m in matches:
        upco.append(str(matches[m]))
    return upco


def main():
    logger.info('Initializing scrapers and performing web requests')

    # init all scraper classes
    bov = bovada.Bovada()
    xbt = xbet.Xbet()
    bkmkr = bookmaker.Bookmaker()
    inter = intertops.Intertops()
    sports = sportsbet.Sportsbet()

    # init emailer class
    mailer = Emailer()

    # use bovada as baseline odds
    matches = bov.get_matches(LEAGUE)
    logger.info('Successfully retrieved odds from bovada.lv')


    # retrieve heritage data and update for better off
    new_odds = sports.get_matches(LEAGUE)
    logger.info('Successfully retrieved odds from sportsbook.ag')
    update_odds(matches, new_odds)

    # retrieve xbet data and update for better odds
    new_odds = xbt.get_matches(LEAGUE)
    logger.info('Successfully retrieved odds from xbet.ag')
    update_odds(matches, new_odds)

    # retrieve bookmaker data and update for better odds
    new_odds = bkmkr.get_matches(LEAGUE)
    logger.info('Successfully retrieved odds from bookmaker.eu')
    update_odds(matches, new_odds)

    # retrieve intertops data and update for better odds
    new_odds = inter.get_matches(LEAGUE)
    logger.info('Successfully retrieved odds from intertops.eu')
    update_odds(matches, new_odds)


    # return a list of matches with sure profit opportunities
    opps = find_profit_opps(matches)
    # get a list of upcoming matches in string form
    match_strings = upcoming(matches)

    # send profit opps with new line characters inserted if any are detected
    if len(opps) > 0:
        mailer.send_mail(PROF, '\n'.join(opps))

    # uncomment to send match logs
    # mailer.send_mail(MUS, '\n'.join(match_strings))


    logger.info('Execution successfully completed')
    mailer.send_log(FILENAME)

if __name__ == '__main__':
    main()
