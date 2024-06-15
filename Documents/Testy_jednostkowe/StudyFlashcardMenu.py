import tkinter as tk
from tkinter import ttk
import os
from timer_factory import create_timer

class StudyFlashcardMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure_styles()  # Konfiguracja stylów
        self.create_study_widgets()  # Utworzenie widżetów
        self.place_study_widgets()  # Umiejscowienie widżetów

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("Custom.TButton", font=(self.controller.current_font, self.controller.current_font_size))

    def create_study_widgets(self):
        # Utworzenie elementów okna
        self.selection_frame = tk.Frame(self)
        self.selection_frame.configure(bg=self.controller.bg_color)

        # Tytuł okna
        self.title_label = tk.Label(self.selection_frame, text="Study Flashcards", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)

        # Combobox wyboru zestawu
        sets = self.controller.query_database("SELECT Nazwa_zbioru FROM Zbiory")
        set_names = [row[0] for row in sets]
        self.set_combobox = ttk.Combobox(self.selection_frame, values=set_names, font=(self.controller.current_font, self.controller.current_font_size))
        self.set_combobox.set("Select Set")

        # Combobox wyboru kolejności
        self.order_combobox = ttk.Combobox(self.selection_frame, values=["Random order", "Sequence order", "Priority order"], font=(self.controller.current_font, self.controller.current_font_size))
        self.order_combobox.set("Select order")

        # Przycisk show & hide
        self.show_hide_button = ttk.Button(self.selection_frame, text="show & hide", style="Custom.TButton", command=self.switch_to_show_hide_menu)

        # Przycisk type & check
        self.type_check_button = ttk.Button(self.selection_frame, text="type & check", style="Custom.TButton", command=self.switch_to_type_check_menu)

        # Przycisk drag & drop
        self.drag_drop_button = ttk.Button(self.selection_frame, text="drag & drop", style="Custom.TButton", command=self.switch_to_drag_drop_menu)

        # Licznik ilości fiszek
        self.amount_flashcards_label = tk.Label(self.selection_frame, text="Number of Flashcards", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.decrease_amount_button = ttk.Button(self.selection_frame, text="-", command=self.decrease_amount_flashcard)
        self.counter_amount_flashcards = tk.IntVar(value=10)
        self.counter_amount_label = tk.Label(self.selection_frame, textvariable=self.counter_amount_flashcards, font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.increase_amount_button = ttk.Button(self.selection_frame, text="+", command=self.increase_amount_flashcard)

        # Licznik czasu odpowiedzi
        self.time_answer_label = tk.Label(self.selection_frame, text="Time to answer", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.decrease_time_button = ttk.Button(self.selection_frame, text="-", command=self.decrease_time_answer)
        self.counter_time_answer = tk.IntVar(value=10)
        self.counter_time_label = ttk.Label(self.selection_frame, textvariable=self.counter_time_answer, font=(self.controller.current_font, self.controller.current_font_size))
        self.increase_time_button = ttk.Button(self.selection_frame, text="+", command=self.increase_time_answer)

        # Checkbox do używania timera
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.selection_frame, text="Using Timer?", variable=self.checkbox_var, command=self.on_checkbox_toggled, bg=self.controller.bg_color, activebackground=self.controller.bg_color)

        # Przycisk powrotu do głównego menu
        self.back_button = ttk.Button(self.selection_frame, text="Main Menu", style="Custom.TButton", command=lambda: self.controller.show_frame("MainMenu"))

    def place_study_widgets(self):
        # Umiejscowienie elementów okna
        self.selection_frame.pack(fill="both", expand=True)
        
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.set_combobox.place(relx=0.5, rely=0.2, width=250, height=40, anchor='center')
        self.order_combobox.place(relx=0.5, rely=0.3, width=250, height=40, anchor='center')
        
        self.show_hide_button.place(relx=0.5, rely=0.55, width=250, height=40, anchor='center')
        self.type_check_button.place(relx=0.5, rely=0.65, width=250, height=40, anchor='center')
        self.drag_drop_button.place(relx=0.5, rely=0.75, width=250, height=40, anchor='center')
        
        self.amount_flashcards_label.place(relx=0.32, rely=0.4, anchor='center')
        self.decrease_amount_button.place(relx=0.27, rely=0.45, width=30, height=30, anchor='center')
        self.counter_amount_label.place(relx=0.32, rely=0.45, anchor='center')
        self.increase_amount_button.place(relx=0.37, rely=0.45, width=30, height=30, anchor='center')
        
        self.time_answer_label.place(relx=0.68, rely=0.4, anchor='center')
        self.decrease_time_button.place(relx=0.63, rely=0.45, width=30, height=30, anchor='center')
        self.counter_time_label.place(relx=0.68, rely=0.45, anchor='center')
        self.increase_time_button.place(relx=0.73, rely=0.45, width=30, height=30, anchor='center')
        
        self.checkbox.place(relx=0.68, rely=0.37, anchor='center')
        self.back_button.place(relx=0.5, rely=0.9, width=250, height=40, anchor='center')

    def switch_to_show_hide_menu(self):
        # Przełącz na ShowHideMenu
        if self.validate_comboboxes():
            self.update_settings()
            self.controller.show_frame("ShowHideMenu")
        else:
            self.show_incorrect_selection_message()

    def switch_to_type_check_menu(self):
        # Przełącz na TypeCheckMenu
        if self.validate_comboboxes():
            self.update_settings()
            self.controller.show_frame("TypeCheckMenu")
        else:
            self.show_incorrect_selection_message()

    def switch_to_drag_drop_menu(self):
        # Przełącz na DragDropMenu
        if self.validate_comboboxes():
            self.update_settings()
            self.controller.show_frame("DragDropMenu")
        else:
            self.show_incorrect_selection_message()

    def validate_comboboxes(self):
        # Sprawdzenie, czy comboboxy są wypełnione
        set_selected = str(self.set_combobox.get())
        order_selected = str(self.order_combobox.get())

        sets = self.controller.query_database("SELECT Nazwa_zbioru FROM Zbiory")
        set_names = str([row[0] for row in sets])
        order_names = ["Random order", "Sequence order", "Priority order"]

        return str(set_selected) in str(set_names) and order_selected in order_names

    def update_settings(self):
        # Aktualizacja ustawień w bazie danych
        query = "UPDATE Ustawienia_Nauki SET Zbior = ?, Kolejnosc = ?, Ilosc_Fiszek = ?, Czas_Odpowiedzi = ?"
        params = (str(self.set_combobox.get()), str(self.order_combobox.get()), str(self.counter_amount_flashcards.get()), str(self.counter_time_answer.get()))
        self.controller.update_database(query, params)

    def show_incorrect_selection_message(self):
        # Wyświetlenie komunikatu o niepoprawnym wyborze
        incorrect_selection_label = ttk.Label(self.selection_frame, text="Incorrect selection. Please fill all fields.", font=("Arial", 20), foreground="red")
        incorrect_selection_label.place(relx=0.5, rely=0.82, anchor='center')
        self.after(3000, incorrect_selection_label.destroy)

    def decrease_amount_flashcard(self):
        # Zmniejszenie ilości fiszek
        current_value = self.counter_amount_flashcards.get()
        if current_value > 1:
            self.counter_amount_flashcards.set(current_value - 1)

    def increase_amount_flashcard(self):
        # Zwiększenie ilości fiszek
        current_value = self.counter_amount_flashcards.get()
        self.counter_amount_flashcards.set(current_value + 1)

    def decrease_time_answer(self):
        # Zmniejszenie czasu odpowiedzi
        current_value = self.counter_time_answer.get()
        if current_value > 0:
            self.counter_time_answer.set(current_value - 1)

    def increase_time_answer(self):
        # Zwiększenie czasu odpowiedzi
        current_value = self.counter_time_answer.get()
        self.counter_time_answer.set(current_value + 1)

    def on_checkbox_toggled(self):
        # Przełącznik timera
        if self.checkbox_var.get():
            self.controller.timer_enabled = 1
        else:
            self.controller.timer_enabled = 0

    def start_timer(self, duration, mode):
        # Rozpocznij timer
        if hasattr(self, 'timer_window') and self.timer_window:
            self.timer.destroy()
            self.timer_window.destroy()
        self.timer_window = tk.Toplevel(self)
        self.timer_window.title("Timer")
        self.timer = create_timer(self.timer_window, duration, self.timer_ended, mode)  # Użycie fabryki

    def timer_ended(self):
        # Zakończ timer
        self.timer_window.destroy()
        self.timer_window = None
        self.timer = None

    def stop_timer(self):
        # Zatrzymaj timer
        if hasattr(self, 'timer') and self.timer:
            self.timer.destroy()
            self.timer_window.destroy()
            self.timer = None
            self.timer_window = None

    def update_data_before_switch(self):
        # Zaktualizuj dane przed przełączeniem
        self.order_flashcard = self.order_combobox.get()

    def switch_ShowHideMenu(self):
        # Przełącz do ShowHideMenu
        if self.if_comboboxes_are_filled():
            self.update_data_before_switch()
            query = "UPDATE Ustawienia_Nauki SET Zbior = ?, Kolejnosc = ?, Ilosc_Fiszek = ?, Czas_Odpowiedzi = ?"
            params = (
                self.set_combobox.get(),
                self.order_combobox.get(),
                self.counter_amount_flashcards.get(),
                self.counter_time_answer.get()
            )
            self.controller.update_database(query, params)
            self.controller.show_frame("ShowHideMenu")
        else:
            self.incorrect_selection()

    def switch_TypeCheckMenu(self):
        # Przełącz do TypeCheckMenu
        if self.if_comboboxes_are_filled():
            self.update_data_before_switch()
            query = "UPDATE Ustawienia_Nauki SET Zbior = ?, Kolejnosc = ?, Ilosc_Fiszek = ?, Czas_Odpowiedzi = ?"
            params = (
                self.set_combobox.get(),
                self.order_combobox.get(),
                self.counter_amount_flashcards.get(),
                self.counter_time_answer.get()
            )
            self.controller.update_database(query, params)
            self.controller.show_frame("TypeCheckMenu")
        else:
            self.incorrect_selection()

    def switch_DragDropMenu(self):
        # Przełącz do DragDropMenu
        if self.if_comboboxes_are_filled():
            self.update_data_before_switch()
            query = "UPDATE Ustawienia_Nauki SET Zbior = ?, Kolejnosc = ?, Ilosc_Fiszek = ?, Czas_Odpowiedzi = ?"
            params = (
                self.set_combobox.get(),
                self.order_combobox.get(),
                self.counter_amount_flashcards.get(),
                self.counter_time_answer.get()
            )
            self.controller.update_database(query, params)
            self.controller.show_frame("DragDropMenu")
        else:
            self.incorrect_selection()

    def incorrect_selection(self):
        # Błędny wybór
        incorrect_selection_label = ttk.Label(self, text="Incorrect selection. Please fill all fields.", font=("Arial", 20), foreground="red")
        incorrect_selection_label.place(relx=0.5, rely=0.82, anchor='center')
        self.after(3000, incorrect_selection_label.destroy)

    def if_comboboxes_are_filled(self):
        # Sprawdź, czy combobox'y są wypełnione
        query = "SELECT Nazwa_zbioru FROM Zbiory"
        result = self.controller.query_database(query)
        set_names = [row[0] for row in result]

        order_names = ["Random order", "Sequence order", "Priority order"]
        can_proceed = self.set_combobox.get() in set_names and self.order_combobox.get() in order_names

        return can_proceed

    def hide_widgets(self):
        self.title_label.place_forget()
        self.set_combobox.place_forget()
        self.order_combobox.place_forget()
        self.show_hide_button.place_forget()
        self.type_check_button.place_forget()
        self.drag_drop_button.place_forget()
        self.back_button.place_forget()
        self.amount_flashcards_label.place_forget()
        self.decrease_amount_button.place_forget()
        self.counter_amount_label.place_forget()
        self.increase_amount_button.place_forget()
        self.time_answer_label.place_forget()
        self.decrease_time_button.place_forget()
        self.counter_time_label.place_forget()
        self.increase_time_button.place_forget()
        self.checkbox.place_forget()

    def decrease_amount_flashcard(self):
        # Zmniejsz liczbę fiszek
        current_value = self.counter_amount_flashcards.get()
        if current_value > 1:
            self.counter_amount_flashcards.set(current_value - 1)

    def increase_amount_flashcard(self):
        # Zwiększ liczbę fiszek
        current_value = self.counter_amount_flashcards.get()
        self.counter_amount_flashcards.set(current_value + 1)

    def decrease_time_answer(self):
        # Zmniejsz czas odpowiedzi
        current_value = self.counter_time_answer.get()
        
        if current_value > 1:
            self.counter_time_answer.set(current_value - 1)

    def increase_time_answer(self):
        # Zwiększ czas odpowiedzi
        current_value = self.counter_time_answer.get()
        self.counter_time_answer.set(current_value + 1)