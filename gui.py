from NBP_API import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FormatStrFormatter
from matplotlib import ticker
import customtkinter as CT
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from mplcursors import cursor

PADING_VALUE = 10 #offset from the axis
DROP_DOWN_MENU_VALUE = ["USD", "EUR", "CHF", "GBP", "ZŁOTO"]
TODAY = datetime.today()

class GUI:
    def __init__(self) -> None:
        #Open Tkinter window
        self.app_window = CT.CTk()
        self.app_window.title('Kursy walut')

        self._create_frame_date_input()
        self._create_frame_result()
        self._create_frame_graph()
        self._create_frame_exchange()

        #Creating grid table
        self.frame_result.grid(column = 0, row = 1, sticky = "NEWS")
        self.frame_graph.grid(column = 1, row = 0, rowspan = 3, sticky = "NEWS")
        self.frame_date_input.grid(column = 0, row = 0, sticky = "NEWS")
        self.frame_exchange.grid(column = 0, row = 2, stick = "NEWS")

        #first column is const, second column is resizable
        self.app_window.rowconfigure(0, weight=1)
        self.app_window.rowconfigure(1, weight=1)
        self.app_window.rowconfigure(2, weight=1)
        self.app_window.columnconfigure(0, weight=0)
        self.app_window.columnconfigure(1, weight=1)

        self._bind_functions()

        self._set_default_values()
        
        #Start Tkinter loop
        self.app_window.mainloop()

    def _create_frame_date_input(self):
        self.frame_date_input = CT.CTkFrame(master=self.app_window, border_width = 1)

        #Labels and Title to Input Form Frame
        label_period = CT.CTkLabel(self.frame_date_input, text='PODAJ ZAKRES')
        self.start_date_entry = CT.CTkEntry(self.frame_date_input)
        start_date_label = CT.CTkLabel(self.frame_date_input, text='Data startu: ')
        self.end_date_entry = CT.CTkEntry(self.frame_date_input)
        end_date_label = CT.CTkLabel(self.frame_date_input, text='Data zakończenia: ')

        # Create quick buttons for basic periods
        buttons_choice_1d = CT.CTkButton(self.frame_date_input, text="1D", 
                                      command = lambda: self.period_button_pushed(self.combo_currencies.get(), 1), width=40)
        buttons_choice_1m = CT.CTkButton(self.frame_date_input, text="1M", 
                                      command = lambda: self.period_button_pushed(self.combo_currencies.get(), 30), width=40)
        buttons_choice_3m = CT.CTkButton(self.frame_date_input, text="3M", 
                                      command = lambda: self.period_button_pushed(self.combo_currencies.get(), 90), width=40)
        buttons_choice_6m = CT.CTkButton(self.frame_date_input, text="6M", 
                                      command = lambda: self.period_button_pushed(self.combo_currencies.get(), 180), width=40)

        #Creating Drop-Down menu with currencies and gold
        combo_currencies_label = CT.CTkLabel(self.frame_date_input, text = 'Wybierz walutę: ')
        self.combo_currencies = CT.CTkComboBox(self.frame_date_input, state = "readonly", values = DROP_DOWN_MENU_VALUE)

        #Get information from Input Form Frame
        accept_button = CT.CTkButton(
            self.frame_date_input, 
            text = "OK", 
            command = lambda: self.OK_button_pushed(self.combo_currencies.get(), self.start_date_entry.get(), self.end_date_entry.get())
            )

        COLSPAN = 4

        # Place all elements
        label_period.grid(column = 0, columnspan = COLSPAN, row = 0, padx = PADING_VALUE, pady = PADING_VALUE, sticky="EW")
        start_date_label.grid(column = 0, columnspan = COLSPAN, row = 1, padx = PADING_VALUE)
        self.start_date_entry.grid(column = 0, columnspan = COLSPAN, row = 2, padx = PADING_VALUE)
        end_date_label.grid(column = 0, columnspan = COLSPAN, row = 3, padx = PADING_VALUE)
        self.end_date_entry.grid(column = 0, columnspan = COLSPAN, row = 4, padx = PADING_VALUE)
        combo_currencies_label.grid(column = 0, columnspan = COLSPAN, row = 5, padx = PADING_VALUE)
        self.combo_currencies.grid(column = 0, columnspan = COLSPAN, row = 6, padx = PADING_VALUE)
        accept_button.grid(column = 0, columnspan = COLSPAN, row = 7, pady = PADING_VALUE)
        buttons_choice_1d.grid(column = 0, row = 8)
        buttons_choice_1m.grid(column = 1, row = 8)
        buttons_choice_3m.grid(column = 2, row = 8)
        buttons_choice_6m.grid(column = 3, row = 8)

    def _create_frame_result(self):

        self.frame_result = CT.CTkFrame(master=self.app_window, border_width = 1)

        #Label and Title to frame with rates values(text field)
        result_label = CT.CTkLabel(self.frame_result, text='Rezultat')
        result = CT.CTkTextbox(self.frame_result, height = 200, width = 370)

        #Settings for result label and text field
        result.configure(state = 'normal')
        result.configure(state = 'disabled')
        result_label.pack(padx = PADING_VALUE, pady = PADING_VALUE)
        result.pack(padx = PADING_VALUE, pady = (0, PADING_VALUE))

        #Loop prints rates information 
        basic_codes = ['EUR', 'USD', 'GBP', 'CHF']
        currencies, currencies_date = get_today_exchange_rate(basic_codes)
        gold, gold_date = get_today_gold_rate()

        result.configure(state='normal')

        result.insert(tk.INSERT, f'Kurs złota na dzień: {gold_date}\n')
        result.insert(tk.INSERT, f'Wartość złota 1g - {gold:0.2f} zł.\n')
        result.insert(tk.INSERT, f'Kursy walut na dzień: {currencies_date}\n')

        for currency in currencies:
            result.insert(tk.INSERT, f'{currency['currency'].upper()}, wynosi 1{currency['code']} - {currency['mid']:.2f}zł.\n')
        result.configure(state='disabled')

    def _create_frame_graph(self):

        self.frame_graph = CT.CTkFrame(master=self.app_window, border_width = 1)

        #Create atributes to plot graph
        graph_label = CT.CTkLabel(self.frame_graph, text='Wykres wartości w czasie')
        self.fig = Figure(figsize = (7.0, 8.0), dpi = 100)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_graph)

        #Create graph space
        graph_label.pack(padx = PADING_VALUE, pady = PADING_VALUE)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx = PADING_VALUE, pady = PADING_VALUE)

    def _create_frame_exchange(self):

        self.frame_exchange = CT.CTkFrame(master=self.app_window, border_width = 1)

        #exchange frame
        exchange_label = CT.CTkLabel(self.frame_exchange, text = "Przelicz walutę")
        confirm_button = CT.CTkButton(self.frame_exchange, text="Przelicz", width=60)
        currency_quantity_left = CT.CTkEntry(self.frame_exchange)
        combo_currencies_left = CT.CTkComboBox(self.frame_exchange, state = "readonly", values = DROP_DOWN_MENU_VALUE)
        currency_quantity_right = CT.CTkEntry(self.frame_exchange)
        combo_currencies_right = CT.CTkComboBox(self.frame_exchange, state = "readonly", values = DROP_DOWN_MENU_VALUE)
        exchange_label.grid(row =0, columnspan = 4, sticky = "NEWS")
        confirm_button.grid(row = 2, columnspan = 4, sticky = "NEWS")
        currency_quantity_left.grid(row = 1, column = 0, sticky = "NEWS")
        combo_currencies_left.grid(row = 1, column = 1, sticky = "NEWS")
        currency_quantity_right.grid(row = 1, column = 2, sticky = "NEWS")
        combo_currencies_right.grid(row = 1, column = 3, sticky = "NEWS")

    def _bind_functions(self):
        self.start_date_entry.bind('<FocusIn>', self.on_entry_click)
        self.start_date_entry.bind('<FocusOut>', self.on_focusout)
        self.start_date_entry.bind('<KeyPress>', self.on_key_press)
        self.start_date_entry.bind('<KeyRelease>', self.on_key_release)

    def _set_default_values(self):
        self.combo_currencies.set("USD")
        self.start_date_entry.insert(0,'rrrr-mm-dd')
        self.end_date_entry.insert(0, TODAY.strftime('%Y-%m-%d'))

    def OK_button_pushed(self, currencies_code, start_date, end_date):
        """_summary_

        Args:
            code (str): three-letter currency code (ISO 4217 standard) or GOLD
            start_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
            end_date (str): date in YYYY-MM-DD format (ISO 8601 standard)
        """
        if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
            self.wrong_date_popup()
            return
        
        self.fig.clear()
        if currencies_code == 'ZŁOTO':
            self.key_date, value_rate = prepare_gold_data(start_date, end_date)
            gold_plot = self.fig.add_subplot(111)
            gold_plot.plot(self.key_date, value_rate, marker = 'o')
            gold_plot.tick_params(axis='x', rotation=45)
            gold_plot.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
            gold_plot.xaxis.set_major_locator(ticker.AutoLocator())
            gold_plot.grid(visible=True, linewidth=1)
            gold_plot.set_ylabel('Kurs za 1g [PLN]')
            gold_plot.format_coord = self.format_coords
            cursor(gold_plot, hover=True)
            self.canvas.draw()
        else:
            self.key_date, value_rate = prepare_currencies_data(currencies_code, start_date, end_date)
            currency_plot = self.fig.add_subplot(111)
            currency_plot.plot(self.key_date, value_rate, marker = 'o')
            currency_plot.tick_params(axis='x', rotation=45)
            currency_plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            currency_plot.xaxis.set_major_locator(ticker.AutoLocator())
            currency_plot.grid(visible=True, linewidth=1)
            currency_plot.set_ylabel(f'Kurs za 1 {currencies_code} - PLN')
            currency_plot.format_coord = self.format_coords
            cursor(currency_plot, hover=True)
            self.canvas.draw()

    def format_coords(self, x, y):
        idx = round(x)
        return f"Data={self.key_date[idx]}, Kurs={y:.2f}PLN"

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
        if event.keysym == "BackSpace":
            return
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
            end_date (str): date in YYYY-MM-DD format (ISO 8601 standard), today
        """
        start_date_period = datetime.strftime((datetime.today() - timedelta(days = day_period)), '%Y-%m-%d')
        self.start_date_entry.delete(0, tk.END)
        self.start_date_entry.insert(0, start_date_period)
        self.OK_button_pushed(code, self.start_date_entry.get(), self.end_date_entry.get())

    def center_window_to_display(self, Screen: CT.CTk, width: int, height: int, scale_factor: float = 1.0):
        """Centers the window to the main display/monitor"""
        screen_width = Screen.winfo_screenwidth()
        screen_height = Screen.winfo_screenheight()
        x = int(((screen_width/2) - (width/2)) * scale_factor)
        y = int(((screen_height/2) - (height/1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"

    def wrong_date_popup(self):
        messagebox.showwarning(title="Błąd", message="Błędna wartość daty.")
