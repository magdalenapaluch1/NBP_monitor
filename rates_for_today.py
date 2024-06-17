
from API_details import get_currencies, get_gold_rate

def get_today_exchange_rate(codes):
    """gets current rates of currencies
    """
    currencies_list = []

    json_response = get_currencies()
    effective_date = json_response[0]['effectiveDate']

    for name_currency in json_response[0]['rates']:
        if name_currency['code'] in codes:
            currencies_list.append({'currency': name_currency['currency'].upper(), 'code': name_currency['code'], 'mid': name_currency['mid']})

    return currencies_list, effective_date

def get_today_gold_rate():
    """gets current rates of gold
    """

    json_response = get_gold_rate()
    gold_date = json_response[0]['data']

    gold_rate = json_response[0]['cena']

    return gold_rate, gold_date
