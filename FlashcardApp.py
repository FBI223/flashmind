import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from ttkthemes import ThemedStyle
from tkinter import colorchooser, filedialog, messagebox
import sqlite3
import os
from datetime import datetime
import shutil
import json

from ExportSelectedSets import ExportSelectedSets
from EditSetMenu import EditSetMenu
from EditFlashCardMenu import EditFlashCardMenu
from ProfileMenu import ProfileMenu
from SettingsMenu import SettingsMenu
from MainMenu import MainMenu
from StudyFlashcardMenu import StudyFlashcardMenu
from ShowHideMenu import ShowHideMenu
from TypeCheckMenu import TypeCheckMenu
from DragDropMenu import DragDropMenu

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db_path = os.path.join(os.getcwd(), "fiszki.db")

        self.initialize_theme_style()  # Inicjalizacja stylu motywu
        self.initialize_menu_bar()  # Inicjalizacja menu
        self.set_icon()  # Ustawienie ikony
        self.load_settings_from_database()  # Załadowanie ustawień z bazy danych
        self.handle_window_close_event()  # Obsługa zamknięcia okna
        self.initialize_frames()  # Inicjalizacja ramek

        self.show_frame("MainMenu")  # Wyświetlenie ramki głównego menu
    
    def initialize_theme_style(self):
        self.style = ThemedStyle(self)
        self.bg_color = "#f0f0f0"  # Domyślny kolor tła

    def initialize_menu_bar(self):
        # Zmienna dla czasomierza
        self.timer_enabled = 0

        # Utworzenie paska menu
        self.title("FlashMind")  # Tytuł okna aplikacji
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Utworzenie menu "File"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        # Dodanie opcji do menu "File"
        file_menu.add_command(label="Import", command=self.import_file)
        file_menu.add_command(label="Export", command=lambda: self.show_frame("ExportSelectedSets"))
        file_menu.add_separator()
        file_menu.add_command(label="Back Up", command=self.back_up_db)
        file_menu.add_command(label="Restore", command=self.restore_db)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.custom_exit)

    def set_icon(self):
        # Ustawienie ikony aplikacji
        self.images_path = os.path.join(os.getcwd(), "images")
        self.logo_path = os.path.join(self.images_path, "logo.ico")
        if os.path.exists(self.logo_path):
            self.iconbitmap(self.logo_path)
        else:
            print(f"Ikona nie istnieje w podanej ścieżce: {self.logo_path}")

    def load_settings_from_database(self):
        # Ustawienia domyślne
        self.default_resolution = "700x700"
        self.default_theme = "vista"
        self.default_font = "Arial"
        self.default_font_size = 16
        self.default_big_font_size = 30
        self.default_background_color = "#f0f0f0"

        # Załadowanie ustawień z bazy danych
        query = "SELECT Rozdzielczosc, Motyw, Czcionka, Rozmiar_Czcionki, Kolor FROM Ustawienia LIMIT 1"
        result = self.query_database(query)
        if result:
            resolution_in, theme_in, font_in, font_size_in , color_in = result[0]
            if resolution_in == "Full Screen":
                self.attributes("-fullscreen", True)
            else:
                self.geometry(resolution_in)
                self.attributes("-fullscreen", False)
            self.set_theme(theme_in)
            self.current_font = font_in
            self.current_font_size = font_size_in
            self.current_big_font_size = 30
            self.bg_color = color_in

        else:
            # Ustawienia domyślne
            self.geometry(self.default_resolution)
            self.set_theme(self.default_theme)
            self.current_font = self.default_font
            self.current_font_size = self.default_font_size
            self.current_big_font_size = self.default_big_font_size
            self.bg_color = self.default_background_color

        # Aktualizacja ostatniego powiadomienia
        x = "no notifications"
        query = "UPDATE Profile SET OSTATNIE_POWIADOMIENIE = ?"
        self.update_database(query, (x,))

    def handle_window_close_event(self):
        # Obsługa zamknięcia okna
        self.protocol("WM_DELETE_WINDOW", self.custom_exit)

    def initialize_frames(self):
        # Inicjalizacja ramek
        self.frames = {}
        for F in (MainMenu, StudyFlashcardMenu, ShowHideMenu, TypeCheckMenu, DragDropMenu,
                  EditSetMenu, EditFlashCardMenu, ProfileMenu, SettingsMenu, ExportSelectedSets):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def back_up_db(self):
        # Funkcja tworzenia kopii zapasowej bazy danych
        file_path = filedialog.asksaveasfilename(
            title="Save file", 
            defaultextension=".db", 
            filetypes=(("Database files", "*.db"), ("Other files", "*.*"))
        )
        
        if file_path:
            if os.path.basename(file_path) != "fiszki.db":
                db_path = os.path.join(os.getcwd(), "fiszki.db")
                shutil.copyfile(db_path, file_path)
                messagebox.showinfo("Back Up", f"File backed up succesfully to {file_path}")
            else:
                messagebox.showinfo("Back Up", f"Cannot back up file named fiszki.db")

    def restore_db(self):
        # Prompt the user to select the backup file
        backup_file_path = filedialog.askopenfilename(
            title="Select backup file",
            defaultextension=".db" ,
            filetypes=(("Database files", "*.db"), ("All Files", "*.*"))
        )

        if ( "." not in backup_file_path ):
            return

        if ( ".db" not in backup_file_path ):
            messagebox.showinfo( "Restore" , f"Cannot read this file type: { backup_file_path } ")
            return
        
        if backup_file_path:
            try:
                # Connect to the backup database
                db = sqlite3.connect(backup_file_path)
                cursor = db.cursor()

                # Check if the Back_Up_Restore table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Back_Up_Restore';")
                table_exists = cursor.fetchone()
                if table_exists:
                    # Execute the query to check the flag
                    cursor.execute("SELECT * FROM Back_Up_Restore LIMIT 1")
                    

                    # Remove the current database file if it exists
                    if os.path.exists(self.db_path):
                        os.remove(self.db_path)

                    # Copy the backup file to the application's directory and rename it to fiszki.db
                    shutil.copyfile(backup_file_path, self.db_path)
                    messagebox.showinfo("Restore" , f"Database restored from {backup_file_path} " )
                else:
                    messagebox.showinfo("Restore" , "Cannot restore from this database file.")
            except sqlite3.Error as e:
                messagebox.showinfo( "Restore" ,f"Error during database operation: {e}")
            finally:
                db.close()

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select file", defaultextension=".db" ,filetypes=(("Database files", "*.db" ), ("Text files", "*.txt") ))
        if file_path:
            if os.path.basename(file_path) != "fiszki.db":
                db = sqlite3.connect(file_path)
                cursor = db.cursor()
                db2 = sqlite3.connect(self.db_path)
                cursor2 = db2.cursor()

                # dodawanie do tabeli Zbiory:
                query = "SELECT Nazwa_Zbioru FROM Zbiory"
                cursor.execute(query)
                rows = cursor.fetchall()

                query2 = "SELECT Nazwa_Zbioru FROM Zbiory"
                cursor2.execute(query2)
                pom = cursor2.fetchall()
                if rows:
                    for r in rows:

                        # dodajemy tylko wtedy gdy nie ma w bazie jeszcze tego zbioru
                        if r not in pom:
                            query2 = "INSERT INTO Zbiory (Nazwa_Zbioru) VALUES (?)"
                            cursor2.execute(query2, (str(r[0]),))
                            db2.commit()

                # dodawanie do tabeli Fiszki:
                query = "SELECT ID_Zbioru, Definicja, Odpowiedz FROM Fiszki"
                cursor.execute(query)
                all_rows = cursor.fetchall()

                if all_rows:

                    for row in all_rows:
                        query2 = "INSERT OR IGNORE INTO Fiszki (ID_Zbioru, Definicja, Odpowiedz) VALUES (?, ?, ?)"
                        cursor2.execute(query2, (str(row[0]), str(row[1]), str(row[2])))
                        db2.commit()
                db.close()
                db2.close()
                messagebox.showinfo("Import", f"File imported: {file_path}")

            else:
                messagebox.showinfo("Import", f"Cannot import from fiszki.db")

    def export_to_database(self, selected_sets, file_path):
        db = sqlite3.connect(file_path)
        db2 = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor2 = db2.cursor()
        cursor.execute('''CREATE TABLE Zbiory (Nazwa_Zbioru STRING)''')
        db.commit()
        cursor.execute('''CREATE TABLE Fiszki (ID_Zbioru STRING, Definicja, Odpowiedz)''')
        db.commit()

        for row in selected_sets:
            cursor.execute('''INSERT INTO Zbiory (Nazwa_Zbioru) VALUES (?)''', (str(row),))

            query2 = "SELECT ID_Zbioru, Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ?"
            cursor2.execute(query2, (str(row),))

            rows = cursor2.fetchall()
            if rows:
                for r in rows:
                    cursor.execute('''INSERT INTO Fiszki (ID_Zbioru, Definicja, Odpowiedz) VALUES (?, ?, ?)''', (str(r[0]), str(r[1]), str(r[2])))
                db.commit()

        db.close()
        db2.close()

    def export_to_text_file(self, selected_sets, file_path):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        with open(file_path, 'w') as f:
            for row in selected_sets:
                query = "SELECT ID_Zbioru, Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ?"
                cursor.execute(query, (str(row),))
                rows = cursor.fetchall()
                if rows:
                    for r in rows:
                        f.write(f"{r[0]} {r[1]} {r[2]}\n")
        db.close()

    def export_to_json_file(self, selected_sets, file_path):
        data = {}
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        for row in selected_sets:
            query = "SELECT ID_Zbioru, Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ?"
            cursor.execute(query, (str(row),))
            rows = cursor.fetchall()
            if rows:
                set_name = f"Set_{row}"
                data[set_name] = []
                for r in rows:
                    data[set_name].append({
                        "ID_Zbioru": r[0],
                        "Definicja": r[1],
                        "Odpowiedz": r[2]
                    })
        db.close()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def export_file(self):
        selected_sets = self.frames['ExportSelectedSets'].get_selected_sets()
        if selected_sets:
            file_path = filedialog.asksaveasfilename(title="Save file", defaultextension=".txt", filetypes=(("Database files", "*.db"), ("Json files", "*.json"), ("Text files", "*.txt"), ("Other files", "*.*")))
            if file_path:
                if os.path.basename(file_path) != "fiszki.db":
                    print(os.path.basename(file_path))
                    if file_path.endswith(".db"):
                        self.export_to_database(selected_sets, file_path)
                    elif file_path.endswith(".txt"):
                        self.export_to_text_file(selected_sets, file_path)
                    elif file_path.endswith(".json"):
                        self.export_to_json_file(selected_sets, file_path)
                    else:
                        messagebox.showinfo("Export", f"Unsupported data type")
                else:
                    messagebox.showwarning("Export", "Cannot overwrite fiszki.db")
        else:
            messagebox.showwarning("Export", "No sets selected for export.")

    def get_set_names(self):
        query = "SELECT Nazwa_zbioru FROM Zbiory"
        result = self.query_database(query)
        sets = [row[0] for row in result]
        return sets

    def show_frame(self, page_name):
        frame_classes = {
            "EditFlashCardMenu": EditFlashCardMenu,
            "EditSetMenu": EditSetMenu,
            "ShowHideMenu": ShowHideMenu,
            "TypeCheckMenu": TypeCheckMenu,
            "DragDropMenu": DragDropMenu,
            "StudyFlashcardMenu": StudyFlashcardMenu,
            "ProfileMenu": ProfileMenu,
            "ExportSelectedSets": ExportSelectedSets
        }

        if page_name in frame_classes:
            frame = frame_classes[page_name](parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame = self.frames[page_name]

        frame.configure(bg=self.bg_color)
        frame.tkraise()

    def update_background_color(self, widget, color):
        try:
            widget.configure(bg=color)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            try:
                if isinstance(child, (tk.Frame, ttk.Frame)):
                    self.update_background_color(child, color)
                else:
                    child.configure(bg=color)
            except tk.TclError:
                # Widget nie obsługuje opcji 'bg', pomiń
                pass

    def set_background_color(self, color_code=None):
        if not color_code:
            color_code = colorchooser.askcolor(title="Choose background color")[1]
        if color_code:
            self.configure(bg=color_code)
            self.bg_color = color_code
            for frame in self.frames.values():
                self.update_background_color(frame, color_code)

    def set_theme(self, theme_name):
        self.style.set_theme(theme_name)

    def set_font(self, font_name):
        self.current_font = font_name
        exceptions = [
            self.frames['MainMenu'].title_label,
            self.frames['SettingsMenu'].title_label,
            self.frames['ProfileMenu'].title_label,
            self.frames['ShowHideMenu'].title_label,
            self.frames['TypeCheckMenu'].title_label,
            self.frames['DragDropMenu'].title_label,
            self.frames['EditSetMenu'].title_label,
            self.frames['EditFlashCardMenu'].edit_title_label,
            self.frames['StudyFlashcardMenu'].title_label,
        ]
        for frame in self.frames.values():
            self.update_font_keep_size(frame, exceptions)

        #zmiana czcionki przycisków
        self.style.configure("Custom.TButton", font=(self.current_font, self.current_font_size))

    def update_font_keep_size(self, widget, exceptions):
        for child in widget.winfo_children():
            try:
                if isinstance(child, (ttk.Button, ttk.Label, tk.Label, ttk.Combobox, ttk.Entry)):
                    font = tkFont.Font(font=child.cget("font"))
                    if child in exceptions:
                        current_size = font.cget("size")
                        child.config(font=(self.current_font, current_size))
                    else:
                        child.config(font=(self.current_font, self.current_font_size))
                elif isinstance(child, (tk.Frame, ttk.Frame)):
                    self.update_font_keep_size(child, exceptions)
            except tk.TclError:
                # Widget nie obsługuje opcji 'font', pomiń
                pass

    def set_resolution(self, resolution):
        self.geometry(resolution)

    def custom_exit(self):
        print("Performing cleanup actions before exit...")

        now = str(datetime.now())
        query = "UPDATE Profile SET OSTATNIE_POWIADOMIENIE = ?"
        self.update_database(query, (now,))

        self.quit()
    
    def update_database(self, query, params):
        # Aktualizacja danych w bazie
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute(query, params)
        db.commit()
        db.close()

    def query_database(self, query, params=()):
        # Pobieranie danych z bazy
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        db.close()
        return result