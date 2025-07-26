from globals.Util import Globals
import json
from tkinter import  colorchooser
class ThemeController:
    def __init__(self, view):
        self.view = view
        self.theme = None
        self.apply_theme()

    def apply_theme(self):
        """
        Applies the theme to the GUI.
        If there is no theme given it will just use the defaults
        """
        theme = self.load_theme()
        if theme:
            primary_color = theme.get("primary_color", Globals.DEFAULT_PRIMARY)
            off_color = theme.get("off_color", Globals.DEFAULT_OFF)
        else:
            primary_color, off_color = Globals.DEFAULT_PRIMARY, Globals.DEFAULT_OFF
        
        self.view.set_theme(primary_color, off_color)

    def load_theme(self):
        """
        LOADS the theme from the config file to apply it.
        """
        try:
            with open(Globals.CONFIG_FILE, 'r') as file:
                return json.load(file)
        except Exception:
            return None
        
    def change_theme(self):
        """
        Opens a color picker for user to select new primary and off color theme

        Applies the color immediately to the GUI and saves them to the config file so it is saved
        between closing and opening the GUI.
        
        """
        primary = colorchooser.askcolor(title="Choose Primary Color")[1]
        if not primary: return
        off = colorchooser.askcolor(title= "Choose Off Color")[1]
        if not off: return
        self.view.set_theme(primary, off)
        self.save_theme(primary, off)  
        
    def save_theme(self, primary_color, off_color):
        """
        Saves the given color thme to the config file and applies them to the GUI
        """

        config = {
            "primary_color": primary_color,
            "off_color": off_color
        }
        try:
            with open(Globals.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.theme = config
            self.view.set_theme(primary_color, off_color)
            self.view.print_output("Theme saved and applied")
        except Exception as e:
            self.view.print_output(f"Failed to save theme: {e}")

    def reset_theme(self):
        """
        Resets the theme to default colors and updates config
        """
        self.save_theme(Globals.DEFAULT_PRIMARY, Globals.DEFAULT_OFF)
