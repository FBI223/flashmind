import unittest
from unittest.mock import Mock, patch
import tkinter as tk
import sys
import os

# Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

from FlashcardApp import FlashcardApp
from EditSetMenu import EditSetMenu

class TestEditSetMenu(unittest.TestCase):
    def setUp(self):
        self.controller = Mock(spec=FlashcardApp)
        self.controller.current_font = "Arial"
        self.controller.current_font_size = 12
        self.controller.current_big_font_size = 18
        self.controller.bg_color = "white"
        self.controller.query_database.return_value = []  # Default return value for queries

        self.root = tk.Tk()
        self.menu = EditSetMenu(self.root, self.controller)

    def tearDown(self):
        self.root.destroy()

    def test_update_set_combobox(self):
        self.controller.query_database.return_value = [("Set1",), ("Set2",)]
        self.menu.update_set_combobox()
        expected_values = ("Set1", "Set2")
        self.assertEqual(self.menu.set_combobox["values"], expected_values)

    def test_rename_set(self):
        self.menu.set_combobox.set("OldSet")
        self.menu.rename_entry.insert(0, "NewSet")

        self.controller.query_database.side_effect = [
            [("OldSet",)],  # First call to get set names
            [],  # Second call to check if new set name exists
            []  # Third call to refresh set names after renaming
        ]
        
        self.menu.rename_set()

        self.controller.update_database.assert_any_call(
            "UPDATE Fiszki SET ID_Zbioru = ? WHERE ID_Zbioru = ?",
            ("NewSet", "OldSet")
        )
        self.controller.update_database.assert_any_call(
            "UPDATE Zbiory SET Nazwa_zbioru = ? WHERE Nazwa_zbioru = ?",
            ("NewSet", "OldSet")
        )

    def test_delete_set(self):
        self.menu.set_combobox.set("SetToDelete")

        self.controller.query_database.side_effect = [
            [("SetToDelete",)],  # First call to get set names
            [("SetToDelete",)],  # Second call to check if set exists
            []  # Third call to refresh set names after deletion
        ]
        
        self.menu.delete_set()

        self.controller.update_database.assert_any_call(
            "DELETE FROM Fiszki WHERE ID_Zbioru = ?",
            ("SetToDelete",)
        )
        self.controller.update_database.assert_any_call(
            "DELETE FROM Zbiory WHERE Nazwa_zbioru = ?",
            ("SetToDelete",)
        )


    def test_add_set(self):
        self.menu.new_entry.insert(0, "NewSet")

        self.controller.query_database.return_value = []

        self.menu.add_set()

        self.controller.update_database.assert_called_once_with(
            "INSERT INTO Zbiory (Nazwa_zbioru) VALUES (?)",
            ("NewSet",)
        )

    def test_update_entry_from_combobox(self):
        self.menu.set_combobox.set("SetToEdit")
        event = Mock()
        self.menu.update_entry_from_combobox(event)
        self.assertEqual(self.menu.rename_entry.get(), "SetToEdit")

    def test_go_to_main_menu(self):
        self.menu.rename_entry.insert(0, "SomeName")
        self.menu.new_entry.insert(0, "AnotherName")
        self.menu.go_to_main_menu()
        self.assertEqual(self.menu.rename_entry.get(), "")
        self.assertEqual(self.menu.new_entry.get(), "")
        self.assertEqual(self.menu.set_combobox.get(), "Select Set")
        self.controller.show_frame.assert_called_once_with("MainMenu")

if __name__ == "__main__":
    unittest.main()
