import tkinter as tk
from tkinter import ttk
import sqlite3
import os

class ProfileMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.setup_frames() # Okno dla potwierdzenia resetu profilu
        self.configure_styles() # Styl przycisków
        self.load_data()  # Załaduj dane
        self.create_widgets()  # Dodanie elementów okna
        self.place_widgets()  # Umiejscowienie elementów

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("Custom.TButton", font=(self.controller.current_font, self.controller.current_font_size))

    def setup_frames(self):
        # Okno ze statystykami
        self.profile_frame = tk.Frame(self)
        self.profile_frame.pack(fill="both", expand=True)
        self.profile_frame.configure(bg=self.controller.bg_color)

        # Okno z resetem
        self.delete_frame = tk.Frame(self)
        self.delete_frame.configure(bg=self.controller.bg_color)

    def load_data(self):
        self.flashcard_count = 0
        self.set_count = 0
        self.correct_in = 0
        self.incorrect_in = 0
        self.exp_points_in = 0

        query = "SELECT DOBRZE, ZLE FROM Profile LIMIT 1"
        result = self.controller.query_database(query)
        if result:
            self.correct_in, self.incorrect_in = result[0]

        query = 'SELECT COUNT(*) FROM Fiszki'
        result = self.controller.query_database(query)
        self.flashcard_count = result[0][0] or 0

        query = 'SELECT COUNT(*) FROM Zbiory'
        result = self.controller.query_database(query)
        self.set_count = result[0][0] or 0

        query = 'SELECT SUM(Stopien_Przyswojenia) FROM Fiszki'
        result = self.controller.query_database(query)
        self.exp_points_in = result[0][0] or 0

    def create_widgets(self):
        # Tytuł okna
        self.title_label = tk.Label(self.profile_frame, text="Profile Statistics", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)

        # Statystyki
        self.stat1_label = tk.Label(self.profile_frame, text="Number of flashcards: " + str(self.flashcard_count), font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.stat2_label = tk.Label(self.profile_frame, text="Number of sets: " + str(self.set_count), font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.stat3_label = tk.Label(self.profile_frame, text="Level: " + str(self.calculate_level()), font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.stat4_label = tk.Label(self.profile_frame, text="Number of exp points: " + str(self.exp_points_in), font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.stat5_label = tk.Label(self.profile_frame, text="Correct answers: " + str(self.correct_in), font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.stat6_label = tk.Label(self.profile_frame, text="Incorrect answers: " + str(self.incorrect_in), font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)

        # Ustawienia przypomnienia
        self.profile_label = tk.Label(self.profile_frame, text="Set Reminder:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.profile_combobox = ttk.Combobox(self.profile_frame, values=["no reminder", "20s", "1m", "5m", "10m", "30m", "1h", "2h", "5h", "12h", "1d", "2d", "7d"], font=(self.controller.current_font, self.controller.current_font_size))
        self.profile_combobox.set("Set interval")
        self.profile_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))

        # Przyciski
        self.ok_button = ttk.Button(self.profile_frame, text="Ok", style="Custom.TButton", command=self.set_reminder)
        self.reset_button = ttk.Button(self.profile_frame, text="Reset Profile", style="Custom.TButton", command=self.reset_profile)
        self.main_menu_button = ttk.Button(self.profile_frame, text="Main Menu", style="Custom.TButton", command=self.go_to_main_menu)

        # Potwierdzenie resetu
        self.Sure = tk.Label(self.delete_frame, text="Are you sure you want to reset your stats?", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.Yes_Button = ttk.Button(self.delete_frame, text="Yes", style="Custom.TButton", command=self.Yes_command)
        self.No_Button = ttk.Button(self.delete_frame, text="No", style="Custom.TButton", command=self.No_command)

    def place_widgets(self):
        # Tytuł okna
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')

        # Statystyki
        self.stat1_label.place(relx=0.5, rely=0.2, anchor='center')
        self.stat2_label.place(relx=0.5, rely=0.27, anchor='center')
        self.stat3_label.place(relx=0.5, rely=0.34, anchor='center')
        self.stat4_label.place(relx=0.5, rely=0.41, anchor='center')
        self.stat5_label.place(relx=0.5, rely=0.48, anchor='center')
        self.stat6_label.place(relx=0.5, rely=0.55, anchor='center')

        # Ustawienia przypomnienia
        self.profile_label.place(relx=0.5, rely=0.62, anchor='center')
        self.profile_combobox.place(relx=0.5, rely=0.68, width=250, height=40, anchor='center')

        # Przyciski
        self.ok_button.place(relx=0.5, rely=0.75, width=250, height=40, anchor='center')
        self.reset_button.place(relx=0.5, rely=0.82, width=250, height=40, anchor='center')
        self.main_menu_button.place(relx=0.5, rely=0.89, width=250, height=40, anchor='center')

        # Potwierdzenie resetu
        self.Sure.place(relx=0.5, rely=0.4, anchor='center')
        self.Yes_Button.place(relx=0.3, rely=0.5, width=250, height=40, anchor='center')
        self.No_Button.place(relx=0.7, rely=0.5, width=250, height=40, anchor='center')
        self.Sure.place_forget()
        self.Yes_Button.place_forget()
        self.No_Button.place_forget()

    def calculate_level(self):
        exp_points = self.exp_points_in
        if exp_points < 50:
            return "Flashcard Novice"
        elif exp_points < 100:
            return "Knowledge Explorer"
        elif exp_points < 250:
            return "Word Hunter"
        elif exp_points < 500:
            return "Memory Guardian"
        elif exp_points < 1000:
            return "Retention Master"
        elif exp_points < 2500:
            return "Language Wizard"
        else:
            return "Flashcard Guru"

    def set_reminder(self):
        values = ["no reminder", "20s", "1m", "5m", "10m", "30m", "1h", "2h", "5h", "12h", "1d", "2d", "7d"]
        #format_daty = "%Y-%m-%d %H:%M:%S.%f"

        if self.profile_combobox.get() in values :
            selected_interval = self.profile_combobox.get()
            query = "UPDATE Profile SET INTERWAL = ?"
            self.controller.update_database(query, (selected_interval, ))

    def reset_profile(self):
        self.profile_frame.forget()
        self.delete_frame.pack(fill="both", expand=True)
        self.Sure.place(relx=0.5, rely=0.4, anchor='center')
        self.Yes_Button.place(relx=0.3, rely=0.5, width=250, height=40, anchor='center')
        self.No_Button.place(relx=0.7, rely=0.5, width=250, height=40, anchor='center')

    def Yes_command(self):
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = 0"
        self.controller.update_database(query, ())

        query2 = "UPDATE Profile SET DOBRZE = 0"
        self.controller.update_database(query2, ())

        query3 = "UPDATE Profile SET ZLE = 0"
        self.controller.update_database(query3, ())

        self.delete_frame.pack_forget()
        self.controller.show_frame("ProfileMenu")

    def No_command(self):
        self.delete_frame.pack_forget()
        self.controller.show_frame("ProfileMenu")

    def go_to_main_menu(self):
        self.profile_combobox.set("Set interval")
        self.profile_combobox.config(font=(self.controller.current_font, self.controller.current_font_size ))
        self.controller.show_frame("MainMenu")