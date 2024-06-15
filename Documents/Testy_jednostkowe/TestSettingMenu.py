import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk, colorchooser
import sys
import os

#Add flash_mind_v1 to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flash_mind_v1')))

#Import the class to test
from FlashcardApp import FlashcardApp
from SettingsMenu import SettingsMenu

class TestSettingsMenu(unittest.TestCase):

    @patch('SettingsMenu.colorchooser.askcolor')
    def test_set_background_color(self, mock_askcolor):
        # Mock the controller
        controller = MagicMock(spec=FlashcardApp)
        controller.current_font = "Arial"
        controller.current_font_size = 12
        controller.current_big_font_size = 14
        controller.bg_color = "#f0f0f0"

        # Create instance of SettingsMenu
        root = tk.Tk()
        settings_menu = SettingsMenu(root, controller)

        # Define the return value for colorchooser.askcolor
        mock_askcolor.return_value = ((255, 255, 255), '#ffffff')

        # Call the method
        settings_menu.set_background_color()

        # Check if the controller method was called with the correct argument
        controller.set_background_color.assert_called_with('#ffffff')

    def test_go_to_main_menu(self):
        # Mock the controller
        controller = MagicMock(spec=FlashcardApp)
        controller.current_font = "Arial"
        controller.current_font_size = 12
        controller.current_big_font_size = 14
        controller.bg_color = "#f0f0f0"

        # Create instance of SettingsMenu
        root = tk.Tk()
        settings_menu = SettingsMenu(root, controller)

        # Set some values in the comboboxes
        settings_menu.resolution_combobox.set("1024x768")
        settings_menu.theme_combobox.set("clam")
        settings_menu.font_combobox.set("Arial")

        # Call the method
        settings_menu.go_to_main_menu()

        # Check if the comboboxes are reset to default values
        self.assertEqual(settings_menu.resolution_combobox.get(), "Select Resolution")
        self.assertEqual(settings_menu.theme_combobox.get(), "Select Theme")
        self.assertEqual(settings_menu.font_combobox.get(), "Select Font")
        controller.show_frame.assert_called_with("MainMenu")

    def test_set_font(self):
        # Mock the controller
        controller = MagicMock(spec=FlashcardApp)
        controller.current_font = "Arial"
        controller.current_font_size = 12
        controller.current_big_font_size = 14
        controller.bg_color = "#f0f0f0"

        # Create instance of SettingsMenu
        root = tk.Tk()
        settings_menu = SettingsMenu(root, controller)

        # Set a valid font in the combobox
        settings_menu.font_combobox.set("Helvetica")

        # Call the method
        settings_menu.set_font()

        # Check if the controller method was called with the correct argument
        controller.set_font.assert_called_with("Helvetica")

    def test_set_theme(self):
        # Mock the controller
        controller = MagicMock(spec=FlashcardApp)
        controller.current_font = "Arial"
        controller.current_font_size = 12
        controller.current_big_font_size = 14
        controller.bg_color = "#f0f0f0"

        # Create instance of SettingsMenu
        root = tk.Tk()
        settings_menu = SettingsMenu(root, controller)

        # Set a valid theme in the combobox
        settings_menu.theme_combobox.set("clam")

        # Call the method
        settings_menu.set_theme()

        # Check if the controller method was called with the correct argument
        controller.set_theme.assert_called_with("clam")
        
    def test_set_resolution(self):
        # Mock the controller
        controller = MagicMock(spec=FlashcardApp)
        controller.current_font = "Arial"
        controller.current_font_size = 12
        controller.current_big_font_size = 14
        controller.bg_color = "#f0f0f0"

        # Create instance of SettingsMenu
        root = tk.Tk()
        settings_menu = SettingsMenu(root, controller)

        # Set a valid resolution in the combobox
        settings_menu.resolution_combobox.set("1280x720")

        # Call the method
        settings_menu.set_resolution()

        # Check if the controller method was called with the correct argument
        controller.geometry.assert_called_with("1280x720")

if __name__ == "__main__":
    unittest.main()
