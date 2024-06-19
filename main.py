from rates_for_today import get_today_exchange_rate, get_today_gold_rate
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graph
import tkinter as tk

a = ["A", "B", "C", "D", "E"]
b = [45000, 42000, 52000, 49000, 47000]

def main():

    key1, value1 = graph.create_graph_currencies()

    app_window = tk.Tk()
    app_window.title('Kursy walut')
    app_window.geometry("800x500")

    label = tk.Label(text='Rezultat')
    label.pack()

    result = tk.Text(height=10, width=70)
    result.config(state = 'normal')
    result.config(state='disabled')
    result.pack()


    basic_codes = ['EUR', 'USD', 'GBP', 'CHF']
    currencies, currencies_date = get_today_exchange_rate(basic_codes)
    gold, gold_date = get_today_gold_rate()

    result.config(state='normal')

    result.insert(tk.INSERT, f'Kurs złota na dzień: {gold_date}\n')

    result.insert(tk.INSERT, f'Wartość złota 1g - {gold:0.2f} zł.\n')

    result.insert(tk.INSERT, f'Kursy walut na dzień: {currencies_date}\n')
    for currency in currencies:
        result.insert(tk.INSERT, f'Kurs waluty: {currency['currency'].upper()}, wynosi 1{currency['code']} - {currency['mid']:.2f}zł.\n')
    result.config(state='disabled')

    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).plot(key1, value1)

    canvas = FigureCanvasTkAgg(fig, master=app_window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    app_window.mainloop()

if __name__ == '__main__':
    main()