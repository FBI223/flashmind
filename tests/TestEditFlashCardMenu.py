import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

from FlashcardApp import FlashcardApp
from EditFlashCardMenu import EditFlashCardMenu

class TestEditFlashCardMenu(unittest.TestCase):
    def setUp(self):
        self.controller = Mock(spec=FlashcardApp)
        self.controller.current_font = "Arial"
        self.controller.current_font_size = 12
        self.controller.current_big_font_size = 18
        self.controller.bg_color = "white"
        self.controller.query_database.return_value = []  # Default return value for queries

        self.root = tk.Tk()
        self.menu = EditFlashCardMenu(self.root, self.controller)

    def tearDown(self):
        self.root.destroy()

    def test_load_set_names(self):
        self.controller.query_database.return_value = [("Set1",), ("Set2",)]
        self.menu.load_set_names()
        expected_values = ("Set1", "Set2")
        self.assertEqual(self.menu.set_combobox["values"], expected_values)

    def test_add_flashcard(self):
        self.menu.set_combobox.set("Set1")
        self.menu.front_entry.insert(0, "Front1")
        self.menu.back_entry.insert(0, "Back1")

        self.controller.query_database.return_value = []
        self.menu.add_flashcard()
        
        self.controller.update_database.assert_called_once_with(
            "INSERT INTO Fiszki (ID_Zbioru, Definicja, Odpowiedz) VALUES (?, ?, ?)", 
            ("Set1", "Front1", "Back1")
        )

    def test_delete_flashcard(self):
        self.menu.set_combobox.set("Set1")
        self.menu.flashcard_combobox.set("Flashcard1")

        self.controller.query_database.return_value = [("Flashcard1",)]
        self.menu.delete_flashcard()

        self.controller.update_database.assert_called_once_with(
            "DELETE FROM Fiszki WHERE Definicja = ? AND ID_Zbioru = ?",
            ("Flashcard1", "Set1")
        )

    def test_modify_flashcard_front_and_back(self):
        self.menu.set_combobox.set("Set1")
        self.menu.flashcard_combobox.set("Flashcard1")
        self.menu.front_entry.insert(0, "NewFront")
        self.menu.back_entry.insert(0, "NewBack")

        self.controller.query_database.return_value = []
        self.menu.modify_flashcard()

        self.controller.update_database.assert_called_once_with(
            "UPDATE Fiszki SET Definicja = ?, Odpowiedz = ? WHERE ID_Zbioru = ? AND Definicja = ?",
            ("NewFront", "NewBack", "Set1", "Flashcard1")
        )

    def test_modify_flashcard_back_only(self):
        self.menu.set_combobox.set("Set1")
        self.menu.flashcard_combobox.set("Flashcard1")
        self.menu.back_entry.insert(0, "NewBack")

        self.controller.query_database.return_value = [("Flashcard1",)]
        self.menu.modify_flashcard()

        self.controller.update_database.assert_called_once_with(
            "UPDATE Fiszki SET Odpowiedz = ? WHERE ID_Zbioru = ? AND Definicja = ?",
            ("NewBack", "Set1", "Flashcard1")
        )

    def test_modify_flashcard_front_only(self):
        self.menu.set_combobox.set("Set1")
        self.menu.flashcard_combobox.set("Flashcard1")
        self.menu.front_entry.insert(0, "NewFront")

        self.controller.query_database.return_value = []
        self.menu.modify_flashcard()

        self.controller.update_database.assert_called_once_with(
            "UPDATE Fiszki SET Definicja = ? WHERE ID_Zbioru = ? AND Definicja = ?",
            ("NewFront", "Set1", "Flashcard1")
        )

if __name__ == "__main__":
    unittest.main()