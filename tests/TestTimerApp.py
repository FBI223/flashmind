import unittest
from unittest.mock import Mock, patch
import tkinter as tk
import winsound
import sys
import os

# Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

from TimerApp import TimerApp_points, TimerApp_def
from TimerApp import TimerApp_points, TimerApp_def

class TestTimerAppPoints(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.duration = 60
        self.end_callback = Mock()

    def test_init(self):
        timer_app = TimerApp_points(self.root, self.duration, self.end_callback)
        self.assertEqual(timer_app.duration, 60)
        self.assertEqual(timer_app.time_left, 59)
        self.assertIsInstance(timer_app.label, tk.Label)
        self.assertEqual(timer_app.label["text"], "01:00")
        self.assertEqual(timer_app.label["font"], ("Helvetica 44"))
        self.assertTrue(timer_app.root.winfo_exists())  # Check if the root window exists

    @patch('TimerApp.winsound.Beep')
    def test_update_timer_tick_sound(self, mock_beep):
        timer_app = TimerApp_points(self.root, self.duration, self.end_callback)
        timer_app.time_left = 4
        timer_app.update_timer()
        mock_beep.assert_called_once_with(1000, 100)
    
    @patch('TimerApp.winsound.MessageBeep')
    def test_update_timer_end_callback(self, mock_message_beep):
        timer_app = TimerApp_points(self.root, self.duration, self.end_callback)
        timer_app.time_left = 0
        timer_app.update_timer()
        mock_message_beep.assert_called_once_with(winsound.MB_OK)
        self.end_callback.assert_called_once()

    def tearDown(self):
        self.root.destroy()

class TestTimerAppDef(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.duration = 60
        self.end_callback = Mock()

    def test_init(self):
        timer_app = TimerApp_def(self.root, self.duration, self.end_callback)
        self.assertEqual(timer_app.duration, 60)
        self.assertEqual(timer_app.time_left, 59)
        self.assertIsInstance(timer_app.label, tk.Label)
        self.assertEqual(timer_app.label["text"], "01:00")
        self.assertEqual(timer_app.label["font"], ("Helvetica 34"))
        self.assertTrue(timer_app.root.winfo_exists())  # Check if the root window exists

    def test_update_timer(self):
        timer_app = TimerApp_def(self.root, self.duration, self.end_callback)
        timer_app.time_left = 5
        timer_app.update_timer()
        self.assertEqual(timer_app.time_left, 4)
        self.assertEqual(timer_app.label["text"], "00:05")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
