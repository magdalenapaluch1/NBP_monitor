from rates_for_today import get_today_exchange_rate, get_today_gold_rate
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graph
import tkinter as tk
from tkinter import ttk

PADING_VALUE = 10
DROP_DOWN_MENU_VALUE = ["USD", "EUR", "CHF", "GBP", "ZŁOTO"]

def button_pushed(figure, canvas, code, start_date, end_date):

    if code == 'ZŁOTO':
        key_date, value_rate = graph.create_graph_gold(start_date, end_date)
        figure.clear()
        figure.add_subplot(111).plot(key_date, value_rate)
        canvas.draw()
    else:
        key_date, value_rate = graph.create_graph_currencies(code, start_date, end_date)
        figure.clear()
        figure.add_subplot(111).plot(key_date, value_rate)
        canvas.draw()


def main():

    app_window = tk.Tk()
    app_window.title('Kursy walut')
    #app_window.geometry("1200x800")

    frame_result = tk.Frame(app_window, highlightbackground='black', highlightthickness=1)
    frame_result.grid(column = 0, row = 0, sticky = "NEWS")
    frame_graph = tk.Frame(app_window, highlightbackground='black', highlightthickness=1)
    frame_graph.grid(column = 0, row = 1, columnspan = 2, sticky = "NEWS")
    frame_date_input = tk.Frame(app_window, highlightbackground='black', highlightthickness=1)
    frame_date_input.grid(column = 1, row = 0, sticky = "NEWS")

    result_label = tk.Label(frame_result, text='Rezultat')
    result_label.pack()

    result = tk.Text(frame_result, height=10, width=70)
    result.config(state = 'normal')
    result.config(state = 'disabled')
    result.pack(padx=PADING_VALUE, pady=(0, PADING_VALUE))

    label_period = tk.Label(frame_date_input, text='Podaj zakres')
    label_period.grid(column = 0, row = 0)

    #okna do wprowadzenia daty Entry
    start_date = tk.Entry(frame_date_input)
    start_date.insert(0,'rrrr-mm-dd')
    start_date.grid(column = 0, row = 2, padx = PADING_VALUE)
    start_date_label = tk.Label(frame_date_input, text='Data startu: ', )
    start_date_label.grid(column = 0, row = 1, padx = PADING_VALUE)
    end_date = tk.Entry(frame_date_input)
    end_date.insert(0,'rrrr-mm-dd')
    end_date.grid(column = 0, row = 4, padx = PADING_VALUE)
    end_date_label = tk.Label(frame_date_input, text='Data zakończenia: ')
    end_date_label.grid(column = 0, row = 3, padx = PADING_VALUE)
    #wybór waluty z menu rozwijanego
    combo_currencies_label = tk.Label(frame_date_input, text='Wybierz walutę: ')
    combo_currencies_label.grid(column = 0, row = 5, padx = PADING_VALUE)
    combo_currencies = ttk.Combobox(frame_date_input, state="readonly", values=DROP_DOWN_MENU_VALUE)
    combo_currencies.current(0)
    combo_currencies.grid(column = 0, row = 6, padx = PADING_VALUE)
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)  # A tk.DrawingArea.
    #Button zatwierdzajacy
    accept_button = tk.Button(frame_date_input, text = "OK", command= lambda: button_pushed(fig, canvas, combo_currencies.get(), start_date.get(), end_date.get()))
    accept_button.grid(column = 0, row = 7, pady = PADING_VALUE)


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

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx = PADING_VALUE, pady = PADING_VALUE)


    app_window.mainloop()

if __name__ == '__main__':
    main()