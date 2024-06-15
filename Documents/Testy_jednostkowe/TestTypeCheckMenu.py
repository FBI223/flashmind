import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

# Import the class to test
from TypeCheckMenu import TypeCheckMenu
from FlashcardApp import FlashcardApp

class TestTypeCheckMenu(unittest.TestCase):
    @patch('sqlite3.connect')
    def setUp(self, mock_connect):
        self.mock_db = Mock()
        self.mock_cursor = Mock()
        mock_connect.return_value = self.mock_db
        self.mock_db.cursor.return_value = self.mock_cursor

        # Ustawienie wartości zwrotnych dla fetchone i fetchall
        self.mock_cursor.fetchone.return_value = ("B", "Random order", 15, 10)
        self.mock_cursor.fetchall.return_value = [("Definition 1", "Answer 1"), ("Definition 2", "Answer 2")]

        self.mock_controller = Mock(spec=FlashcardApp)
        self.mock_controller.timer_enabled = 0
        self.mock_controller.current_font = "Arial"
        self.mock_controller.current_big_font_size = 16
        self.mock_controller.current_font_size = 12
        self.mock_controller.timer_enabled = 0
        self.mock_controller.bg_color = "white"
        self.mock_controller.query_database.return_value = []

        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.type_check_menu = TypeCheckMenu(self.frame, self.mock_controller)

    @patch('sqlite3.connect')
    def test_initialize_settings_with_db(self, mock_connect):
        # Mocking the database connection and cursor
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('B', 'Random order', 20, 10)

        self.type_check_menu.initialize_settings()

        self.assertEqual(self.type_check_menu.zbior_in, 'B')
        self.assertEqual(self.type_check_menu.kolejnosc_in, 'Random order')
        self.assertEqual(self.type_check_menu.ilosc_fiszek_in, 20)
        self.assertEqual(self.type_check_menu.czas_odpowiedzi_in, 10)

    @patch('sqlite3.connect')
    def test_retrieve_flashcards(self, mock_connect):
        # Mocking the database connection and cursor
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Definition1', 'Answer1'), ('Definition2', 'Answer2')]

        self.type_check_menu.retrieve_flashcards()
        
        expected_flashcards = [['Definition1', 'Answer1', 0], ['Definition2', 'Answer2', 0]]
        self.assertEqual(self.type_check_menu.flashcards, expected_flashcards)
        self.assertEqual(self.type_check_menu.index_flashcards, 0)

    def test_create_ui(self):
        # Test UI creation
        self.type_check_menu.flashcards = [['Definition1', 'Answer1', 0]]
        self.type_check_menu.create_ui()
        
        self.assertIsInstance(self.type_check_menu.title_label, ttk.Label)
        self.assertIsInstance(self.type_check_menu.go_back_button, ttk.Button)

    def test_check_answer_correct(self):
        # Test correct answer
        self.type_check_menu.flashcards = [['Definition1', 'Answer1', 0]]
        self.type_check_menu.answer_entry = Mock()
        self.type_check_menu.answer_entry.get.return_value = 'Answer1'
        self.type_check_menu.correct_wrong_label = Mock()
        self.type_check_menu.handle_correct_answer = Mock()

        self.type_check_menu.check_answer()
        self.type_check_menu.handle_correct_answer.assert_called_once()

    def test_check_answer_wrong(self):
        # Test wrong answer
        self.type_check_menu.flashcards = [['Definition1', 'Answer1', 0]]
        self.type_check_menu.answer_entry = Mock()
        self.type_check_menu.answer_entry.get.return_value = 'WrongAnswer'
        self.type_check_menu.correct_wrong_label = Mock()
        self.type_check_menu.handle_wrong_answer = Mock()

        self.type_check_menu.check_answer()
        self.type_check_menu.handle_wrong_answer.assert_called_once()

    def test_show_next_flashcard(self):
        # Test showing the next flashcard
        self.type_check_menu.flashcards = [['Definition1', 'Answer1', 1], ['Definition2', 'Answer2', 0]]
        self.type_check_menu.flashcard_label = Mock()
        self.type_check_menu.clean_input = Mock()

        self.type_check_menu.show_next_flashcard()
        self.assertEqual(self.type_check_menu.index_flashcards, 1)
        self.type_check_menu.flashcard_label.config.assert_called_with(text='Definition2')

    def test_show_previous_flashcard(self):
        # Test showing the previous flashcard
        self.type_check_menu.flashcards = [['Definition1', 'Answer1', 0], ['Definition2', 'Answer2', 1]]
        self.type_check_menu.flashcard_label = Mock()
        self.type_check_menu.clean_input = Mock()
        self.type_check_menu.index_flashcards = 1

        self.type_check_menu.show_previous_flashcard()
        self.assertEqual(self.type_check_menu.index_flashcards, 0)
        self.type_check_menu.flashcard_label.config.assert_called_with(text='Definition1')


if __name__ == '__main__':
    unittest.main()
