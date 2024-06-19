from rates_for_today import get_today_exchange_rate, get_today_gold_rate
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graph
import tkinter as tk
from tkinter import ttk
from datetime import datetime

PADING_VALUE = 10 #offset from the axis
DROP_DOWN_MENU_VALUE = ["USD", "EUR", "CHF", "GBP", "ZŁOTO"]
TODAY = datetime.today()

class GUI:

    def __init__(self) -> None:
        #Open Tkinter window
        app_window = tk.Tk()
        app_window.title('Kursy walut')

        #Create Frames in Tkinter window
        frame_result = tk.Frame(app_window, highlightbackground = 'black', highlightthickness = 0)
        frame_graph = tk.Frame(app_window, highlightbackground = 'black', highlightthickness = 0)
        frame_date_input = tk.Frame(app_window, highlightbackground = 'black', highlightthickness = 0)

        #Label and Title to frame with rates values(text field)
        result_label = tk.Label(frame_result, text='Rezultat')
        result = tk.Text(frame_result, height = 10, width = 70)

        #Labels and Title to Input Form Frame
        label_period = tk.Label(frame_date_input, text='Podaj zakres')
        start_date = tk.Entry(frame_date_input)
        start_date_label = tk.Label(frame_date_input, text='Data startu: ')
        end_date = tk.Entry(frame_date_input)
        end_date_label = tk.Label(frame_date_input, text='Data zakończenia: ')
        #Creating Drop-Down menu with currencies and gold
        combo_currencies_label = tk.Label(frame_date_input, text = 'Wybierz walutę: ')
        combo_currencies = ttk.Combobox(frame_date_input, state = "readonly", values = DROP_DOWN_MENU_VALUE)

        #Create atributes to plot graph
        graph_label = tk.Label(frame_result, text='Wykres wartości w czasie')
        fig = Figure(figsize = (5, 4), dpi = 100)
        canvas = FigureCanvasTkAgg(fig, master = frame_graph)

        #Get information from Input Form Frame
        accept_button = tk.Button(
            frame_date_input, 
            text = "OK", 
            command = lambda: self.button_pushed(fig, canvas, combo_currencies.get(), start_date.get(), end_date.get())
            )

        #Creating grid table
        frame_result.grid(column = 0, row = 0, sticky = "NEWS")
        frame_graph.grid(column = 0, row = 1, columnspan = 2, sticky = "NEWS")
        frame_date_input.grid(column = 1, row = 0, sticky = "NEWS")

        #Settings for result label and text field
        result.config(state = 'normal')
        result.config(state = 'disabled')
        result_label.pack()
        result.pack(padx = PADING_VALUE, pady = (0, PADING_VALUE))

        #Entry dates period to plot graph
        start_date.insert(0,'rrrr-mm-dd')
        start_date_label.grid(column = 0, row = 1, padx = PADING_VALUE)
        end_date.insert(0,TODAY.strftime('%Y-%m-%d'))
        end_date.grid(column = 0, row = 4, padx = PADING_VALUE)

        #User choice of currency
        combo_currencies_label.grid(column = 0, row = 5, padx = PADING_VALUE)
        combo_currencies.current(0)

        #Arrangement grids
        label_period.grid(column = 0, row = 0)
        start_date.grid(column = 0, row = 2, padx = PADING_VALUE)
        end_date_label.grid(column = 0, row = 3, padx = PADING_VALUE)
        combo_currencies.grid(column = 0, row = 6, padx = PADING_VALUE)
        accept_button.grid(column = 0, row = 7, pady = PADING_VALUE)

        #Loop prints rates information 
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

        #Create graph space
        graph_label.pack()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx = PADING_VALUE, pady = PADING_VALUE)

        #Start Tkinter loop
        app_window.mainloop()

    def button_pushed(self, figure, canvas, code, start_date, end_date):
        """_summary_

        Args:
            figure (figure): container for all chart elements, which allows them to be organized and managed.
            canvas (canvas): the object responsible for rendering the contents of Figure on the screen
            code (str): three-letter currency code (ISO 4217 standard) or GOLD
            start_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
            end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        """

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
