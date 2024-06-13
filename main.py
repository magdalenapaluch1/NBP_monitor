from rates_for_today import get_today_exchange_rate, get_today_gold_rate
import tkinter as tk

def main():
    app_window = tk.Tk()
    app_window.title('Kursy walut')
    app_window.geometry("500x300")

    label = tk.Label(text='Rezultat')
    label.pack()

    result = tk.Text(height=10, width=70)
    result.config(state = 'normal')
    result.config(state='disabled')
    result.pack()


    basic_codes = ['EUR', 'USD', 'GBP', 'CHF']
    currencies = get_today_exchange_rate(basic_codes)
    gold = get_today_gold_rate()

    result.config(state='normal')

    result.insert(tk.INSERT, f'Wartość złota 1g - {gold:0.2f} zł.\n')

    for currency in currencies:
        result.insert(tk.INSERT, f'Kurs waluty: {currency['currency'].upper()}, wynosi 1{currency['code']} - {currency['mid']:.2f}zł.\n')
    result.config(state='disabled')

    app_window.mainloop()

if __name__ == '__main__':
    main()