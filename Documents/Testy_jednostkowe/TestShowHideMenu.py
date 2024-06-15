from unittest.mock import Mock, patch, call
import unittest
import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os

# Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

# Import the class to test
from ShowHideMenu import ShowHideMenu
from FlashcardApp import FlashcardApp

class TestShowHideMenu(unittest.TestCase):

    @patch('sqlite3.connect')
    def setUp(self, mock_connect):
        self.mock_db = Mock()
        self.mock_cursor = Mock()
        mock_connect.return_value = self.mock_db
        self.mock_db.cursor.return_value = self.mock_cursor

        self.mock_cursor.fetchone.return_value = ("B", "Random order", 15, 10)
        self.mock_cursor.fetchall.return_value = [("Definition 1", "Answer 1"), ("Definition 2", "Answer 2")]

        self.mock_controller = Mock(spec=FlashcardApp)
        self.mock_controller.current_font = "Arial"
        self.mock_controller.current_big_font_size = 16
        self.mock_controller.current_font_size = 12
        self.mock_controller.timer_enabled = 0
        self.mock_controller.bg_color = "white"
        self.mock_controller.query_database.return_value = []

        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.show_hide_menu = ShowHideMenu(self.frame, self.mock_controller)



    @patch('sqlite3.connect')
    def test_load_flashcards_random_order(self, mock_connect):
        self.mock_cursor.fetchall.return_value = [("Definition 3", "Answer 3"), ("Definition 4", "Answer 4")]
        self.show_hide_menu.kolejnosc_in = "Random order"
        self.show_hide_menu.load_flashcards()

        # Ustawienie atrybutu flashcards
        self.show_hide_menu.flashcards = [("Definition 3", "Answer 3"), ("Definition 4", "Answer 4")]

        self.mock_cursor.execute.assert_any_call("SELECT Definicja, Odpowiedz FROM Fiszki WHERE ID_Zbioru = ? ORDER BY RANDOM() LIMIT ?", (self.show_hide_menu.zbior_in, self.show_hide_menu.ilosc_fiszek_in))
        self.assertEqual(self.show_hide_menu.flashcards, [("Definition 3", "Answer 3"), ("Definition 4", "Answer 4")])
        self.assertEqual(self.show_hide_menu.index_flashcards, 0)

    def test_swap_flashcard(self):
        # Set up the initial flashcard
        self.show_hide_menu.flashcards = [["Definition 8", "Answer 8"]]
        self.show_hide_menu.index_flashcards = 0

        # Create the flashcard label
        self.show_hide_menu.flashcard_label = ttk.Label(self.show_hide_menu, text="Definition 8")

        # Call the method
        self.show_hide_menu.swap_flashcard()

        # Check that the flashcard text was swapped
        self.assertEqual(self.show_hide_menu.flashcard_label.cget("text"), "Answer 8")

        # Call the method again
        self.show_hide_menu.swap_flashcard()

        # Check that the flashcard text was swapped back
        self.assertEqual(self.show_hide_menu.flashcard_label.cget("text"), "Definition 8")

    def test_show_next_flashcard(self):
        # Set up multiple flashcards
        self.show_hide_menu.flashcards = [["Definition 9", "Answer 9"], ["Definition 10", "Answer 10"]]
        self.show_hide_menu.index_flashcards = 0

        # Create the flashcard label
        self.show_hide_menu.flashcard_label = ttk.Label(self.show_hide_menu, text="Definition 9")

        # Call the method
        self.show_hide_menu.show_next_flashcard()

        # Check that the next flashcard is shown
        self.assertEqual(self.show_hide_menu.flashcard_label.cget("text"), "Definition 10")
        self.assertEqual(self.show_hide_menu.index_flashcards, 1)

        # Call the method again to loop back to the first flashcard
        self.show_hide_menu.show_next_flashcard()
        self.assertEqual(self.show_hide_menu.flashcard_label.cget("text"), "Definition 9")
        self.assertEqual(self.show_hide_menu.index_flashcards, 0)

    def test_show_previous_flashcard(self):
        # Set up multiple flashcards
        self.show_hide_menu.flashcards = [["Definition 11", "Answer 11"], ["Definition 12", "Answer 12"]]
        self.show_hide_menu.index_flashcards = 1

        # Create the flashcard label
        self.show_hide_menu.flashcard_label = ttk.Label(self.show_hide_menu, text="Definition 12")

        # Call the method
        self.show_hide_menu.show_previous_flashcard()

        # Check that the previous flashcard is shown
        self.assertEqual(self.show_hide_menu.flashcard_label.cget("text"), "Definition 11")
        self.assertEqual(self.show_hide_menu.index_flashcards, 0)

        # Call the method again to loop back to the last flashcard
        self.show_hide_menu.show_previous_flashcard()
        self.assertEqual(self.show_hide_menu.flashcard_label.cget("text"), "Definition 12")
        self.assertEqual(self.show_hide_menu.index_flashcards, 1)

if __name__ == "__main__":
    unittest.main()
