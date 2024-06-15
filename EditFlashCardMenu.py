import tkinter as tk
from tkinter import ttk
import sqlite3
import os

class EditFlashCardMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.current_set = ""
        self.current_flashcard = ""

        self.configure_styles()  # Styl przycisków
        self.configure_frames()  # Ustawienie ramek
        self.create_widgets()  # Dodanie elementów okna
        self.place_widgets()  # Umiejscowienie elementów
        self.load_set_names()  # Załadowanie nazw zbiorów

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("Custom.TButton", font=(self.controller.current_font, self.controller.current_font_size))
    
    def configure_frames(self):
        self.selection_frame = tk.Frame(self)
        self.selection_frame.pack(fill="both", expand=True)
        self.edit_frame = tk.Frame(self)

        self.selection_frame.configure(bg=self.controller.bg_color)
        self.edit_frame.configure(bg=self.controller.bg_color)

    def create_widgets(self):
        self.create_selection_frame_widgets()
        self.create_edit_frame_widgets()

    def create_selection_frame_widgets(self):
        # Tytuł okna
        self.selection_title_label = tk.Label(self.selection_frame, text="Select Set to Edit", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)

        self.set_combobox = ttk.Combobox(self.selection_frame, font=(self.controller.current_font, self.controller.current_font_size))
        self.set_combobox.set("Select Set")
        self.set_combobox.bind("<<ComboboxSelected>>", self.update_entry_from_combobox)
        self.next_button = ttk.Button(self.selection_frame, text="Next", style="Custom.TButton", command=self.show_edit_frame)
        self.selection_main_menu_button = ttk.Button(self.selection_frame, text="Main Menu", style="Custom.TButton", command=lambda: self.controller.show_frame("MainMenu"))

    def create_edit_frame_widgets(self):
        # Tytuł okna
        self.edit_title_label = tk.Label(self.edit_frame, text="Edit Flashcards", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)

        self.flashcard_combobox = ttk.Combobox(self.edit_frame, font=(self.controller.current_font, self.controller.current_font_size))
        self.flashcard_combobox.set("Select Flashcard")
        self.flashcard_combobox.bind("<<ComboboxSelected>>", self.update_entry_from_combobox)
        self.front_label = tk.Label(self.edit_frame, text="Front:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.front_entry = ttk.Entry(self.edit_frame)
        self.back_label = tk.Label(self.edit_frame, text="Back:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.back_entry = ttk.Entry(self.edit_frame)
        self.add_button = ttk.Button(self.edit_frame, text="Add", style="Custom.TButton", command=self.add_flashcard)
        self.delete_button = ttk.Button(self.edit_frame, text="Delete", style="Custom.TButton", command=self.delete_flashcard)
        self.modify_button = ttk.Button(self.edit_frame, text="Update", style="Custom.TButton", command=self.modify_flashcard)
        self.go_back_button = ttk.Button(self.edit_frame, text="Go Back", style="Custom.TButton", command=self.show_selection_frame)
        self.edit_main_menu_button = ttk.Button(self.edit_frame, text="Main Menu", style="Custom.TButton", command=self.go_to_main_menu)

    def place_widgets(self):
        self.place_selection_frame_widgets()
        self.place_edit_frame_widgets()

    def place_selection_frame_widgets(self):
        self.selection_title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.set_combobox.place(relx=0.5, rely=0.4, width=250, height=40, anchor='center')
        self.next_button.place(relx=0.5, rely=0.5, width=250, height=40, anchor='center')
        self.selection_main_menu_button.place(relx=0.5, rely=0.85, width=250, height=40, anchor='center')

    def place_edit_frame_widgets(self):
        self.edit_title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.flashcard_combobox.place(relx=0.5, rely=0.2, width=250, height=40, anchor='center')
        self.front_label.place(relx=0.5, rely=0.25, anchor='center')
        self.front_entry.place(relx=0.5, rely=0.3, width=250, height=40, anchor='center')
        self.back_label.place(relx=0.5, rely=0.35, anchor='center')
        self.back_entry.place(relx=0.5, rely=0.4, width=250, height=40, anchor='center')
        self.add_button.place(relx=0.5, rely=0.5, width=250, height=40, anchor='center')
        self.delete_button.place(relx=0.5, rely=0.57, width=250, height=40, anchor='center')
        self.modify_button.place(relx=0.5, rely=0.64, width=250, height=40, anchor='center')
        self.go_back_button.place(relx=0.5, rely=0.71, width=250, height=40, anchor='center')
        self.edit_main_menu_button.place(relx=0.5, rely=0.85, width=250, height=40, anchor='center')

    def load_set_names(self):
        query = "SELECT Nazwa_zbioru FROM Zbiory ORDER BY Nazwa_zbioru ASC"
        result = self.controller.query_database(query)
        set_names = [row[0] for row in result]
        self.set_combobox.config(values=set_names)

    def too_many_characters(self):
        incorrect_selection_label = ttk.Label(self, text="The maximum number of characters is 200", font=("Arial", 18), foreground="red")
        incorrect_selection_label.place(relx=0.5, rely=0.45, anchor='center')
        self.after(3000, incorrect_selection_label.destroy)  # Usunięcie wiadomości po czasie

    def go_to_main_menu(self):
        self.back_entry.delete(0, tk.END)
        self.front_entry.delete(0, tk.END)
        self.set_combobox.set("Select Set")
        self.set_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))
        self.flashcard_combobox.set("Select Flashcard")
        self.flashcard_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))
        self.controller.show_frame("MainMenu")
        
    def update_entry_from_combobox(self, event):
        selected_flashcard = str(self.flashcard_combobox.get())
        if selected_flashcard and selected_flashcard != "Select Flashcard":
            query = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE Definicja = ?"
            result = self.controller.query_database(query, (str(selected_flashcard),))
            if result:
                front, back = result[0]
                self.front_entry.delete(0, tk.END)
                self.front_entry.insert(0, front)
                self.back_entry.delete(0, tk.END)
                self.back_entry.insert(0, back)
        else:
            # Wyczyść pola, jeśli nie wybrano poprawnego flashcard
            self.front_entry.delete(0, tk.END)
            self.back_entry.delete(0, tk.END)

    def show_edit_frame(self):
        selected_set = str(self.set_combobox.get())
        self.current_set = selected_set
        query = "SELECT Nazwa_zbioru FROM Zbiory"
        result = self.controller.query_database(query)
        set_names = [row[0] for row in result]
        if str(selected_set) in str(set_names):
            self.selection_frame.pack_forget()
            self.edit_frame.pack(fill="both", expand=True)
            self.load_flashcards(selected_set)

    def show_selection_frame(self):
        self.front_entry.delete(0, tk.END)
        self.back_entry.delete(0, tk.END)
        self.set_combobox.set("Select Set")
        self.set_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))
        self.flashcard_combobox.set("Select Flashcard")
        self.flashcard_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))
        self.edit_frame.pack_forget()
        self.selection_frame.pack(fill="both", expand=True)

    def load_flashcards(self, selected_set):
        query = "SELECT Definicja FROM Fiszki WHERE ID_Zbioru = ? ORDER BY Definicja ASC"
        result = self.controller.query_database(query, (str(selected_set),))
        flashcards = [row[0] for row in result]
        self.flashcard_combobox['values'] = flashcards

    def add_flashcard(self):
        curr_set = str(self.set_combobox.get())
        front_text = str(self.front_entry.get())
        back_text = str(self.back_entry.get())
        if len(front_text) <= 200 and len(back_text) <= 200:
            query = "SELECT Definicja, Odpowiedz FROM Fiszki WHERE Definicja = ? AND ID_Zbioru = ? LIMIT 1"
            result = self.controller.query_database(query, (str(front_text), str(curr_set)))
            if not result and front_text and back_text:
                query = "INSERT INTO Fiszki (ID_Zbioru, Definicja, Odpowiedz) VALUES (?, ?, ?)"
                self.controller.update_database(query, (str(curr_set), str(front_text), str(back_text)))
            self.reset_entries()
            self.load_flashcards(curr_set)
        else:
            self.too_many_characters()

    def delete_flashcard(self):
        curr_set = str(self.set_combobox.get())
        selected_flashcard = str(self.flashcard_combobox.get())
        query = "SELECT Definicja FROM Fiszki WHERE Definicja = ? AND ID_Zbioru = ? LIMIT 1"
        result = self.controller.query_database(query, (str(selected_flashcard), str(curr_set)))
        if result:
            query = "DELETE FROM Fiszki WHERE Definicja = ? AND ID_Zbioru = ?"
            self.controller.update_database(query, (str(selected_flashcard), str(curr_set)))
        self.reset_entries()
        self.load_flashcards(curr_set)

    def modify_flashcard(self):
        curr_set = str(self.set_combobox.get()) # Aktualnie wybrany zbior
        selected_flashcard = str(self.flashcard_combobox.get())
        front_text = str(self.front_entry.get())
        back_text = str(self.back_entry.get())

        if len(front_text) <= 150 and len(back_text) <= 150:
            if front_text and not back_text:  # tylko front wypełniony
                self.update_front_only(curr_set, selected_flashcard, front_text)
            elif not front_text and back_text:  # tylko back wypełniony
                self.update_back_only(curr_set, selected_flashcard, back_text)
            elif front_text and back_text:  # oba wypełnione
                self.update_front_and_back(curr_set, selected_flashcard, front_text, back_text)
            
            self.reset_entries()
            self.load_flashcards(curr_set)
        else:
            self.too_many_characters()

    def update_back_only(self, curr_set, selected_flashcard, back_text):
        query = "UPDATE Fiszki SET Odpowiedz = ? WHERE ID_Zbioru = ? AND Definicja = ?"
        self.controller.update_database(query, (str(back_text), str(curr_set), str(selected_flashcard)))

    def update_front_only(self, curr_set, selected_flashcard, front_text):
        query = "SELECT Definicja FROM Fiszki WHERE Definicja = ? AND ID_Zbioru = ? LIMIT 1"
        result = self.controller.query_database(query, (str(front_text), str(curr_set)))
        if not result:
            query = "UPDATE Fiszki SET Definicja = ? WHERE ID_Zbioru = ? AND Definicja = ?"
            self.controller.update_database(query, (str(front_text), str(curr_set), str(selected_flashcard)))

    def update_front_and_back(self, curr_set, selected_flashcard, front_text, back_text):
        query = "SELECT Definicja FROM Fiszki WHERE Definicja = ? AND ID_Zbioru = ? LIMIT 1"
        result = self.controller.query_database(query, (str(front_text), str(curr_set)))
        if result:
            query = "UPDATE Fiszki SET Odpowiedz = ? WHERE ID_Zbioru = ? AND Definicja = ?"
            self.controller.update_database(query, (str(back_text), str(curr_set), str(selected_flashcard)))
        else:
            query = "UPDATE Fiszki SET Definicja = ?, Odpowiedz = ? WHERE ID_Zbioru = ? AND Definicja = ?"
            self.controller.update_database(query, (str(front_text), str(back_text), str(curr_set), str(selected_flashcard)))

    def reset_entries(self):
        self.front_entry.delete(0, tk.END)
        self.back_entry.delete(0, tk.END)
        self.flashcard_combobox.set("Select Flashcard")
        self.flashcard_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))