'''Connection with API to get response about currencies and gold'''

from requests import get

BASE_URL = 'https://api.nbp.pl/api/'

def send_request_and_get_response(url):
    api_url = url
    response = get(api_url)
    return response


def get_currencies() -> list:
    """API connection to show the details of curriencies for today

    Returns:
        list: information about rates of currencies
    """

    response = send_request_and_get_response(BASE_URL + '/exchangerates/tables/A/today/')
    if response.status_code == 404:
        response = send_request_and_get_response(BASE_URL + '/exchangerates/tables/A/') 
        #TODO handle other errors
    currency_data = response.json()
    return currency_data

def get_currencies_from_period(code: str, start_date:str, end_date:str):
    """API connection to show the details (rates) of curriencies from period
        user can enter start and end date to see the rates.
        Archived data is available as follows:
        for exchange rates from January 2, 2002,
        however, a single query cannot cover a period longer than 93 days.

    Args:
        code (str): three-letter currency code (ISO 4217 standard)
        start_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
    """

    rates_from_period = {}
    response = send_request_and_get_response(BASE_URL + f'/exchangerates/rates/A/{code}/{start_date}/{end_date}/?format=json')

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
    response = send_request_and_get_response(BASE_URL + '/cenyzlota/today')
    if response.status_code == 404:
        response = send_request_and_get_response(BASE_URL + '/cenyzlota/')
        #TODO handle other errors
    gold_data = response.json()
    return gold_data

def get_gold_from_period(start_date:str, end_date:str):
    """API connection to show the details (rates) of gold from period
        user can enter start and end date to see the rates.
        Archived data is available as follows:
        for exchange rates from January 2, 2013,
        however, a single query cannot cover a period longer than 93 days. 

    Args:
        start_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
    """

    gold_rates_from_period = {}
    response = send_request_and_get_response(BASE_URL + f'/cenyzlota/{start_date}/{end_date}/?format=json')

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

'''Rates for today currencies and gold'''

def get_today_exchange_rates_by_list(codes):
    """gets current rates of currencies
    """
    currencies_list = []

    json_response = get_currencies()
    effective_date = json_response[0]['effectiveDate']

    for name_currency in json_response[0]['rates']:
        if name_currency['code'] in codes:
            currencies_list.append({'currency': name_currency['currency'].upper(), 'code': name_currency['code'], 'mid': name_currency['mid']})

    return currencies_list, effective_date

def get_today_exchange_rate(code):
    response = send_request_and_get_response(f'https://api.nbp.pl/api/exchangerates/rates/A/{code}/')
    json_cur_data = response.json()

    # Json returns one dict
    # {'table': 'A', 'currency': 'dolar amerykański', 'code': 'USD', 'rates': [{'no': '204/A/NBP/2024', 'effectiveDate': '2024-10-18', 'mid': 3.9718}]}
    currency_rate = json_cur_data['rates'][0]['mid']

    return currency_rate

def get_today_gold_rate():
    """gets current rates of gold
    """

    json_response = get_gold_rate()
    gold_date = json_response[0]['data']

    gold_rate = json_response[0]['cena']

    return gold_rate, gold_date

'''Graph date preparation'''

def prepare_currencies_data(code, start_date, end_date):

    result = get_currencies_from_period(code, start_date, end_date)

    graph_date = list(result.keys())
    graph_rates = list(result.values())

    return graph_date, graph_rates

def prepare_gold_data(start_date, end_date):

    result = get_gold_from_period(start_date, end_date)

    graph_date = list(result.keys())
    graph_rates = list(result.values())

    return graph_date, graph_rates
