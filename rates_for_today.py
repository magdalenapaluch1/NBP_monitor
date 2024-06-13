
from API_details import get_currencies, get_gold_rate
from datetime import date

#CONSTANS VALUES

codes = ['EUR', 'USD', 'GBP', 'CHF']

def show_today():
    """get and print todays date
    """
    
    today = date.today().strftime('%d/%m/%Y')

    print('Kurs na dzień: ' + today)

def show_today_exchange_rate():
    """print current rates of currencies
    """
    
    json_response = get_currencies()

    show_today()

    for name_currency in json_response[0]['rates']:
        if name_currency['code'] in codes:
            print(f'Kurs waluty: {name_currency['currency'].upper()}, wynosi 1{name_currency['code']} - {name_currency['mid']:.2f}zł.')

def show_today_gold_rate():
    """print current rates of gold
    """

    json_response = get_gold_rate()

    gold_rate = json_response[0]['cena']
    
    show_today()

    print('Wartość złota 1g - {:0.2f} zł.'.format(gold_rate))
