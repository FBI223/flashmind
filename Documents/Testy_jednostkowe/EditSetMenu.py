import tkinter as tk
from tkinter import ttk
import sqlite3
import os

class EditSetMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure_styles() # Styl przycisków
        self.configure_frames() # Ustawienie frames
        self.create_widgets() # Dodanie elementów okna
        self.place_widgets() # Umiejscowienie elementów

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
        # Tytuł okna
        self.title_label = tk.Label(self, text="Select Set to Edit", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)

        # Etykieta i combobox wyboru zestawu
        self.combobox_label = tk.Label(self, text="Select Set:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.set_combobox = ttk.Combobox(self, font=(self.controller.current_font, self.controller.current_font_size))
        self.set_combobox.set("Select Set")
        self.set_combobox.bind("<<ComboboxSelected>>", self.update_entry_from_combobox)
        self.update_set_combobox()

        # Przemianowanie zestawu
        self.rename_label = tk.Label(self, text="Rename Selected Set:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.rename_entry = ttk.Entry(self)

        # Przycisk przemianowania
        self.rename_button = ttk.Button(self, text="Rename Set", style="Custom.TButton", command=self.rename_set)

        # Przycisk usunięcia
        self.remove_button = ttk.Button(self, text="Remove Set", style="Custom.TButton", command=self.delete_set)

        # Przycisk resetowania
        self.reset_button = ttk.Button(self, text="Reset Set Stats", style="Custom.TButton", command=self.reset_set)

        # Dodanie nowego zestawu
        self.new_label = tk.Label(self, text="Add New Set:", font=(self.controller.current_font, self.controller.current_font_size), bg=self.controller.bg_color)
        self.new_entry = ttk.Entry(self)
        self.add_button = ttk.Button(self, text="Add Set", style="Custom.TButton", command=self.add_set)

        # Przycisk powrotu do głównego menu
        self.main_menu_button = ttk.Button(self, text="Main Menu", style="Custom.TButton", command=self.go_to_main_menu)

    def place_widgets(self):
        # Tytuł okna
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')

        # Etykieta i combobox wyboru zestawu
        self.combobox_label.place(relx=0.5, rely=0.18, anchor='center')
        self.set_combobox.place(relx=0.5, rely=0.24, width=250, height=40, anchor='center')

        # Przemianowanie zestawu
        self.rename_label.place(relx=0.5, rely=0.3, anchor='center')
        self.rename_entry.place(relx=0.5, rely=0.36, width=250, height=40, anchor='center')
        self.rename_button.place(relx=0.5, rely=0.43, width=250, height=40, anchor='center')

        # Usunięcie i resetowanie zestawu
        self.remove_button.place(relx=0.5, rely=0.50, width=250, height=40, anchor='center')
        self.reset_button.place(relx=0.5, rely=0.57, width=250, height=40, anchor='center')

        # Dodanie nowego zestawu
        self.new_label.place(relx=0.5, rely=0.64, anchor='center')
        self.new_entry.place(relx=0.5, rely=0.71, width=250, height=40, anchor='center')
        self.add_button.place(relx=0.5, rely=0.78, width=250, height=40, anchor='center')

        # Przycisk powrotu do głównego menu
        self.main_menu_button.place(relx=0.5, rely=0.92, width=250, height=40, anchor='center')
        
    def reset_set(self):
        incorrect_selection_label = tk.Label(self, text="Set was reseted", font=("Arial", 30), foreground="green", bg=self.controller.bg_color)
        incorrect_selection_label.place(relx=0.5, rely=0.44, anchor='center')
        name = str(self.set_combobox.get())
        query = "UPDATE Fiszki SET Stopien_Przyswojenia = 0 WHERE ID_Zbioru = ?"
        self.controller.update_database(query, (str(name),))
        self.after(1500, incorrect_selection_label.destroy)  # Usunięcie wiadomości po czasie

    def go_to_main_menu(self):
        self.rename_entry.delete(0, tk.END)
        self.new_entry.delete(0, tk.END)
        self.set_combobox.set("Select Set")  # Ustawienie domyślnej wartości
        self.set_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))
        self.controller.show_frame("MainMenu")

    def update_set_combobox(self):
        query = "SELECT Nazwa_zbioru FROM Zbiory ORDER BY Nazwa_zbioru ASC"
        result = self.controller.query_database(query)
        set_names = [row[0] for row in result]
        self.set_combobox['values'] = set_names
        self.set_combobox.set("Select Set")
        self.set_combobox.config(font=(self.controller.current_font, self.controller.current_font_size))

    def update_entry_from_combobox(self, event):
        selected_set = str(self.set_combobox.get())
        self.rename_entry.delete(0, tk.END)
        self.rename_entry.insert(0, selected_set)

    def rename_set(self):
        query = "SELECT Nazwa_zbioru FROM Zbiory"
        result = self.controller.query_database(query)
        
        set_names = [row[0] for row in result]
        
        if str(self.set_combobox.get()) in str(set_names):
            old_name = str(self.set_combobox.get())
            new_name = str(self.rename_entry.get())
            query = "SELECT Nazwa_zbioru FROM Zbiory WHERE Nazwa_zbioru = ? LIMIT 1"
            first_row = self.controller.query_database(query, (str(new_name),))
            if not first_row:
                query = "UPDATE Fiszki SET ID_Zbioru = ? WHERE ID_Zbioru = ?"
                self.controller.update_database(query, (str(new_name), str(old_name)))
                query = "UPDATE Zbiory SET Nazwa_zbioru = ? WHERE Nazwa_zbioru = ?"
                self.controller.update_database(query, (str(new_name), str(old_name)))
            self.rename_entry.delete(0, tk.END)
            self.new_entry.delete(0, tk.END)
            self.update_set_combobox()

    def delete_set(self):
        query = "SELECT Nazwa_zbioru FROM Zbiory"
        result = self.controller.query_database(query)
        set_names = [row[0] for row in result]

        if str(self.set_combobox.get()) in str(set_names):
            delete_name = str(self.set_combobox.get())
            query = "SELECT Nazwa_zbioru FROM Zbiory WHERE Nazwa_zbioru = ? LIMIT 1"
            result = self.controller.query_database(query, (str(delete_name),))
            if result:
                delete_queries = [
                    ("DELETE FROM Fiszki WHERE ID_Zbioru = ?", (str(delete_name),)),
                    ("DELETE FROM Zbiory WHERE Nazwa_zbioru = ?", (str(delete_name),))
                ]
                for query, params in delete_queries:
                    self.controller.update_database(query, params)
                self.rename_entry.delete(0, tk.END)
                self.new_entry.delete(0, tk.END)
                self.update_set_combobox()

    def add_set(self):
        set_name = str(self.new_entry.get())
        query = "SELECT Nazwa_zbioru FROM Zbiory WHERE Nazwa_zbioru = ? LIMIT 1"
        result = self.controller.query_database(query, (str(set_name),))
        if not result:
            query = "INSERT INTO Zbiory (Nazwa_zbioru) VALUES (?)"
            self.controller.update_database(query, (str(set_name),))
            self.rename_entry.delete(0, tk.END)
            self.new_entry.delete(0, tk.END)
            self.update_set_combobox()