import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk

import sys
import os

#Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

# Import the class to test
from FlashcardApp import FlashcardApp
from ProfileMenu import ProfileMenu

class TestProfileMenu(unittest.TestCase):

    @patch('ProfileMenu.sqlite3.connect')
    def setUp(self, mock_connect):
        # Mock the database connection and cursor
        self.mock_db = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_db
        self.mock_db.cursor.return_value = self.mock_cursor
        
        # Mock the controller
        self.controller = MagicMock(spec=FlashcardApp)
        self.controller.current_font = "Arial"
        self.controller.current_font_size = 12
        self.controller.current_big_font_size = 14
        self.controller.bg_color = "#ffffff"

        # Set up mock return values for the query_database method
        self.controller.query_database.side_effect = [
            [(10, 5)],  # First query: DOBRZE, ZLE
            [(100,)],   # Second query: COUNT(*) FROM Fiszki
            [(5,)],     # Third query: COUNT(*) FROM Zbiory
            [(50,)]     # Fourth query: SUM(Stopien_Przyswojenia)
        ]

        # Create instance of ProfileMenu
        self.root = tk.Tk()
        self.profile_menu = ProfileMenu(self.root, self.controller)
    
    def test_reset_profile(self):
        with patch.object(self.profile_menu, 'profile_frame', create=True) as mock_profile_frame, \
             patch.object(self.profile_menu, 'delete_frame', create=True) as mock_delete_frame:
            self.profile_menu.reset_profile()
            mock_profile_frame.forget.assert_called()
            mock_delete_frame.pack.assert_called_with(fill="both", expand=True)

    def test_no_command(self):
        with patch.object(self.profile_menu, 'delete_frame', create=True) as mock_delete_frame:
            self.profile_menu.No_command()
            mock_delete_frame.pack_forget.assert_called()
            self.controller.show_frame.assert_called_with("ProfileMenu")

    @patch('ProfileMenu.sqlite3.connect')
    def test_load_data(self, mock_connect):
        # Reconfigure the mock connection for this specific test
        mock_connect.return_value = self.mock_db
                
        self.controller.query_database.side_effect = [
            [(10, 5)],  # First query: DOBRZE, ZLE
            [(100,)],   # Second query: COUNT(*) FROM Fiszki
            [(5,)],     # Third query: COUNT(*) FROM Zbiory
            [(50,)]     # Fourth query: SUM(Stopien_Przyswojenia)
        ]

        self.profile_menu.load_data()

        # Check if the cursor executed the expected queries
        self.controller.query_database.assert_any_call("SELECT DOBRZE, ZLE FROM Profile LIMIT 1")
        self.controller.query_database.assert_any_call("SELECT COUNT(*) FROM Fiszki")
        self.controller.query_database.assert_any_call("SELECT COUNT(*) FROM Zbiory")
        self.controller.query_database.assert_any_call("SELECT SUM(Stopien_Przyswojenia) FROM Fiszki")
        
        # Check if the loaded data is correct
        self.assertEqual(self.profile_menu.correct_in, 10)
        self.assertEqual(self.profile_menu.incorrect_in, 5)
        self.assertEqual(self.profile_menu.flashcard_count, 100)
        self.assertEqual(self.profile_menu.set_count, 5)
        self.assertEqual(self.profile_menu.exp_points_in, 50)


    def test_calculate_level(self):
        self.profile_menu.exp_points_in = 0
        self.assertEqual(self.profile_menu.calculate_level(), "Flashcard Novice")
        self.profile_menu.exp_points_in = 75
        self.assertEqual(self.profile_menu.calculate_level(), "Knowledge Explorer")
        self.profile_menu.exp_points_in = 200
        self.assertEqual(self.profile_menu.calculate_level(), "Word Hunter")
        self.profile_menu.exp_points_in = 400
        self.assertEqual(self.profile_menu.calculate_level(), "Memory Guardian")
        self.profile_menu.exp_points_in = 800
        self.assertEqual(self.profile_menu.calculate_level(), "Retention Master")
        self.profile_menu.exp_points_in = 1500
        self.assertEqual(self.profile_menu.calculate_level(), "Language Wizard")
        self.profile_menu.exp_points_in = 3000
        self.assertEqual(self.profile_menu.calculate_level(), "Flashcard Guru")

    def test_go_to_main_menu(self):
        self.profile_menu.go_to_main_menu()
        self.assertEqual(self.profile_menu.profile_combobox.get(), "Set interval")
        self.controller.show_frame.assert_called_with("MainMenu")

    def test_set_reminder(self):
        self.profile_menu.profile_combobox.set("1h")
        self.profile_menu.set_reminder()
        self.controller.update_database.assert_called_with("UPDATE Profile SET INTERWAL = ?", ('1h',))

    def test_yes_command(self):
        self.profile_menu.Yes_command()
        self.controller.update_database.assert_any_call("UPDATE Fiszki SET Stopien_Przyswojenia = 0", ())
        self.controller.update_database.assert_any_call("UPDATE Profile SET DOBRZE = 0", ())
        self.controller.update_database.assert_any_call("UPDATE Profile SET ZLE = 0", ())


if __name__ == "__main__":
    unittest.main()
