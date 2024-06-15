import tkinter as tk
from tkinter import ttk
import sqlite3
import os
from PIL import Image, ImageTk

# Klasa przycisków z ikonami
class IconButton(ttk.Button):
    def __init__(self, parent, image_path, text, command, controller):
        self.controller = controller
        self.image = Image.open(image_path)
        self.image = self.image.resize((30, 30))
        self.image_tk = ImageTk.PhotoImage(self.image)
        
        super().__init__(parent, text=text, image=self.image_tk, compound='left', style="Custom.TButton", command=command)

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")

        self.configure_style() # Styl przycisków
        self.configure_grid(parent) # Stworzenie grid
        self.add_logo_image() # Logo aplikacji
        self.create_widgets() # Dodanie elementów okna
        self.place_widgets() # Umiejscowienie elementów
        self.update_random_quote() # Dodanie cytatu
    
    def configure_style(self):
        self.style = ttk.Style(self)
        self.style.configure("Custom.TButton", font=(self.controller.current_font, self.controller.current_font_size))

    def configure_grid(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def add_logo_image(self):
        if os.path.exists(self.controller.logo_path):
            self.image = Image.open(self.controller.logo_path)
            self.image = self.image.resize((110, 110))
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(self, image=self.photo, bg=self.controller.bg_color)
            self.image_label.place(relx=0.5, rely=0.2, anchor='center')
        else:
            print(f"Obrazek nie istnieje w podanej ścieżce: {self.controller.logo_path}")

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Flash Mind App", font=(self.controller.current_font, self.controller.current_big_font_size), bg=self.controller.bg_color)
        
        self.logo_image = self.add_logo_image()
        
        self.buttons_data = [
            ("study.png", "Study Flashcards", "StudyFlashcardMenu", 0.32),
            ("edit.png", "Edit Set", "EditSetMenu", 0.40),
            ("edit_flashcard.png", "Edit Flashcards", "EditFlashCardMenu", 0.48),
            ("profile.png", "Profile", "ProfileMenu", 0.56),
            ("settings.png", "Settings", "SettingsMenu", 0.64),
            ("exit.png", "Exit", self.controller.custom_exit, 0.76)
        ]

        self.buttons = []
        for image, text, command, rel_y in self.buttons_data:
            image_path = os.path.join(os.getcwd(), "images", image)
            if isinstance(command, str):
                button = IconButton(self, image_path, text, lambda c=command: self.controller.show_frame(c), self.controller)
            else:
                button = IconButton(self, image_path, text, command, self.controller)
            self.buttons.append((button, rel_y))

        self.random_quote_label = tk.Label(self, text="", font=(self.controller.current_font, 18), bg=self.controller.bg_color)

    def place_widgets(self):
        # Tytuł główny
        self.title_label.place(relx=0.5, rely=0.08, anchor='center')
        
        # Logo aplikacji
        if self.logo_image:
            self.logo_label = tk.Label(self, image=self.logo_image)
            self.logo_label.place(relx=0.5, rely=0.2, anchor='center')

        # Przyciski
        for button, rel_y in self.buttons:
            button.place(relx=0.5, rely=rel_y, width=250, height=40, anchor='center')
        
        # Cytat
        self.random_quote_label.place(relx=0.5, rely=0.94, anchor='s')
        self.random_quote_label.config(wraplength=self.winfo_width() - 40)
        
        self.bind("<Configure>", self.on_resize)

    def get_random_quote(self):
        query = "SELECT Tresc FROM Cytaty ORDER BY RANDOM() LIMIT 1"
        result = self.controller.query_database(query)
        if result:
            return result[0][0]
        return ""

    def update_random_quote(self):
        random_quote = self.get_random_quote()
        self.random_quote_label.config(text=random_quote)

    def on_resize(self, event):
        self.random_quote_label.config(wraplength=event.width - 40)  # Aktualizuj wraplength podczas zmiany rozmiaru okna
        self.random_quote_label.place_configure(relx=0.5, rely=0.94, anchor='s')  # Utrzymaj pozycję na dole ekranu