import tkinter as tk
from tkinter import ttk
import sqlite3
import os

from StudyFlashcardMenu import StudyFlashcardMenu


class TypeCheckMenu(StudyFlashcardMenu):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #ukrycie widżetów z StudyFlashcardMenu
        self.hide_widgets()
        self.initialize_settings()
        self.setup_timer()
        self.retrieve_flashcards()
        self.create_ui()      

    def initialize_settings(self):
        self.sciezka = os.path.join(os.getcwd(), "fiszki.db")
        self.zbior_in = "A"
        self.kolejnosc_in = "Sequence order"
        self.ilosc_fiszek_in = 10
        self.czas_odpowiedzi_in = 5
        self.ilosc_odwiedzonych = 0

        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "SELECT Zbior, Kolejnosc , Ilosc_Fiszek, Czas_Odpowiedzi FROM Ustawienia_Nauki LIMIT 1"
        cursor.execute(query)
        first_row = cursor.fetchone()
        if first_row:
            z_in , kolejnosc_in , ilosc_fiszek_in, czas_in = first_row
            self.czas_odpowiedzi_in = czas_in
            self.zbior_in = z_in
            self.kolejnosc_in = kolejnosc_in
            self.ilosc_fiszek_in = ilosc_fiszek_in
        else:
            print("blad odczytu w bazie danych")
        db.close()

    def setup_timer(self):
        if self.controller.timer_enabled == 1:
            self.start_timer(self.czas_odpowiedzi_in ,  "points")

    def retrieve_flashcards(self):
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query2 = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? AND ID_Zbioru = ?"
        if self.kolejnosc_in == "Random order":
            query2 = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? ORDER BY RANDOM() LIMIT ?"
        elif self.kolejnosc_in == "Sequence order":
            query2 = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? LIMIT ?"
        elif self.kolejnosc_in == "Priority order":
            query2 = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? ORDER BY Stopien_Przyswojenia ASC LIMIT ?"

        cursor.execute(query2, (str(self.zbior_in), self.ilosc_fiszek_in))
        all_rows = cursor.fetchall()
        db.close()

        self.flashcards = [[row[0], row[1], 0] for row in all_rows]
        self.index_flashcards = 0

    def create_ui(self):
        self.title_label  = ttk.Label(self, text="Type & Check", font=(self.controller.current_font, self.controller.current_big_font_size))
        self.title_label .place(relx=0.5, rely=0.05, anchor='center')

        # Definicja fiszka
        if len(self.flashcards) > 0:
            self.create_ui_flashcard()
        else:
            self.create_ui_warning()

        self.go_back_button = ttk.Button(self, text="Go Back", style="Custom.TButton", command=self.show_study_flashcard_menu )
        self.go_back_button.place(relx=0.5, rely=0.8, width=250, height=40, anchor='center')

        main_menu_button = ttk.Button(self, text="Main Menu", style="Custom.TButton", command=self.show_main_menu )
        main_menu_button.place(relx=0.5, rely=0.90, width=250, height=40, anchor='center')
    
    def create_ui_flashcard(self):
        self.flashcard_label = tk.Label(self, text=self.flashcards[self.index_flashcards][0], wraplength=400, justify="center", font=(self.controller.current_font, self.controller.current_font_size), anchor='center', relief="solid")
        self.flashcard_label.place(relx=0.5, rely=0.23, width=450, height=150, anchor='center')

        #miejsce do wpisywania odpowiedzi
        self.answer_entry = ttk.Entry(self.selection_frame, font=(self.controller.current_font, self.controller.current_font_size))
        self.answer_entry.place(relx=0.5, rely=0.43, width=400, height=40, anchor='center')

        #przycisk do sprawdzania odpowiedzi
        self.check_answer_button = ttk.Button(self, text="Check", style="Custom.TButton", command=self.check_answer)
        self.check_answer_button.place(relx=0.5, rely=0.53, width=250, height=40, anchor='center')

        #przycisk do sprawdzania odpowiedzi
        self.check_answer_button = ttk.Button(self, text="Show Answer", style="Custom.TButton", command=self.show_answer)
        self.check_answer_button.place(relx=0.5, rely=0.6, width=250, height=40, anchor='center')

        #Etykieta do wypisywania Correct/Wrong
        self.correct_wrong_label = ttk.Label(self.selection_frame, font=(self.controller.current_font, self.controller.current_font_size))
        self.correct_wrong_label.place(relx=0.5, rely=0.65, anchor='center')

        # Przyciski do sterowania fiszkami
        self.create_ui_buttons()
        
    def create_ui_buttons(self):
        self.prev_button = ttk.Button(self, text="back", style="Custom.TButton", command=self.show_previous_flashcard)
        self.prev_button.place(relx=0.15, rely=0.7, width=100, height=40, anchor='center')

        self.easy_button = ttk.Button(self, text="Easy", style="Custom.TButton", command=self.easy_method)
        self.easy_button.place(relx=0.35, rely=0.7, width=100, height=40, anchor='center')

        self.easy_button = ttk.Button(self, text="Medium", style="Custom.TButton", command=self.medium_method)
        self.easy_button.place(relx=0.5, rely=0.7, width=100, height=40, anchor='center')

        self.hard_button = ttk.Button(self, text="Hard", style="Custom.TButton", command=self.hard_method)
        self.hard_button.place(relx=0.65, rely=0.7, width=100, height=40, anchor='center')

        self.next_button = ttk.Button(self, text="next", style="Custom.TButton", command=self.show_next_flashcard)
        self.next_button.place(relx=0.85, rely=0.7, width=100, height=40, anchor='center')

    def create_ui_warning(self):
        self.correct_wrong_label = ttk.Label(self.selection_frame, font=(self.controller.current_font, self.controller.current_font_size))
        self.correct_wrong_label.place(relx=0.5, rely=0.5, anchor='center')
        self.correct_wrong_label.config(text="Not enough flashcards in the set", foreground="red")

    def timer_ended(self):
        self.timer_window.destroy()
        self.timer_window = None
        self.timer = None

        self.check_answer()

    def show_study_flashcard_menu(self):
        if hasattr(self, 'timer') and self.timer:
            self.timer.destroy()
            self.timer_window.destroy()
            self.timer = None
            self.timer_window = None

        self.controller.timer_enabled = 0
        self.controller.show_frame("StudyFlashcardMenu")

    def show_main_menu(self):
        if hasattr(self, 'timer') and self.timer:
            self.timer.destroy()
            self.timer_window.destroy()
            self.timer = None
            self.timer_window = None

        self.controller.timer_enabled = 0
        self.controller.show_frame("MainMenu")

    def check_answer(self):
        answer = str(self.answer_entry.get())

        self.destroy_timer()

        if answer == str(self.flashcards[self.index_flashcards][1]) and self.flashcards[self.index_flashcards][2] == 0:
            self.handle_correct_answer()
        elif answer != str(self.flashcards[self.index_flashcards][1]) and self.flashcards[self.index_flashcards][2] == 0:
            self.handle_wrong_answer()

    def destroy_timer(self):
        if hasattr(self, 'timer') and self.timer:
            self.timer.destroy()
            self.timer_window.destroy()
            self.timer = None
            self.timer_window = None

    def handle_correct_answer(self):
        self.ilosc_odwiedzonych += 1
        # Update profile for correct answer
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "UPDATE Profile SET DOBRZE = DOBRZE + 1"
        cursor.execute(query)
        db.commit()
        db.close()

        # Increment proficiency level for correct answer
        inc = 3
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia + ? WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (inc, str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
        db.commit()
        db.close()

        self.correct_wrong_label.config(text="Correct", foreground="green")
        self.flashcards[self.index_flashcards][2] = 1

    def handle_wrong_answer(self):
        self.ilosc_odwiedzonych += 1
        # Update profile for wrong answer
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "UPDATE Profile SET ZLE = ZLE + 1"
        cursor.execute(query)
        db.commit()
        db.close()

        # Decrement proficiency level for wrong answer
        decr = 2
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia - ? WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (decr, str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
        db.commit()

        # Ensure proficiency level doesn't go below zero
        query2 = "SELECT Stopien_Przyswojenia FROM Fiszki WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query2, (str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
        row = cursor.fetchone()
        if row:
            stopien = row
        if stopien[0] < 0:
            query3 = "UPDATE Fiszki SET Stopien_Przyswojenia = 0 WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
            cursor.execute(query3, (str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
            db.commit()

        db.close()

        self.correct_wrong_label.config(text="Wrong", foreground="red")
        self.flashcards[self.index_flashcards][2] = 1

    def clean_input(self):
        self.answer_entry.delete(0, "end")  # Wyczyść pole w Entry
        self.correct_wrong_label.config(text="", foreground="black")

    def show_next_flashcard(self):
        if self.ilosc_odwiedzonych < len(self.flashcards):
            if self.index_flashcards + 1 >= len(self.flashcards):
                self.index_flashcards = 0
            else:
                self.index_flashcards += 1
            while self.flashcards[self.index_flashcards][2] == 1:
                if self.index_flashcards + 1 >= len(self.flashcards):
                    self.index_flashcards = 0
                else:
                    self.index_flashcards += 1

            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][0])
            if self.controller.timer_enabled == 1 :
                self.start_timer(self.czas_odpowiedzi_in , "points" )
        else:
            self.controller.show_frame("StudyFlashcardMenu")
            if hasattr(self, 'timer') and self.timer:
                self.timer.destroy()
                self.timer_window.destroy()
                self.timer = None
                self.timer_window = None
        self.clean_input()

    def show_previous_flashcard(self):
        if self.ilosc_odwiedzonych < len(self.flashcards):
            if self.index_flashcards - 1  >= 0:
                self.index_flashcards -= 1
            else:
                self.index_flashcards = len(self.flashcards) - 1
            while self.flashcards[self.index_flashcards][2] == 1:
                if self.index_flashcards - 1  >= 0:
                    self.index_flashcards -= 1
                else:
                    self.index_flashcards = len(self.flashcards) - 1

            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][0])

            if self.controller.timer_enabled == 1 :
                self.start_timer(self.czas_odpowiedzi_in , "points")
        else:
            self.controller.show_frame("StudyFlashcardMenu")
        self.clean_input()

    def show_answer(self):
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.insert(0, self.flashcards[self.index_flashcards][1])
        if self.flashcards[self.index_flashcards][2] == 0:
            self.stop_timer()

            self.ilosc_odwiedzonych += 1
            decr = 1
            sciezka = os.path.join(os.getcwd(), "fiszki.db")
            db = sqlite3.connect(sciezka)
            cursor = db.cursor()
            query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia - ? WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
            cursor.execute(query, (decr, str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
            db.commit()
            query2 = "SELECT Stopien_Przyswojenia FROM Fiszki WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
            cursor.execute(query2, (str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
            row = cursor.fetchone()
            if row:
                stopien = row
            if stopien[0] < 0:
                query3 = "UPDATE Fiszki SET Stopien_Przyswojenia = 0 WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
                cursor.execute(query3, (str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
                db.commit()
            db.close()
        self.flashcards[self.index_flashcards][2] = 1

    def easy_method(self):
        if self.flashcards[self.index_flashcards][2] == 0:
            self.ilosc_odwiedzonych += 1
        self.flashcards[self.index_flashcards][2] = 1
        inc = 1
        sciezka = os.path.join(os.getcwd(), "fiszki.db")
        db = sqlite3.connect(sciezka)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia + ? WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (inc, str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
        db.commit()
        db.close()
        self.show_next_flashcard()

    def medium_method(self):
        if self.flashcards[self.index_flashcards][2] == 0:
            self.ilosc_odwiedzonych += 1
        self.flashcards[self.index_flashcards][2] = 1
        self.show_next_flashcard()

    def hard_method(self):
        if self.flashcards[self.index_flashcards][2] == 0:
            self.ilosc_odwiedzonych += 1
        self.flashcards[self.index_flashcards][2] = 1
        sciezka = os.path.join(os.getcwd(), "fiszki.db")
        db = sqlite3.connect(sciezka)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = 0 WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
        db.commit()
        db.close()
        self.show_next_flashcard()

