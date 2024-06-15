import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import random


from StudyFlashcardMenu import StudyFlashcardMenu



class DragDropMenu(StudyFlashcardMenu):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.controller = controller
        self.initialize_variables()
        self.hide_widgets()
        self.load_settings_from_db()
        self.setup_timer()
        self.load_flashcards_from_db()
        self.create_widgets()
        
    def initialize_variables(self):
        self.db_path = os.path.join(os.getcwd(), "fiszki.db")
        self.czy_przydzielone_pkt = 0
        self.time_over = 0
        self.zbior_in = "A"
        self.kolejnosc_in = "Sequence order"
        self.ilosc_fiszek_in = 10
        self.czas_odpowiedzi_in = 5
        self.ilosc_odwiedzonych = 0

    def load_settings_from_db(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = "SELECT Zbior, Kolejnosc , Ilosc_Fiszek, Czas_Odpowiedzi FROM Ustawienia_Nauki LIMIT 1"
        cursor.execute(query)
        first_row = cursor.fetchone()
        if first_row:
            self.zbior_in, self.kolejnosc_in, self.ilosc_fiszek_in, self.czas_odpowiedzi_in = first_row
        else:
            print("blad odczytu w bazie danych")
        db.close()

    def setup_timer(self):
        if self.controller.timer_enabled == 1:
            self.start_timer(self.czas_odpowiedzi_in, "points")

    def load_flashcards_from_db(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? AND ID_Zbioru = ?"
        if self.kolejnosc_in == "Random order":
            query = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? ORDER BY RANDOM() LIMIT ?"
        elif self.kolejnosc_in == "Sequence order":
            query = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? LIMIT ?"
        elif self.kolejnosc_in == "Priority order":
            query = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? ORDER BY Stopien_Przyswojenia ASC LIMIT ?"

        cursor.execute(query, (self.zbior_in, self.ilosc_fiszek_in))
        all_rows = cursor.fetchall()
        self.flashcards = [[row[0], row[1], 0] for row in all_rows]
        self.index_flashcards = 0
        db.close()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Drag & Drop", font=(self.controller.current_font, self.controller.current_big_font_size))
        self.title_label.place(relx=0.5, rely=0.05, anchor='center')

        if len(self.flashcards) > 2:
            self.correct_wrong_label = ttk.Label(self.selection_frame, font=(self.controller.current_font, self.controller.current_font_size))
            self.correct_wrong_label.place(relx=0.5, rely=0.74, anchor='center')

            self.check_answer_button = ttk.Button(self, text="Check", style="Custom.TButton", command=self.show_answer)
            self.check_answer_button.place(relx=0.25, rely=0.81, width=100, height=40, anchor='center')

            self.drag_drop_frame = tk.Frame(self, width=700, height=400)
            self.drag_drop_frame.place(relx=0.5, rely=0.40, anchor='center')

            self.create_flashcard_buttons()

            self.next_button = ttk.Button(self, text="next", style="Custom.TButton", command=self.show_next_flashcard)
            self.next_button.place(relx=0.75, rely=0.81, width=100, height=40, anchor='center')
        else:
            self.warning_label = ttk.Label(self.selection_frame, font=(self.controller.current_font, self.controller.current_font_size))
            self.warning_label.place(relx=0.5, rely=0.5, anchor='center')
            self.warning_label.config(text="Not enough flashcards in the set", foreground="red")

        self.go_back_button = ttk.Button(self, text="Go Back", style="Custom.TButton", command=self.show_study_flashcard_menu)
        self.go_back_button.place(relx=0.5, rely=0.88, width=250, height=40, anchor='center')

        self.main_menu_button = ttk.Button(self, text="Main Menu", style="Custom.TButton", command=self.show_main_menu)
        self.main_menu_button.place(relx=0.5, rely=0.95, width=250, height=40, anchor='center')

    def timer_ended(self):
        self.time_over = 1
        self.timer_window.destroy()
        self.timer_window = None
        self.timer = None

        self.show_answer()

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
        ile_zaznaczonych, pyt_odp = self.collect_selected_answers()

        if self.time_over == 1:
            self.handle_time_over(ile_zaznaczonych, pyt_odp)
            self.czy_przydzielone_pkt = 1
        else:
            self.handle_normal_time(ile_zaznaczonych, pyt_odp)
            
    def collect_selected_answers(self):
        ile_zaznaczonych = 0
        pyt_odp = []

        for x in self.answer_buttons:
            temp = x.cget("text")
            temp = str(temp)
            if "\n=\n" in temp:
                ile_zaznaczonych += 1
                parts = temp.split("\n=\n")
                if len(parts) == 2:
                    pyt_odp.append([parts[0], parts[1], 0])  # 0 oznacza złą odpowiedź, 1 oznacza dobrze udzielona odpowiedź

        return ile_zaznaczonych, pyt_odp

    def handle_time_over(self, ile_zaznaczonych, pyt_odp):
        if self.czy_przydzielone_pkt == 0 and ile_zaznaczonych < 3:
            self.correct_wrong_label.config(text="Times over", foreground="red")
            self.update_database_for_incorrect_answers()
        elif ile_zaznaczonych == 3 and self.czy_przydzielone_pkt == 0:
            self.destroy_timer()
            pyt_odp_z_bazy = self.fetch_correct_answers_from_db(pyt_odp)
            ile_ok = self.compare_answers(pyt_odp, pyt_odp_z_bazy)
            self.correct_wrong_label.config(text="You got " + str(ile_ok) + " correct answers", foreground="blue")
            self.update_points(pyt_odp, pyt_odp_z_bazy)

    def handle_normal_time(self, ile_zaznaczonych, pyt_odp):
        if ile_zaznaczonych < 3:
            self.correct_wrong_label.config(text="Match other flashcards", foreground="orange")
        elif ile_zaznaczonych == 3:
            self.destroy_timer()
            pyt_odp_z_bazy = self.fetch_correct_answers_from_db(pyt_odp)
            ile_ok = self.compare_answers(pyt_odp, pyt_odp_z_bazy)
            self.correct_wrong_label.config(text="You got " + str(ile_ok) + " correct answers", foreground="blue")
            self.update_points(pyt_odp, pyt_odp_z_bazy)

    def destroy_timer(self):
        if hasattr(self, 'timer') and self.timer:
            self.timer.destroy()
            self.timer_window.destroy()
            self.timer = None
            self.timer_window = None

    def fetch_correct_answers_from_db(self, pyt_odp):
        pyt_odp_z_bazy = []
        for i in range(3):
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()
            query = "SELECT Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? AND Definicja = ? LIMIT 1"
            cursor.execute(query, (self.zbior_in, pyt_odp[i][0]))
            first_row = cursor.fetchone()
            pyt_odp_z_bazy.append([pyt_odp[i][0], first_row[0]])
            db.close()
        return pyt_odp_z_bazy

    def compare_answers(self, pyt_odp, pyt_odp_z_bazy):
        ile_ok = 0
        for i in range(3):
            if str(pyt_odp_z_bazy[i][1]) == str(pyt_odp[i][1]):
                pyt_odp[i][2] = 1  # dobrze odpowiedzielismy na pytanie
                ile_ok += 1
        return ile_ok

    def update_points(self, pyt_odp, pyt_odp_z_bazy):
        if self.czy_przydzielone_pkt == 0:
            for i in range(3):
                if pyt_odp[i][2] == 0:
                    self.increment_incorrect_count()
                    self.decrease_proficiency(pyt_odp_z_bazy[i])
                elif pyt_odp[i][2] == 1:
                    self.increment_correct_count()
                    self.increase_proficiency(pyt_odp_z_bazy[i])
            self.czy_przydzielone_pkt = 1

    def increment_incorrect_count(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = "UPDATE Profile SET ZLE = ZLE + 1"
        cursor.execute(query)
        db.commit()
        db.close()

    def increment_correct_count(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = "UPDATE Profile SET DOBRZE = DOBRZE + 1"
        cursor.execute(query)
        db.commit()
        db.close()

    def decrease_proficiency(self, answer):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia - 1 WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (answer[0], answer[1], self.zbior_in))
        db.commit()
        query2 = "SELECT Stopien_Przyswojenia FROM Fiszki WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query2, (answer[0], answer[1], self.zbior_in))
        row = cursor.fetchone()
        if row and row[0] < 0:
            query3 = "UPDATE Fiszki SET Stopien_Przyswojenia = 0 WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
            cursor.execute(query3, (answer[0], answer[1], self.zbior_in))
            db.commit()
        db.close()

    def increase_proficiency(self, answer):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia + 1 WHERE Definicja = ? AND Odpowiedz = ? AND ID_Zbioru = ?"
        cursor.execute(query, (answer[0], answer[1], self.zbior_in))
        db.commit()
        db.close()

    def update_database_for_incorrect_answers(self):
        for i in range(3):
            self.increment_incorrect_count()
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()
            query = "UPDATE Fiszki SET Stopien_Przyswojenia = Stopien_Przyswojenia - 1 WHERE Definicja = ? AND ID_Zbioru = ?"
            cursor.execute(query, (self.flashcards[self.index_flashcards + i][0], self.zbior_in))
            db.commit()
            query2 = "SELECT Stopien_Przyswojenia FROM Fiszki WHERE Definicja = ? AND ID_Zbioru = ?"
            cursor.execute(query2, (self.flashcards[self.index_flashcards + i][0], self.zbior_in))
            row = cursor.fetchone()
            if row and row[0] < 0:
                query3 = "UPDATE Fiszki SET Stopien_Przyswojenia = 0 WHERE Definicja = ? AND ID_Zbioru = ?"
                cursor.execute(query3, (self.flashcards[self.index_flashcards + i][0], self.zbior_in))
                db.commit()
            db.close()

    def show_next_flashcard(self):
        if self.czy_przydzielone_pkt == 0:
            self.correct_wrong_label.config(text="Match other flashcards or Check", foreground="orange")
        elif self.czy_przydzielone_pkt == 1:
            for button in self.answer_and_definition_buttons:
                button.place_forget()

            self.index_flashcards += 3
            self.czy_przydzielone_pkt = 0

            if self.index_flashcards + 2 < len( self.flashcards ):
                self.create_flashcard_buttons()
                self.time_over = 0
                self.correct_wrong_label.config(text="", foreground="red")

                if self.controller.timer_enabled == 1 :
                    self.start_timer(self.czas_odpowiedzi_in, "points")
            else:
                self.controller.show_frame("StudyFlashcardMenu")
                if hasattr(self, 'timer') and self.timer:
                    self.timer.destroy()
                    self.timer_window.destroy()
                    self.timer = None
                    self.timer_window = None

    def show_answer(self):
        if self.czy_przydzielone_pkt == 0:
            self.check_answer()
            if self.czy_przydzielone_pkt == 1:
                self.answer_and_definition_buttons = []

                answer_positions = [(350, 65), (350, 200), (350, 335)]
                if self.czy_przydzielone_pkt == 1: # jesli juz przydzielilismy punkty to pokazujemy tylko poprawne odpowiedzi
                    for definition_button in self.definition_buttons:
                        definition_button.place_forget()
                    for answer_button in self.answer_buttons:
                        answer_button.place_forget()
                    for i in range(3):
                        odp = str(self.flashcards[self.index_flashcards + i][0]) + "\n=\n" + str(self.flashcards[self.index_flashcards + i][1])
                        answer_and_definition_button = tk.Button(self.drag_drop_frame, text=odp, wraplength=350, justify="center" , width=60 , relief="solid")
                        x_ans, y_ans = answer_positions[i]
                        answer_and_definition_button.place(x=x_ans, y=y_ans, anchor='center')
                        answer_and_definition_button.name = odp
                        self.answer_and_definition_buttons.append(answer_and_definition_button)

    def create_flashcard_buttons(self):
        self.definition_buttons = []
        self.answer_buttons = []
        self.matched = [[None, None], [None, None], [None, None]]
        self.original_positions = {}

        # Użyjemy listy pozycji do losowania
        definition_positions = [(180, 65), (180, 200), (180, 335)]  # Przesunięte w lewo
        answer_positions = [(520, 65), (520, 200), (520, 335)]      # Przesunięte w prawo

        # Losowe indeksy
        random.shuffle(definition_positions)
        random.shuffle(answer_positions)

        for i in range(3):
            definition_button = tk.Button(self.drag_drop_frame, text=self.flashcards[self.index_flashcards + i][0], wraplength=250, justify="center", width=35, relief="solid")
            x_def, y_def = definition_positions[i]
            definition_button.place(x=x_def, y=y_def, anchor='center')
            definition_button.name = self.flashcards[self.index_flashcards + i][0]
            definition_button.index = i
            self.definition_buttons.append(definition_button)
            self.bind_drag(definition_button, definition_button.name)
            self.bind_drop(definition_button, definition_button.name)

            answer_button = tk.Button(self.drag_drop_frame, text=self.flashcards[self.index_flashcards + i][1], wraplength=250, justify="center", width=35, relief="solid")
            x_ans, y_ans = answer_positions[i]
            answer_button.place(x=x_ans, y=y_ans, anchor='center')
            answer_button.name = self.flashcards[self.index_flashcards + i][1]
            answer_button.index = i
            self.answer_buttons.append(answer_button)

            self.matched[i][1] = answer_button.name
            self.original_positions[definition_button.name] = (x_def, y_def)
            self.original_positions[answer_button.name] = (x_ans, y_ans)

            answer_button.bind("<Button-1>", self.on_reset)

    def bind_drag(self, widget, name):
        widget.bind("<ButtonPress-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.name = name

    def bind_drop(self, widget, name):
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.name = name

    def on_drag_start(self, event):
        widget = event.widget
        widget.startX = event.x
        widget.startY = event.y

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y

        if x < 40:
            x = 40
        elif x + widget.winfo_width() > self.drag_drop_frame.winfo_width():
            x = self.drag_drop_frame.winfo_width() - widget.winfo_width()

        if y < 20:
            y = 20
        elif y + widget.winfo_height() > self.drag_drop_frame.winfo_height():
            y = self.drag_drop_frame.winfo_height() - widget.winfo_height()

        widget.place_configure(relx=0.155, rely=0.085)
        if (self.time_over == 0):
            if abs(x - widget.winfo_x()) + abs(y - widget.winfo_y()) > 20:
                widget.place(x=x, y=y)
        else:
            widget.place_forget()

    def on_drop(self, event):
        dropped_element = event.widget
        for button in self.answer_buttons:
            if self.is_overlapping(button, dropped_element):
                dropped_index = dropped_element.index
                target_index = button.index

                # Jeśli odpowiedź jest już zmatchowana, odłącz poprzednią definicję
                if self.matched[target_index][0] is not None:
                    previous_definition_name = self.matched[target_index][0]
                    previous_definition_button = next(b for b in self.definition_buttons if b.name == previous_definition_name)
                    previous_definition_pos = self.original_positions[previous_definition_name]
                    previous_definition_button.place(x=previous_definition_pos[0], y=previous_definition_pos[1], anchor='center')
                    previous_definition_button.config(text=previous_definition_name)

                self.matched[target_index][0] = dropped_element.name
                dropped_element.place_forget()
                button.config(text=f"{dropped_element.name}\n=\n{button.name}", wraplength=300, justify="center", width=45, relief="solid")

    def is_overlapping(self, widget1, widget2):
        x1, y1, w1, h1 = widget1.winfo_x(), widget1.winfo_y(), widget1.winfo_width(), widget1.winfo_height()
        x2, y2, w2, h2 = widget2.winfo_x(), widget2.winfo_y(), widget2.winfo_width(), widget2.winfo_height()

        # Oblicz współrzędne obszaru nachodzenia
        overlap_x1 = max(x1, x2)
        overlap_y1 = max(y1, y2)
        overlap_x2 = min(x1 + w1, x2 + w2)
        overlap_y2 = min(y1 + h1, y2 + h2)

        # Oblicz wymiary obszaru nachodzenia
        overlap_width = max(0, overlap_x2 - overlap_x1)
        overlap_height = max(0, overlap_y2 - overlap_y1)
        overlap_area = overlap_width * overlap_height

        # Oblicz minimalny wymagany obszar nachodzenia (30% dla każdego przycisku)
        widget1_area = w1 * h1
        widget2_area = w2 * h2
        required_overlap_area = 0.3 * min(widget1_area, widget2_area)

        # Sprawdź, czy obszar nachodzenia jest co najmniej 30% obszaru mniejszego z przycisków
        return overlap_area >= required_overlap_area

    def on_reset(self, event):
        button = event.widget
        answer_name = button.name
        answer_index = button.index

        if self.matched[answer_index][0] is not None:
            definition_name = self.matched[answer_index][0]
            definition_button = next(b for b in self.definition_buttons if b.name == definition_name)

            # Przywróć przycisk definicji do jego początkowej pozycji
            definition_pos = self.original_positions[definition_name]
            definition_button.place(x=definition_pos[0], y=definition_pos[1], anchor='center')
            definition_button.config(text=definition_name, wraplength=250, justify="center", width=35, relief="solid")

            # Przywróć przycisk odpowiedzi do jego oryginalnego tekstu
            button.config(text=answer_name, wraplength=250, justify="center", width=35, relief="solid")

            # Usuń powiązanie z 'matched'
            self.matched[answer_index][0] = None
        else:
            print("This answer button is not matched with any definition button.")