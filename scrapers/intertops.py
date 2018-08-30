import requests

class Intertops(object):

    def __intit__(self):
        pass


    def get_request(self):
        url = 'https://sports.intertops.eu/en/Bets/Competition/1018'
        req = requests.get(url)
        return req
