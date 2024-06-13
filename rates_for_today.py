
from API_details import get_currencies, get_gold_rate
from datetime import date

def show_today():
    """get and print todays date
    """
    
    today = date.today().strftime('%d/%m/%Y')

    print('Kurs na dzień: ' + today)

def get_today_exchange_rate(codes):
    """gets current rates of currencies
    """
    currencies_list = []

    json_response = get_currencies()

    show_today()

    for name_currency in json_response[0]['rates']:
        if name_currency['code'] in codes:
            currencies_list.append({'currency': name_currency['currency'].upper(), 'code': name_currency['code'], 'mid': name_currency['mid']})

    return currencies_list

def get_today_gold_rate():
    """gets current rates of gold
    """

    json_response = get_gold_rate()

    gold_rate = json_response[0]['cena']
    
    show_today()

    return gold_rate
