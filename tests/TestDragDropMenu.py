import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os

# Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

# Import the class to test
from DragDropMenu import DragDropMenu
from FlashcardApp import FlashcardApp

class TestDragDropMenu(unittest.TestCase):
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
        self.drag_drop_menu = DragDropMenu(self.frame, self.mock_controller)

    def test_initialize_variables(self):
        self.drag_drop_menu.initialize_variables()
        self.assertEqual(self.drag_drop_menu.db_path, os.path.join(os.getcwd(), "fiszki.db"))
        self.assertEqual(self.drag_drop_menu.czy_przydzielone_pkt, 0)
        self.assertEqual(self.drag_drop_menu.time_over, 0)
        self.assertEqual(self.drag_drop_menu.zbior_in, "A")
        self.assertEqual(self.drag_drop_menu.kolejnosc_in, "Sequence order")
        self.assertEqual(self.drag_drop_menu.ilosc_fiszek_in, 10)
        self.assertEqual(self.drag_drop_menu.czas_odpowiedzi_in, 5)
        self.assertEqual(self.drag_drop_menu.ilosc_odwiedzonych, 0)

    @patch('sqlite3.connect')
    def test_load_flashcards_from_db(self, mock_connect):
        self.drag_drop_menu.load_flashcards_from_db()
        expected_flashcards = []
        self.assertEqual(self.drag_drop_menu.flashcards, expected_flashcards)
        self.assertEqual(self.drag_drop_menu.index_flashcards, 0)

    def test_create_widgets(self):
        self.drag_drop_menu.flashcards = [["Definition 1", "Answer 1", 0], ["Definition 2", "Answer 2", 0], ["Definition 3", "Answer 3", 0]]
        self.drag_drop_menu.create_widgets()
        self.assertIsInstance(self.drag_drop_menu.title_label, ttk.Label)
        self.assertIsInstance(self.drag_drop_menu.correct_wrong_label, ttk.Label)
        self.assertIsInstance(self.drag_drop_menu.check_answer_button, ttk.Button)
        self.assertIsInstance(self.drag_drop_menu.drag_drop_frame, tk.Frame)
        self.assertIsInstance(self.drag_drop_menu.next_button, ttk.Button)
        self.assertIsInstance(self.drag_drop_menu.go_back_button, ttk.Button)
        self.assertIsInstance(self.drag_drop_menu.main_menu_button, ttk.Button)

    def test_collect_selected_answers(self):
        button1 = Mock()
        button1.cget.return_value = "Definition 1\n=\nAnswer 1"
        button2 = Mock()
        button2.cget.return_value = "Definition 2\n=\nAnswer 2"
        button3 = Mock()
        button3.cget.return_value = "Definition 3\n=\nAnswer 3"
        self.drag_drop_menu.answer_buttons = [button1, button2, button3]

        ile_zaznaczonych, pyt_odp = self.drag_drop_menu.collect_selected_answers()
        self.assertEqual(ile_zaznaczonych, 3)
        self.assertEqual(pyt_odp, [["Definition 1", "Answer 1", 0], ["Definition 2", "Answer 2", 0], ["Definition 3", "Answer 3", 0]])

    def test_show_study_flashcard_menu(self):
        self.drag_drop_menu.timer = Mock()
        self.drag_drop_menu.timer_window = Mock()
        self.drag_drop_menu.show_study_flashcard_menu()
        self.assertIsNone(self.drag_drop_menu.timer)
        self.assertIsNone(self.drag_drop_menu.timer_window)
        self.mock_controller.show_frame.assert_called_with("StudyFlashcardMenu")

    def test_show_main_menu(self):
        self.drag_drop_menu.timer = Mock()
        self.drag_drop_menu.timer_window = Mock()
        self.drag_drop_menu.show_main_menu()
        self.assertIsNone(self.drag_drop_menu.timer)
        self.assertIsNone(self.drag_drop_menu.timer_window)
        self.mock_controller.show_frame.assert_called_with("MainMenu")

if __name__ == '__main__':
    unittest.main()
