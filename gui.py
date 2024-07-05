from rates_for_today import get_today_exchange_rate, get_today_gold_rate
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graph
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

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
        frame_date_input = tk.Frame(app_window, highlightbackground = 'black', highlightthickness = 1)

        #Label and Title to frame with rates values(text field)
        result_label = tk.Label(frame_result, text='Rezultat')
        result = tk.Text(frame_result, height = 10, width = 70)

        #Labels and Title to Input Form Frame
        label_period = tk.Label(frame_date_input, text='Podaj zakres')
        self.start_date_entry = tk.Entry(frame_date_input)
        start_date_label = tk.Label(frame_date_input, text='Data startu: ')
        self.end_date_entry = tk.Entry(frame_date_input)
        end_date_label = tk.Label(frame_date_input, text='Data zakończenia: ')
        buttons_choice_1D = tk.Button(frame_date_input, text="1D", 
                                      command = lambda: self.period_button_pushed(combo_currencies.get(), 1))
        buttons_choice_1M = tk.Button(frame_date_input, text="1M", 
                                      command = lambda: self.period_button_pushed(combo_currencies.get(), 30))
        buttons_choice_3M = tk.Button(frame_date_input, text="3M")
        buttons_choice_6M = tk.Button(frame_date_input, text="6M")
        #Creating Drop-Down menu with currencies and gold
        combo_currencies_label = tk.Label(frame_date_input, text = 'Wybierz walutę: ')
        combo_currencies = ttk.Combobox(frame_date_input, state = "readonly", values = DROP_DOWN_MENU_VALUE)

        #Create atributes to plot graph
        graph_label = tk.Label(frame_result, text='Wykres wartości w czasie')
        self.fig = Figure(figsize = (5.0, 7.5), dpi = 100)
        self.canvas = FigureCanvasTkAgg(self.fig, master = frame_graph)


        #Get information from Input Form Frame
        accept_button = tk.Button(
            frame_date_input, 
            text = "OK", 
            command = lambda: self.OK_button_pushed(combo_currencies.get(), self.start_date_entry.get(), self.end_date_entry.get())
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
        self.start_date_entry.insert(0,'rrrr-mm-dd')
        self.start_date_entry.bind('<FocusIn>', self.on_entry_click)
        self.start_date_entry.bind('<FocusOut>', self.on_focusout)
        self.start_date_entry.bind('<KeyPress>', self.on_key_press)
        self.start_date_entry.bind('<KeyRelease>', self.on_key_release)
        start_date_label.grid(column = 0, columnspan = 5, row = 1, padx = PADING_VALUE)
        self.end_date_entry.insert(0,TODAY.strftime('%Y-%m-%d'))
        self.end_date_entry.grid(column = 0, columnspan = 5, row = 4, padx = PADING_VALUE)

        #User choice of currency
        combo_currencies_label.grid(column = 0, columnspan = 5, row = 5, padx = PADING_VALUE)
        combo_currencies.current(0)

        #Arrangement grids
        label_period.grid(column = 0, columnspan = 5, row = 0)
        self.start_date_entry.grid(column = 0, columnspan = 5, row = 2, padx = PADING_VALUE)
        end_date_label.grid(column = 0, columnspan = 5, row = 3, padx = PADING_VALUE)
        combo_currencies.grid(column = 0, columnspan = 5, row = 6, padx = PADING_VALUE)
        accept_button.grid(column = 0, columnspan = 5, row = 7, pady = PADING_VALUE)
        buttons_choice_1D.grid(column = 0, row = 8)
        buttons_choice_1M.grid(column = 1, row = 8)
        buttons_choice_3M.grid(column = 2, row = 8)
        buttons_choice_6M.grid(column = 3, row = 8)

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
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx = PADING_VALUE, pady = PADING_VALUE)

        #Start Tkinter loop
        app_window.mainloop()

    def OK_button_pushed(self, currencies_code, start_date, end_date):
        """_summary_

        Args:
            code (str): three-letter currency code (ISO 4217 standard) or GOLD
            start_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
            end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        """

        if currencies_code == 'ZŁOTO':
            key_date, value_rate = graph.create_graph_gold(start_date, end_date)
            self.fig.clear()
            gold_plot = self.fig.add_subplot(111)
            gold_plot.plot(key_date, value_rate, marker = '*')
            gold_plot.tick_params(axis='x', rotation=45)
            gold_plot.set_ylabel('Wartość')
            self.canvas.draw()
        else:
            key_date, value_rate = graph.create_graph_currencies(currencies_code, start_date, end_date)
            self.fig.clear()
            currency_plot = self.fig.add_subplot(111)
            currency_plot.plot(key_date, value_rate, marker = '*')
            currency_plot.tick_params(axis='x', rotation=45)
            currency_plot.set_ylabel('Wartość')
            self.canvas.draw()

    def on_entry_click(self, event):
        """Removes the default text on the first click"""
        if event.widget.get() == 'rrrr-mm-dd':
            event.widget.delete(0, tk.END)
            event.widget.insert(0, '')

    def on_focusout(self, event):
        """Restores the default text if the field is empty"""
        if event.widget.get() == '':
            event.widget.delete(0, tk.END)
            event.widget.insert(0, 'rrrr-mm-dd')

    def on_key_press(self, event):
        """Check that only numbers are entered and len of date are equal 10"""
        if not event.char.isdigit():
            return 'break'
        pos = event.widget.index(tk.INSERT)
        if pos == 10:
            return 'break'

    def on_key_release(self, event):
        """Adding a dash in the appropriate places in the date 'yyyy-mm-dd'"""
        pos = event.widget.index(tk.INSERT)
        # Automatic hyphen traversal
        if pos in [4, 7]:
            event.widget.insert(pos, '-')


    def period_button_pushed(self, code, day_period):
        """_summary_

        Args:
            code (str): three-letter currency code (ISO 4217 standard) or GOLD
            start_date (str): date in YYYY-MM-DD format (ISO 8601 standard), choice from period buttons
            end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        """
        start_date_period = datetime.strftime((datetime.today() - timedelta(days = day_period)), '%Y-%m-%d')
        print(start_date_period)
        self.start_date_entry.delete(0, tk.END)
        self.start_date_entry.insert(0, start_date_period)
        self.OK_button_pushed(code, self.start_date_entry.get(), self.end_date_entry.get())
