from rates_for_today import get_today_exchange_rate, get_today_gold_rate
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graph
import tkinter as tk

PADING_VALUE = 10

def main():

    key_date, value_rate = graph.create_graph_currencies('USD', '2024-06-03', '2024-06-11')

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
    start_date.grid(column = 0, row = 1, padx = PADING_VALUE)
    #Button zatwierdzajacy
    accept_button = tk.Button(frame_date_input, text = "OK")
    accept_button.grid(column = 0, row = 2)


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
    fig.add_subplot(111).plot(key_date, value_rate)

    canvas = FigureCanvasTkAgg(fig, master=frame_graph)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx = PADING_VALUE, pady = PADING_VALUE)

    app_window.mainloop()

if __name__ == '__main__':
    main()