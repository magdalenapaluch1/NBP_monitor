'''Connection with API to get response about currencies'''

from requests import get

def get_currencies():

    api_url = 'http://api.nbp.pl/api/exchangerates/tables/A/today/'
    response = get(api_url)
    currency_data = response.json()
    return currency_data


def get_gold_rate():
    '''1g złota'''
    api_url = 'http://api.nbp.pl/api/cenyzlota/today'
    response = get(api_url)
    gold_data = response.json()
    return gold_data
