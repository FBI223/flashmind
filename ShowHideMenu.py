
from tkinter import ttk
import sqlite3
import os

from StudyFlashcardMenu import StudyFlashcardMenu

class ShowHideMenu(StudyFlashcardMenu):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.sciezka = os.path.join(os.getcwd(), "fiszki.db")

        self.flashcards = []
        self.zbior_in = "A"
        self.czas_odpowiedzi_in = 5
        self.kolejnosc_in = "Sequence order"
        self.ilosc_fiszek_in = 10

        self.hide_widgets()
        self.load_settings()
        self.load_flashcards()
        self.create_widgets()
        self.place_widgets()

        # ustaw timer
        if self.controller.timer_enabled == 1:
            self.start_timer( self.czas_odpowiedzi_in  , "def" )

    def load_settings(self):
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "SELECT Zbior, Kolejnosc, Ilosc_Fiszek, Czas_Odpowiedzi FROM Ustawienia_Nauki LIMIT 1"
        cursor.execute(query)
        first_row = cursor.fetchone()
        if first_row:
            self.zbior_in, self.kolejnosc_in, self.ilosc_fiszek_in, self.czas_odpowiedzi_in = first_row
        else:
            print("Błąd odczytu z bazy danych")
        db.close()

    def load_flashcards(self):
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
        
        self.flashcards = [[row[0], row[1]] for row in all_rows]
        self.index_flashcards = 0

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Show & Hide", font=(self.controller.current_font, self.controller.current_big_font_size))
        
        if len(self.flashcards) > 0:
            self.flashcard_label = ttk.Label(self, text=self.flashcards[self.index_flashcards][0], wraplength=280, justify="center", anchor='center', font=(self.controller.current_font, self.controller.current_font_size), relief="solid")
            self.flashcard_label.bind("<Button-1>", self.swap_flashcard)

            self.prev_button = ttk.Button(self, text="back", style="Custom.TButton", command=self.show_previous_flashcard)
            self.next_button = ttk.Button(self, text="next", style="Custom.TButton", command=self.show_next_flashcard)
            self.easy_button = ttk.Button(self, text="Easy", style="Custom.TButton", command=self.easy_method)
            self.medium_button = ttk.Button(self, text="Medium", style="Custom.TButton", command=self.medium_method)
            self.hard_button = ttk.Button(self, text="Hard", style="Custom.TButton", command=self.hard_method)
        else:
            self.correct_wrong_label = ttk.Label(self.selection_frame, font=(self.controller.current_font, self.controller.current_font_size))
            self.correct_wrong_label.config(text="Not enough flashcards in the set", foreground="red")

        self.go_back_button = ttk.Button(self, text="Go Back", style="Custom.TButton", command=self.show_study_flashcard_menu)
        self.main_menu_button = ttk.Button(self, text="Main Menu", style="Custom.TButton", command=self.show_main_menu)

    def place_widgets(self):
        self.title_label.place(relx=0.5, rely=0.05, anchor='center')
        
        if len(self.flashcards) > 0:
            self.flashcard_label.place(relx=0.5, rely=0.4, width=300, height=300, anchor='center')
            self.prev_button.place(relx=0.2, rely=0.4, width=100, height=40, anchor='center')
            self.next_button.place(relx=0.8, rely=0.4, width=100, height=40, anchor='center')
            self.easy_button.place(relx=0.3, rely=0.67, width=100, height=40, anchor='center')
            self.medium_button.place(relx=0.5, rely=0.67, width=100, height=40, anchor='center')
            self.hard_button.place(relx=0.7, rely=0.67, width=100, height=40, anchor='center')
        else:
            self.correct_wrong_label.place(relx=0.5, rely=0.5, anchor='center')

        self.go_back_button.place(relx=0.5, rely=0.8, width=250, height=40, anchor='center')
        self.main_menu_button.place(relx=0.5, rely=0.9, width=250, height=40, anchor='center')


    def timer_ended(self):
        self.timer_window.destroy()
        self.timer_window = None
        self.timer = None

        self.show_next_flashcard()

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

    def swap_flashcard(self, event=None):
        button_text = self.flashcard_label.cget("text")
        if button_text == self.flashcards[self.index_flashcards][0]:
            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][1])
        else:
            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][0])

    def show_next_flashcard(self):
        if self.index_flashcards + 1 < len(self.flashcards):
            self.index_flashcards += 1
            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][0])
        else:
            self.index_flashcards = 0
            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][0])

        if self.controller.timer_enabled == 1:
            self.start_timer(self.czas_odpowiedzi_in, "def")

    def show_previous_flashcard(self):
        if self.index_flashcards - 1 >= 0:
            self.index_flashcards -= 1
            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][0])
        else:
            self.index_flashcards = len(self.flashcards) - 1
            self.flashcard_label.config(text=self.flashcards[self.index_flashcards][0])

        if self.controller.timer_enabled == 1:
            self.start_timer(self.czas_odpowiedzi_in, "def")

    def easy_method(self):
        inc = 2
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia + ? WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (inc, str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
        db.commit()
        db.close()
        self.show_next_flashcard()

    def medium_method(self):
        decr = 1
        db = sqlite3.connect(self.sciezka)
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
        self.show_next_flashcard()

    def hard_method(self):
        db = sqlite3.connect(self.sciezka)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = 0 WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (str(self.flashcards[self.index_flashcards][0]), str(self.flashcards[self.index_flashcards][1]), str(self.zbior_in)))
        db.commit()
        db.close()
        self.show_next_flashcard()
