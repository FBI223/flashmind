import tkinter as tk
from tkinter import ttk
import os

class ExportSelectedSets(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure_styles()  # Konfiguracja stylów
        self.create_widgets()  # Dodanie elementów okna
        self.place_widgets()  # Umiejscowienie elementów

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("Custom.TButton", font=(self.controller.current_font, self.controller.current_font_size))

    def create_widgets(self):
        # Tytuł okna
        self.title_label = tk.Label(self, text="Export Selected Sets", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)

        # Lista zbiorów
        self.sets_listbox = tk.Listbox(self, selectmode='multiple', font=(self.controller.current_font, self.controller.current_font_size))
        self.populate_sets_listbox()  # Wypełnienie listy

        # Przyciski
        self.export_button = ttk.Button(self, text="Export", style="Custom.TButton", command=self.controller.export_file)
        self.back_button = ttk.Button(self, text="Main Menu", style="Custom.TButton", command=lambda: self.controller.show_frame("MainMenu"))

    def place_widgets(self):
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.sets_listbox.place(relx=0.5, rely=0.5, anchor='center', width=250, height=150)
        self.export_button.place(relx=0.5, rely=0.7, anchor='center')
        self.back_button.place(relx=0.5, rely=0.85, anchor='center')

    def populate_sets_listbox(self):
        sets = self.controller.get_set_names()
        for set_name in sets:
            self.sets_listbox.insert(tk.END, set_name)

    def get_selected_sets(self):
        selected_indices = self.sets_listbox.curselection()
        return [str(self.sets_listbox.get(i)) for i in selected_indices]