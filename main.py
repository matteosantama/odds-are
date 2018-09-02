# custom module imports
from scrapers import bovada
from scrapers import xbet
from scrapers import bookmaker
from scrapers import intertops
from scrapers import heritage
from match import Match
from emailer import Emailer


LEAGUE = 'nfl'
PROF = 'Sure Profit Opportunities'
MUS = 'Upcoming Matchups'


def update_odds(primary, secondary):
    for key, match in secondary.iteritems():
        if key not in primary:
            print 'ERROR: Could not find match'
            print match
        else:
            if match.home_odds > primary[key].home_odds:
                print 'Found better odds for %s on %s' % (match.home_team, match.hodds_site)
                primary[key].home_odds = match.home_odds
                primary[key].hodds_site = match.hodds_site
            if match.away_odds > primary[key].away_odds:
                print 'Found better odds for %s on %s' % (match.away_team, match.aodds_site)
                primary[key].away_odds = match.away_odds
                primary[key].aodds_site = match.aodds_site


def find_profit_opps(matches):
    opps = []
    for k, v in matches.iteritems():
        if v.home_odds + v.away_odds > 0:
            opps.append(v)
    return opps


def upcoming(matches):
    upco = []
    for m in matches:
        upco.append(str(matches[m]))
    return upco


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


    # retrieve heritage data and update for better off
    new_odds = heri.get_matches(LEAGUE)
    update_odds(matches, new_odds)

    # retrieve xbet data and update for better odds
    new_odds = xbt.get_matches(LEAGUE)
    update_odds(matches, new_odds)

    # retrieve bookmaker data and update for better odds
    new_odds = bkmkr.get_matches(LEAGUE)
    update_odds(matches, new_odds)

    # retrieve intertops data and update for better odds
    new_odds = inter.get_matches(LEAGUE)
    update_odds(matches, new_odds)


    # return a list of matches with sure profit opportunities
    opps = find_profit_opps(matches)
    # get a list of upcoming matches in string form
    match_strings = upcoming(matches)

    # send profit opps with new line characters inserted
    mailer.send_mail(PROF, '\n'.join(opps))
    mailer.send_mail(MUS, '\n'.join(match_strings))

    print 'Execution complete'


if __name__ == '__main__':
    main()
