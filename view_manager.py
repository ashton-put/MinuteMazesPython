# VIEW MANAGER

import arcade
from enum import Enum

class GameMode(Enum):
    STORY_MODE = "story_mode"
    FREE_PLAY = "free_play"

# Manages all view transitions and acts as a mediator between views and game.
class ViewManager:
    
    def __init__(self, window):
        self.window = window
    
    def show_main_menu(self):
        """Show the main menu."""
        from views import MainMenuView
        view = MainMenuView(self)
        self.window.show_view(view)
    
    def show_mouse_selection(self):
        """Show mouse color selection for story mode."""
        from views import MouseSelectionView
        view = MouseSelectionView(self)
        self.window.show_view(view)
    
    def show_game(self, game_mode=GameMode.FREE_PLAY, story_mouse_color="white"):
        """Create and show a new game."""
        from game import GameView
        game_view = GameView(self, game_mode=game_mode, story_mouse_color=story_mouse_color)
        game_view.setup()
        self.window.show_view(game_view)
    
    def show_settings(self, previous_view=None, game_mode=GameMode.FREE_PLAY):
        """Show settings menu."""
        from views import SettingsView
        view = SettingsView(self, previous_view=previous_view, game_mode=game_mode)
        self.window.show_view(view)
    
    def show_in_game_menu(self, game_view):
        """Show pause menu during gameplay."""
        from views import InGameMenuView
        view = InGameMenuView(self, game_view)
        self.window.show_view(view)
    
    def show_congratulations(self, game_view):
        """Show congratulations screen after completing a maze."""
        from views import CongratulationsView
        view = CongratulationsView(self, game_view)
        self.window.show_view(view)
    
    def show_story_victory(self, game_view):
        """Show story mode victory screen."""
        from views import StoryVictoryView
        view = StoryVictoryView(self, game_view)
        self.window.show_view(view)