'''Connection with API to get response about currencies and gold'''

from requests import get

def get_currencies() -> list:
    """API connection to show the details of curriencies for today

    Returns:
        list: information about rates of currencies
    """

    api_url = 'http://api.nbp.pl/api/exchangerates/tables/A/today/'
    response = get(api_url)
    if response.status_code == 404:
        api_url = 'http://api.nbp.pl/api/exchangerates/tables/A/'
        response = get(api_url)
        #TODO handle other errors
    currency_data = response.json()
    return currency_data


def get_gold_rate() -> list:
    """API connection to show the details of gold rates for today
        rates describe only 1g of gold
    Returns:
        list: information about rates of gold
    """
    api_url = 'http://api.nbp.pl/api/cenyzlota/today'
    response = get(api_url)
    if response.status_code == 404:
        api_url = 'http://api.nbp.pl/api/cenyzlota/'
        response = get(api_url)
        #TODO handle other errors
    gold_data = response.json()
    return gold_data
