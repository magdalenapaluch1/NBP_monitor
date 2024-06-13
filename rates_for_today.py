
from API_details import get_currencies, get_gold_rate
from datetime import date

def show_today_exchange_rate():

    json_response = get_currencies()

    GBP_currency = json_response[0]['rates'][10]['mid']
    EUR_currency = json_response[0]['rates'][7]['mid']
    CHF_currency = json_response[0]['rates'][9]['mid']
    USD_currency = json_response[0]['rates'][1]['mid']

    today = date.today().strftime('%d/%m/%Y')
    
    print('Kurs walut na dzień: ' + today)

    print('Kurs funta brytyjskiego wynosi 1GBP - {:0.2f} zł.'.format(GBP_currency))
    print('Kurs euro wynosi 1EUR - {:0.2f} zł.'.format(EUR_currency))
    print('Kurs franka szwajcarskiego wynosi 1CHF - {:0.2f} zł.'.format(CHF_currency))
    print('Kurs dolara amerykańskiego wynosi 1USD - {:0.2f} zł.'.format(USD_currency))

def show_today_gold_rate():

    json_response = get_gold_rate()
    
    gold_rate = json_response[0]['cena']
    
    today = date.today().strftime('%d/%m/%Y')

    print('Kurs złota na dzień: ' + today)
    print('Wartość złota 1g - {:0.2f} zł.'.format(gold_rate))
