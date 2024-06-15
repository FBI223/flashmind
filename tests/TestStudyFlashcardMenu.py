import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

from FlashcardApp import FlashcardApp
from StudyFlashcardMenu import StudyFlashcardMenu

class TestStudyFlashcardMenu(unittest.TestCase):

    def setUp(self):
        # Mockowanie kontrolera
        self.controller = MagicMock(spec=FlashcardApp)
        self.controller.current_font = "Arial"
        self.controller.current_font_size = 12
        self.controller.current_big_font_size = 14
        self.controller.bg_color = "white"
        
        # Tworzenie instancji StudyFlashcardMenu
        self.root = tk.Tk()
        self.study_flashcard_menu = StudyFlashcardMenu(self.root, self.controller)

    def test_create_flashcard_game_buttons(self):
        self.assertEqual(self.study_flashcard_menu.show_hide_button['text'], "show & hide")
        self.assertEqual(self.study_flashcard_menu.type_check_button['text'], "type & check")
        self.assertEqual(self.study_flashcard_menu.drag_drop_button['text'], "drag & drop")

    def test_create_counter_widgets(self):
        self.assertEqual(self.study_flashcard_menu.counter_amount_flashcards.get(), 10)
        self.assertEqual(self.study_flashcard_menu.counter_time_answer.get(), 10)
    def test_increase_decrease_amount_flashcard(self):
        self.study_flashcard_menu.counter_amount_flashcards.set(10)
        self.study_flashcard_menu.increase_amount_flashcard()
        self.assertEqual(self.study_flashcard_menu.counter_amount_flashcards.get(), 11)
        self.study_flashcard_menu.decrease_amount_flashcard()
        self.assertEqual(self.study_flashcard_menu.counter_amount_flashcards.get(), 10)
        self.study_flashcard_menu.decrease_amount_flashcard()
        self.assertEqual(self.study_flashcard_menu.counter_amount_flashcards.get(), 9)

    def test_increase_decrease_time_answer(self):
        self.study_flashcard_menu.counter_time_answer.set(10)
        self.study_flashcard_menu.increase_time_answer()
        self.assertEqual(self.study_flashcard_menu.counter_time_answer.get(), 11)
        self.study_flashcard_menu.decrease_time_answer()
        self.assertEqual(self.study_flashcard_menu.counter_time_answer.get(), 10)
        self.study_flashcard_menu.decrease_time_answer()
        self.assertEqual(self.study_flashcard_menu.counter_time_answer.get(), 9)

    @patch('StudyFlashcardMenu.create_timer')
    def test_start_timer(self, mock_create_timer):
        self.study_flashcard_menu.start_timer(10, "Countdown")
        self.assertTrue(self.study_flashcard_menu.timer_window.winfo_exists())
        mock_create_timer.assert_called_with(self.study_flashcard_menu.timer_window, 10, self.study_flashcard_menu.timer_ended, "Countdown")

    def test_incorrect_selection(self):
        self.study_flashcard_menu.incorrect_selection()
        incorrect_label = [child for child in self.study_flashcard_menu.winfo_children() if isinstance(child, ttk.Label) and child['text'] == "Incorrect selection. Please fill all fields."]
        self.assertTrue(len(incorrect_label) > 0)

    def test_stop_timer(self):
        self.study_flashcard_menu.start_timer(10, "points")
        self.study_flashcard_menu.stop_timer()
        self.assertIsNone(self.study_flashcard_menu.timer)
        self.assertIsNone(self.study_flashcard_menu.timer_window)


if __name__ == "__main__":
    unittest.main()
