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

def get_currencies_from_period(code: str, start_date:str, end_date:str):
    """API connection to show the details (rates) of curriencies from period
        user can enter start and end date to see the rates 

    Args:
        code (str): three-letter currency code (ISO 4217 standard)
        start_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
    """

    rates_from_period = {}
    api_url = f'http://api.nbp.pl/api/exchangerates/rates/A/{code}/{start_date}/{end_date}/?format=json'
    response = get(api_url)
    currencies_period = response.json()

    for rate in currencies_period['rates']:
        if 'effectiveDate' in rate and 'mid' in rate:
            rates_from_period[rate['effectiveDate']] = rate['mid']
        
    return rates_from_period


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

def get_gold_from_period(start_date:str, end_date:str):
    """API connection to show the details (rates) of gold from period
        user can enter start and end date to see the rates 

    Args:
        start_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
    """

    gold_rates_from_period = {}
    api_url = f'http://api.nbp.pl/api/cenyzlota/{start_date}/{end_date}/?format=json'
    response = get(api_url)

    if response.status_code == 200:
        gold_period = response.json()

        for item in gold_period:
            key = item['data']
            value = item ['cena']
            gold_rates_from_period[key] = value
    else:
        print(f"Error data: {response.status_code}")

        #TODO improve print
        
    return gold_rates_from_period