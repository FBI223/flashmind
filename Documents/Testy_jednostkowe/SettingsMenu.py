import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser, filedialog, messagebox
import sqlite3
import os

class SettingsMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure_styles() # Styl przycisków
        self.create_widgets() # Dodanie elementów okna
        self.place_widgets() # Umiejscowienie elementów

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("Custom.TButton", font=(self.controller.current_font, self.controller.current_font_size))

    def create_widgets(self):
        # Tytuł okna
        self.title_label = tk.Label(self, text="Settings", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)

        # Zmiana motywu
        self.theme_label = tk.Label(self, text="Select Theme:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.theme_combobox = ttk.Combobox(self, values=["clam", "alt", "winnative", "xpnative", "aquativo", "black", "vista", "default"], font=(self.controller.current_font, self.controller.current_font_size))
        self.theme_combobox.set("Select Theme")
        self.set_theme_button = ttk.Button(self, text="Set Theme", style="Custom.TButton", command=self.set_theme)

        # Zmiana tła
        self.color_button = ttk.Button(self, text="Set Background Color", style="Custom.TButton", command=self.set_background_color)

        #Zmiana rozmiaru okna
        self.resolution_label = tk.Label(self, text="Select Resolution:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.resolution_combobox = ttk.Combobox(self, values=[
            "700x700",    # Małe
            "1000x1000",  # Średnie
            "1024x768",   # XGA
            "1280x720",   # HD
            "1280x800",   # WXGA
            "1366x768",   # WXGA
            "1440x900",   # WXGA+
            "1600x900",   # HD+
            "1680x1050",  # WSXGA+
            "1920x1080",  # Full HD
            "1920x1200",  # WUXGA
            "Full Screen" # Pełny ekran
        ], font=(self.controller.current_font, self.controller.current_font_size))
        self.resolution_combobox.set("Select Resolution")
        self.set_resolution_button = ttk.Button(self, text="Set Resolution", style="Custom.TButton", command=self.set_resolution)

        # Zmiana czcionki
        self.font_label = tk.Label(self, text="Select Font:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.font_combobox = ttk.Combobox(self, values=["Arial", "Courier", "Helvetica", "Times", "Verdana", "Comic Sans MS", "Impact", "Lucida Grande", "Palatino", "Tahoma", "Georgia", "Trebuchet MS", "Gill Sans"], font=(self.controller.current_font, self.controller.current_font_size))
        self.font_combobox.set("Select Font")
        self.set_font_button = ttk.Button(self, text="Set Font", style="Custom.TButton", command=self.set_font)

        # Ustawienia domyślne
        self.default_button = ttk.Button(self, text="Set to default", style="Custom.TButton", command=self.set_to_default)

        # Powrót do menu
        self.main_menu_button = ttk.Button(self, text="Main Menu", style="Custom.TButton", command=self.go_to_main_menu)

    def place_widgets(self):
        # Tytuł okna
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')

        # Zmiana motywu
        self.theme_label.place(relx=0.5, rely=0.17, anchor='center')
        self.theme_combobox.place(relx=0.5, rely=0.23, width=250, height=40, anchor='center')
        self.set_theme_button.place(relx=0.5, rely=0.30, width=250, height=40, anchor='center')

        # Zmiana tła
        self.color_button.place(relx=0.5, rely=0.37, width=250, height=40, anchor='center')

        #Zmiana rozmiaru okna
        self.resolution_label.place(relx=0.5, rely=0.45, anchor='center')
        self.resolution_combobox.place(relx=0.5, rely=0.51, width=250, height=40, anchor='center')
        self.set_resolution_button.place(relx=0.5, rely=0.58, width=250, height=40, anchor='center')

        # Zmiana czcionki
        self.font_label.place(relx=0.5, rely=0.66, anchor='center')
        self.font_combobox.place(relx=0.5, rely=0.72, width=250, height=40, anchor='center')
        self.set_font_button.place(relx=0.5, rely=0.79, width=250, height=40, anchor='center')

        # Ustawienia domyślne
        self.default_button.place(relx=0.5, rely=0.86, width=250, height=40, anchor='center')

        # Powrót do menu
        self.main_menu_button.place(relx=0.5, rely=0.93, width=250, height=40, anchor='center')

    def set_background_color(self):
        color_code = colorchooser.askcolor(title="Choose background color")[1]

        if color_code and color_code != "Choose background color" :
            self.controller.set_background_color(color_code)

            # Zapisanie wybranego koloru do bazy danych
            query = "UPDATE Ustawienia SET Kolor = ?"
            self.controller.update_database(query, (str(color_code),))
        else:
            print("No color selected or invalid selection.")

    def go_to_main_menu(self):
        # Reset ComboBox do wartości domyślnych
        self.resolution_combobox.set("Select Resolution")
        self.resolution_combobox.config(font=(self.controller.current_font, self.controller.current_font_size ))

        self.theme_combobox.set("Select Theme")
        self.theme_combobox.config(font=(self.controller.current_font, self.controller.current_font_size ))

        self.font_combobox.set("Select Font")
        self.font_combobox.config(font=(self.controller.current_font, self.controller.current_font_size ))

        self.controller.show_frame("MainMenu")

    def set_font(self):
        selected_font = self.font_combobox.get() # Pobranie wybranej czcionki
        if selected_font and selected_font != "Select Font": # Sprawdzenie czy jakaś czcionka została wybrana
            # Zmiana czcionki
            self.controller.set_font(selected_font)

            # Zapisanie wybranej czcionki do bazy danych
            query = "UPDATE Ustawienia SET Czcionka = ?"
            self.controller.update_database(query, (str(selected_font),))
        else:
            print("No font selected or invalid selection.")

    def set_theme(self):
        selected_theme = self.theme_combobox.get() # Pobranie wybranego motywu
        if selected_theme and selected_theme != "Select Theme": # Sprawdzenie czy jakiś motyw został wybrany
            # Zmiana motywu
            self.controller.set_theme(selected_theme)

            # Zmiana czcionki na tę samą - aby zachować rozmiar przy zmianie motywu
            self.controller.set_font(self.controller.current_font)

            # Zapisanie wybranego motywu w bazie danych
            query = "UPDATE Ustawienia SET Motyw = ?"
            self.controller.update_database(query, (str(selected_theme),))
        else:
            print("No theme selected or invalid selection.")

    def set_resolution(self):
        selected_resolution = self.resolution_combobox.get() # Pobranie wybranego rozmiaru okna
        if selected_resolution and selected_resolution != "Select Resolution": # Sprawdzenie czy jakaś rozdzielczość została wybrana
            # Zmiana rozdzielczości
            if selected_resolution == "Full Screen":
                self.controller.attributes("-fullscreen", True)
            else:
                # Wyjście z trybu pełnoekranowego
                self.controller.state('normal')
                self.controller.attributes("-fullscreen", False)

                self.controller.geometry(selected_resolution)
            
            # Zapisanie wybranej rozdzielczości w bazie danych
            query = "UPDATE Ustawienia SET Rozdzielczosc = ?"
            self.controller.update_database(query, (selected_resolution,))
        else:
            print("No resolution selected or invalid selection.")

    def set_to_default(self):
        # Przywracanie domyślnych ustawień
        self.controller.geometry(self.controller.default_resolution)
        self.controller.set_theme(self.controller.default_theme)
        self.controller.set_font(self.controller.default_font)
        self.controller.set_background_color(self.controller.default_background_color)

        # Zapisanie domyślnych ustawień do bazy danych
        query = "UPDATE Ustawienia SET Rozdzielczosc = ?, Motyw = ?, Czcionka = ?, Kolor = ?"
        self.controller.update_database(query, (self.controller.default_resolution, self.controller.default_theme, self.controller.default_font, self.controller.default_background_color))