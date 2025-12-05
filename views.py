# VIEWS - All menu and screen views

import arcade
import arcade.gui
import constants
from constants import (
    CONGRATULATIONS_DELAY,
    UI_BUTTON_WIDTH_LARGE,
    UI_BUTTON_WIDTH_SMALL,
    UI_BUTTON_WIDTH_TINY,
    UI_BUTTON_HEIGHT_LARGE,
    UI_BUTTON_HEIGHT_MEDIUM,
    UI_BUTTON_HEIGHT_SMALL,
    UI_SPACING_LARGE,
    UI_SPACING_MEDIUM,
    UI_SPACING_SMALL,
    UI_SPACING_TINY,
)
from view_manager import GameMode

# Main Menu View with GUI widgets
class MainMenuView(arcade.View):

    def __init__(self, view_manager):
        super().__init__()
        self.view_manager = view_manager
        self.ui = arcade.gui.UIManager()
        
        # Create main layout
        root = arcade.gui.UIAnchorLayout()
        
        # Create vertical box for menu items
        menu_box = arcade.gui.UIBoxLayout(vertical=True, space_between=UI_SPACING_MEDIUM)
        
        # Add title
        title = arcade.gui.UILabel(
            text="Minute Mazes",
            font_size=50,
            text_color=arcade.color.WHITE,
            bold=True
        )
        menu_box.add(title)
        
        # Add some space after title
        menu_box.add(arcade.gui.UISpace(height=UI_SPACING_LARGE))

        # Create Story Mode button
        story_mode_button = arcade.gui.UIFlatButton(
            text="Story Mode",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(story_mode_button)
        
        @story_mode_button.event("on_click")
        def on_story_mode_click(_):
            # Show mouse color selection screen for story mode
            self.view_manager.show_mouse_selection()
        
        # Create Free Play button
        free_play_button = arcade.gui.UIFlatButton(
            text="Free Play",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(free_play_button)
        
        @free_play_button.event("on_click")
        def on_free_play_click(_):
            self.view_manager.show_game(game_mode=GameMode.FREE_PLAY)
        
        # Create settings button
        settings_button = arcade.gui.UIFlatButton(
            text="Settings",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(settings_button)
        
        @settings_button.event("on_click")
        def on_settings_click(_):
            self.view_manager.show_settings(previous_view=None)
        
        # Create quit button
        quit_button = arcade.gui.UIFlatButton(
            text="Quit",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_RED
        )
        menu_box.add(quit_button)
        
        @quit_button.event("on_click")
        def on_quit_click(_):
            arcade.close_window()
        
        # Add instructions at bottom
        menu_box.add(arcade.gui.UISpace(height=UI_SPACING_LARGE))
        instructions = arcade.gui.UILabel(
            text="| WASD or Arrow Keys to Move | R to Restart | ESC or ENTER to Pause | SPACE for Pathfinder |",
            font_size=14,
            text_color=arcade.color.LIGHT_GRAY
        )
        menu_box.add(instructions)
        
        # Center the menu
        root.add(menu_box, anchor_x="center", anchor_y="center")
        self.ui.add(root)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.TEAL)
        self.ui.enable()

    def on_hide_view(self):
        """ Disable UI when leaving view """
        self.ui.disable()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.ui.draw()

# For selecting mouse color at the start of story mode
class MouseSelectionView(arcade.View):

    def __init__(self, view_manager):
        super().__init__()
        self.view_manager = view_manager
        self.ui = arcade.gui.UIManager()
        
        # Create main layout
        root = arcade.gui.UIAnchorLayout()
        
        # Create vertical box for menu items
        menu_box = arcade.gui.UIBoxLayout(vertical=True, space_between=UI_SPACING_MEDIUM)
        
        # Add title
        title = arcade.gui.UILabel(
            text="Choose Your Mouse",
            font_size=42,
            text_color=arcade.color.WHITE,
            bold=True
        )
        menu_box.add(title)
        
        # Add subtitle
        subtitle = arcade.gui.UILabel(
            text="Your choice is locked for Story Mode",
            font_size=18,
            text_color=arcade.color.LIGHT_GRAY
        )
        menu_box.add(subtitle)
        
        menu_box.add(arcade.gui.UISpace(height=UI_SPACING_MEDIUM))
        
        # Create horizontal box for mouse color buttons
        mouse_button_box = arcade.gui.UIBoxLayout(vertical=False, space_between=UI_SPACING_MEDIUM)
        
        # White mouse button
        white_button = arcade.gui.UIFlatButton(
            text="White Mouse",
            width=UI_BUTTON_WIDTH_SMALL,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        mouse_button_box.add(white_button)
        
        @white_button.event("on_click")
        def on_white_click(_):
            self.view_manager.show_game(game_mode=GameMode.STORY_MODE, story_mouse_color="white")
        
        # Grey mouse button
        grey_button = arcade.gui.UIFlatButton(
            text="Grey Mouse",
            width=UI_BUTTON_WIDTH_SMALL,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        mouse_button_box.add(grey_button)
        
        @grey_button.event("on_click")
        def on_grey_click(_):
            self.view_manager.show_game(game_mode=GameMode.STORY_MODE, story_mouse_color="grey")
        
        # Brown mouse button
        brown_button = arcade.gui.UIFlatButton(
            text="Brown Mouse",
            width=UI_BUTTON_WIDTH_SMALL,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        mouse_button_box.add(brown_button)
        
        @brown_button.event("on_click")
        def on_brown_click(_):
            self.view_manager.show_game(game_mode=GameMode.STORY_MODE, story_mouse_color="brown")
        
        menu_box.add(mouse_button_box)
        
        menu_box.add(arcade.gui.UISpace(height=UI_SPACING_LARGE))
        
        # Back button
        back_button = arcade.gui.UIFlatButton(
            text="Back to Main Menu",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_MEDIUM,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(back_button)
        
        @back_button.event("on_click")
        def on_back_click(_):
            self.view_manager.show_main_menu()
        
        # Center the menu
        root.add(menu_box, anchor_x="center", anchor_y="center")
        self.ui.add(root)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.TEAL)
        self.ui.enable()

    def on_hide_view(self):
        """ Disable UI when leaving view """
        self.ui.disable()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.ui.draw()

# Settings Menu View with maze size options
class SettingsView(arcade.View):

    def __init__(self, view_manager, previous_view=None, game_mode=GameMode.FREE_PLAY):
        super().__init__()
        self.view_manager = view_manager
        self.previous_view = previous_view  # Store the view that opened settings
        self.game_mode = game_mode
        self.ui = arcade.gui.UIManager()
        
        # Create main layout
        root = arcade.gui.UIAnchorLayout()
        
        # Create vertical box for menu items
        menu_box = arcade.gui.UIBoxLayout(vertical=True, space_between=12)
        
        # Add title
        title = arcade.gui.UILabel(
            text="Settings",
            font_size=42,
            text_color=arcade.color.WHITE,
            bold=True
        )
        menu_box.add(title)
        
        menu_box.add(arcade.gui.UISpace(height=15))
        
        if self.game_mode == GameMode.FREE_PLAY:
            # Add maze size label
            size_label = arcade.gui.UILabel(
                text="Maze Size",
                font_size=20,
                text_color=arcade.color.WHITE,
                bold=True
            )
            menu_box.add(size_label)
            
            menu_box.add(arcade.gui.UISpace(height=5))
            
            # Create horizontal box for size buttons to save vertical space
            size_button_box = arcade.gui.UIBoxLayout(vertical=False, space_between=UI_SPACING_TINY)
            
            small_button = arcade.gui.UIFlatButton(
                text="Small",
                width=UI_BUTTON_WIDTH_TINY,
                height=UI_BUTTON_HEIGHT_SMALL,
                style=arcade.gui.UIFlatButton.STYLE_BLUE if constants.MAZE_SIZE_SETTING == 21 else None
            )
            size_button_box.add(small_button)
            
            @small_button.event("on_click")
            def on_small_click(_):
                constants.MAZE_SIZE_SETTING = 21
                self.view_manager.show_settings(previous_view=self.previous_view, game_mode=self.game_mode)
            
            medium_button = arcade.gui.UIFlatButton(
                text="Medium",
                width=UI_BUTTON_WIDTH_TINY,
                height=UI_BUTTON_HEIGHT_SMALL,
                style=arcade.gui.UIFlatButton.STYLE_BLUE if constants.MAZE_SIZE_SETTING == 31 else None
            )
            size_button_box.add(medium_button)
            
            @medium_button.event("on_click")
            def on_medium_click(_):
                constants.MAZE_SIZE_SETTING = 31
                self.view_manager.show_settings(previous_view=self.previous_view, game_mode=self.game_mode)
            
            large_button = arcade.gui.UIFlatButton(
                text="Large",
                width=UI_BUTTON_WIDTH_TINY,
                height=UI_BUTTON_HEIGHT_SMALL,
                style=arcade.gui.UIFlatButton.STYLE_BLUE if constants.MAZE_SIZE_SETTING == 51 else None
            )
            size_button_box.add(large_button)
            
            @large_button.event("on_click")
            def on_large_click(_):
                constants.MAZE_SIZE_SETTING = 51
                self.view_manager.show_settings(previous_view=self.previous_view, game_mode=self.game_mode)
            
            menu_box.add(size_button_box)
            
            menu_box.add(arcade.gui.UISpace(height=UI_SPACING_SMALL))

            # Mouse color section
            mouse_label = arcade.gui.UILabel(
                text="Mouse Color",
                font_size=20,
                text_color=arcade.color.WHITE,
                bold=True
            )
            menu_box.add(mouse_label)
            
            menu_box.add(arcade.gui.UISpace(height=5))
            
            # Create horizontal box for mouse color buttons
            mouse_button_box = arcade.gui.UIBoxLayout(vertical=False, space_between=UI_SPACING_TINY)
            
            white_button = arcade.gui.UIFlatButton(
                text="White",
                width=UI_BUTTON_WIDTH_TINY,
                height=UI_BUTTON_HEIGHT_SMALL,
                style=arcade.gui.UIFlatButton.STYLE_BLUE if constants.MOUSE_COLOR_SETTING == "white" else None
            )
            mouse_button_box.add(white_button)
            
            @white_button.event("on_click")
            def on_white_click(_):
                constants.MOUSE_COLOR_SETTING = "white"
                self.view_manager.show_settings(previous_view=self.previous_view, game_mode=self.game_mode)
            
            grey_button = arcade.gui.UIFlatButton(
                text="Grey",
                width=UI_BUTTON_WIDTH_TINY,
                height=UI_BUTTON_HEIGHT_SMALL,
                style=arcade.gui.UIFlatButton.STYLE_BLUE if constants.MOUSE_COLOR_SETTING == "grey" else None
            )
            mouse_button_box.add(grey_button)
            
            @grey_button.event("on_click")
            def on_grey_click(_):
                constants.MOUSE_COLOR_SETTING = "grey"
                self.view_manager.show_settings(previous_view=self.previous_view, game_mode=self.game_mode)
            
            brown_button = arcade.gui.UIFlatButton(
                text="Brown",
                width=UI_BUTTON_WIDTH_TINY,
                height=UI_BUTTON_HEIGHT_SMALL,
                style=arcade.gui.UIFlatButton.STYLE_BLUE if constants.MOUSE_COLOR_SETTING == "brown" else None
            )
            mouse_button_box.add(brown_button)
            
            @brown_button.event("on_click")
            def on_brown_click(_):
                constants.MOUSE_COLOR_SETTING = "brown"
                self.view_manager.show_settings(previous_view=self.previous_view, game_mode=self.game_mode)            
            menu_box.add(mouse_button_box)
            
            menu_box.add(arcade.gui.UISpace(height=UI_SPACING_SMALL))
        
        # Volume section - combine label and percentage
        volume_header_box = arcade.gui.UIBoxLayout(vertical=False, space_between=UI_SPACING_TINY)
        
        volume_label = arcade.gui.UILabel(
            text="Volume:",
            font_size=20,
            text_color=arcade.color.WHITE,
            bold=True
        )
        volume_header_box.add(volume_label)
        
        # Volume percentage display
        volume_percent = int(constants.VOLUME_SETTING * 100)
        volume_display = arcade.gui.UILabel(
            text=f"{volume_percent}%",
            font_size=20,
            text_color=arcade.color.YELLOW,
            bold=True
        )
        volume_header_box.add(volume_display)
        
        menu_box.add(volume_header_box)
        
        menu_box.add(arcade.gui.UISpace(height=5))
        
        # Volume slider
        volume_slider = arcade.gui.UISlider(
            value=constants.VOLUME_SETTING * 100,  # Convert to 0-100 range
            min_value=0,
            max_value=100,
            width=UI_BUTTON_WIDTH_LARGE,
            height=20
        )
        menu_box.add(volume_slider)
        
        @volume_slider.event("on_change")
        def on_slider_change(event):
            constants.VOLUME_SETTING = event.new_value / 100.0  # Convert back to 0.0-1.0
            # Update the volume display label
            volume_display.text = f"{int(event.new_value)}%"
        
        menu_box.add(arcade.gui.UISpace(height=UI_SPACING_SMALL))
        
        # Back button - returns to previous view or main menu
        back_text = "Back" if self.previous_view else "Back to Main Menu"
        back_button = arcade.gui.UIFlatButton(
            text=back_text,
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_MEDIUM,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(back_button)
        
        @back_button.event("on_click")
        def on_back_click(_):
            if self.previous_view:
                # Return to the view that opened settings (e.g., InGameMenuView)
                self.window.show_view(self.previous_view)
            else:
                # No previous view, return to main menu
                self.view_manager.show_main_menu()
        
        # Center the menu
        root.add(menu_box, anchor_x="center", anchor_y="center")
        self.ui.add(root)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.TEAL)
        self.ui.enable()

    def on_hide_view(self):
        """ Disable UI when leaving view """
        self.ui.disable()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.ui.draw()

# In-Game Pause Menu with GUI widgets
class InGameMenuView(arcade.View):

    def __init__(self, view_manager, game_view):
        super().__init__()
        self.game_view = game_view
        self.view_manager = view_manager
        self.ui = arcade.gui.UIManager()
        
        # Create main layout
        root = arcade.gui.UIAnchorLayout()
        
        # Create vertical box for menu items
        menu_box = arcade.gui.UIBoxLayout(vertical=True, space_between=15)
        
        # Add title
        title = arcade.gui.UILabel(
            text="PAUSED",
            font_size=50,
            text_color=arcade.color.WHITE,
            bold=True
        )
        menu_box.add(title)
        
        menu_box.add(arcade.gui.UISpace(height=30))
        
        # Create resume button
        resume_button = arcade.gui.UIFlatButton(
            text="Resume",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(resume_button)
        
        @resume_button.event("on_click")
        def on_resume_click(_):
            self.window.show_view(self.game_view)
        
        # Create settings button
        settings_button = arcade.gui.UIFlatButton(
            text="Settings",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(settings_button)
        
        @settings_button.event("on_click")
        def on_settings_click(_):
            from view_manager import GameMode
            self.view_manager.show_settings(previous_view=self, game_mode=self.game_view.game_mode)

        
        # Create main menu button
        main_menu_button = arcade.gui.UIFlatButton(
            text="Main Menu",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(main_menu_button)
        
        @main_menu_button.event("on_click")
        def on_main_menu_click(_):
            self.view_manager.show_main_menu()
        
        # Create quit button
        quit_button = arcade.gui.UIFlatButton(
            text="Quit",
            width=UI_BUTTON_WIDTH_LARGE,
            height=UI_BUTTON_HEIGHT_LARGE,
            style=arcade.gui.UIFlatButton.STYLE_RED
        )
        menu_box.add(quit_button)
        
        @quit_button.event("on_click")
        def on_quit_click(_):
            arcade.close_window()
        
        # Add instructions at bottom
        menu_box.add(arcade.gui.UISpace(height=UI_SPACING_LARGE))
        instructions = arcade.gui.UILabel(
            text="| WASD or Arrow Keys to Move | R to Restart | ESC or ENTER to Pause | SPACE for Pathfinder |",
            font_size=14,
            text_color=arcade.color.LIGHT_GRAY
        )
        menu_box.add(instructions)
        
        # Center the menu
        root.add(menu_box, anchor_x="center", anchor_y="center")
        self.ui.add(root)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        # Clear pathfinder when showing pause menu
        if self.game_view.pathfinder_active:
            self.game_view.clear_pathfinder()
            # Restore black tile
            if len(self.game_view.path_list) == 0:
                self.game_view._create_exit_black_tile()
        self.ui.enable()

    def on_hide_view(self):
        """ Disable UI when leaving view """
        self.ui.disable()

    def on_draw(self):
        """ Render the screen with semi-transparent overlay. """
        # Draw the game view underneath (frozen state)
        self.game_view.on_draw()
        
        # Draw semi-transparent dark overlay
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.window.width,
            0,
            self.window.height,
            (0, 0, 0, 200)  # Black with alpha
        )
        
        # Draw the UI on top
        self.ui.draw()

# Congratulations View with GUI widgets
class CongratulationsView(arcade.View):

    def __init__(self, view_manager, game_view):
        super().__init__()
        self.view_manager = view_manager
        self.game_view = game_view
        self.display_timer = 0
        self.ui = arcade.gui.UIManager()
        
        # Create main layout
        root = arcade.gui.UIAnchorLayout()
        
        # Create vertical box for content
        content_box = arcade.gui.UIBoxLayout(vertical=True, space_between=15)
        
        # Add congratulations title
        title = arcade.gui.UILabel(
            text="Congratulations!",
            font_size=50,
            text_color=arcade.color.WHITE,
            bold=True
        )
        content_box.add(title)
        
        # Add subtitle
        subtitle = arcade.gui.UILabel(
            text="Maze Completed!",
            font_size=30,
            text_color=arcade.color.WHITE
        )
        content_box.add(subtitle)
        
        content_box.add(arcade.gui.UISpace(height=30))

        # Add score label
        score_text = f"Score: {self.game_view.score}"
        score_label = arcade.gui.UILabel(
            text=score_text,
            font_size=15,
            text_color=arcade.color.LIGHT_GRAY
        )
        content_box.add(score_label)

        # Add total score label
        grand_total_score_text = f"Total Score: {self.game_view.grand_total_score}"
        grand_total_score_label = arcade.gui.UILabel(
            text=grand_total_score_text,
            font_size=15,
            text_color=arcade.color.LIGHT_GRAY
        )
        content_box.add(grand_total_score_label)
        
        # Add time label
        time_text = f"Time: {self.game_view.elapsed_time:.3f} s"
        time_label = arcade.gui.UILabel(
            text=time_text,
            font_size=15,
            text_color=arcade.color.LIGHT_GRAY
        )
        content_box.add(time_label)
        
        # Add best time if it exists
        if self.game_view.best_time is not None:
            if (self.game_view.elapsed_time < self.game_view.best_time):
                best_time_label = arcade.gui.UILabel(
                text=f"Best Time: {self.game_view.elapsed_time:.3f} s",
                font_size=15,
                text_color=arcade.color.YELLOW
            )
            else:
                best_time_label = arcade.gui.UILabel(
                text=f"Best Time: {self.game_view.best_time:.3f} s",
                font_size=15,
                text_color=arcade.color.YELLOW
            )
            content_box.add(best_time_label)
        
        # Add completed mazes count (add 1 since this maze was just completed)
        mazes_label = arcade.gui.UILabel(
            text=f"Mazes Completed: {self.game_view.completed_mazes + 1}",
            font_size=15,
            text_color=arcade.color.LIGHT_GRAY
        )
        content_box.add(mazes_label)
        
        content_box.add(arcade.gui.UISpace(height=UI_SPACING_LARGE))
        
        # Create button row for actions
        button_row = arcade.gui.UIBoxLayout(vertical=False, space_between=UI_SPACING_SMALL)
        
        # Main menu button (first)
        menu_button = arcade.gui.UIFlatButton(
            text="Main Menu",
            width=150,
            height=45,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        button_row.add(menu_button)
        
        @menu_button.event("on_click")
        def on_menu_click(_):
            self.view_manager.show_main_menu()
        
        # Replay button (middle)
        replay_button = arcade.gui.UIFlatButton(
            text="Replay Maze",
            width=150,
            height=45,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        button_row.add(replay_button)
        
        @replay_button.event("on_click")
        def on_replay_click(_):
            # Score is already in grand total, don't deduct it
            self.game_view.restart_maze(deduct_score=False)
            # Return to game view
            self.window.show_view(self.game_view)
        
        # Next maze button (last)
        next_button = arcade.gui.UIFlatButton(
            text="Next Maze",
            width=150,
            height=45,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        button_row.add(next_button)
        
        @next_button.event("on_click")
        def on_next_click(_):
            # Update best time
            if self.game_view.best_time is None or self.game_view.elapsed_time < self.game_view.best_time:
                self.game_view.best_time = self.game_view.elapsed_time
            
            # Increment completed mazes counter
            self.game_view.completed_mazes += 1
            # Reset elapsed time
            self.game_view.elapsed_time = 0
            # Generate new maze
            self.game_view.setup()
            # Return to game view
            self.window.show_view(self.game_view)
        
        content_box.add(button_row)
        
        # Add auto-advance notice
        notice = arcade.gui.UILabel(
            text=f"Auto-advancing in {CONGRATULATIONS_DELAY:.0f} seconds...",
            font_size=14,
            text_color=arcade.color.LIGHT_GRAY,
            italic=True
        )
        content_box.add(notice)
        
        # Center everything
        root.add(content_box, anchor_x="center", anchor_y="center")
        self.ui.add(root)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.TEAL)
        self.display_timer = 0
        self.ui.enable()

    def on_hide_view(self):
        """ Disable UI when leaving view """
        self.ui.disable()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.ui.draw()
        
    def on_update(self, delta_time):
        """ Update the view """
        self.display_timer += delta_time
        if self.display_timer >= CONGRATULATIONS_DELAY:  # After a few seconds
            # Update best time
            if self.game_view.best_time is None or self.game_view.elapsed_time < self.game_view.best_time:
                self.game_view.best_time = self.game_view.elapsed_time

            # Increment completed mazes counter
            self.game_view.completed_mazes += 1
            # Reset elapsed time
            self.game_view.elapsed_time = 0
            # Generate new maze
            self.game_view.setup()
            # Return to game view
            self.window.show_view(self.game_view)

# Grand victory shown when player completes all 10 mazes in story mode
class StoryVictoryView(arcade.View):

    def __init__(self, view_manager, game_view):
        super().__init__()
        self.view_manager = view_manager
        self.game_view = game_view
        self.ui = arcade.gui.UIManager()
        
        # Create main layout
        root = arcade.gui.UIAnchorLayout()
        
        # Create vertical box for content
        content_box = arcade.gui.UIBoxLayout(vertical=True, space_between=UI_SPACING_MEDIUM)
        
        # Add victory title
        title = arcade.gui.UILabel(
            text="STORY COMPLETE!",
            font_size=60,
            text_color=arcade.color.GOLD,
            bold=True
        )
        content_box.add(title)
        
        # Add congratulations message
        subtitle = arcade.gui.UILabel(
            text="You've conquered all 10 mazes!",
            font_size=30,
            text_color=arcade.color.WHITE
        )
        content_box.add(subtitle)
        
        content_box.add(arcade.gui.UISpace(height=UI_SPACING_LARGE))
        
        # Add statistics
        total_score_text = f"Total Cheese Collected: {self.game_view.grand_total_score}"
        score_label = arcade.gui.UILabel(
            text=total_score_text,
            font_size=20,
            text_color=arcade.color.YELLOW
        )
        content_box.add(score_label)
        
        # Add total time if tracked
        if hasattr(game_view, 'total_story_time'):
            time_text = f"Total Time: {self.game_view.total_story_time:.2f} seconds"
            time_label = arcade.gui.UILabel(
                text=time_text,
                font_size=20,
                text_color=arcade.color.WHITE
            )
            content_box.add(time_label)
        
        content_box.add(arcade.gui.UISpace(height=UI_SPACING_LARGE))
        
        # Main menu button
        menu_button = arcade.gui.UIFlatButton(
            text="Return to Main Menu",
            width=300,
            height=60,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        content_box.add(menu_button)
        
        @menu_button.event("on_click")
        def on_menu_click(_):
            self.view_manager.show_main_menu()
        
        # Center everything
        root.add(content_box, anchor_x="center", anchor_y="center")
        self.ui.add(root)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.TEAL)
        self.ui.enable()

    def on_hide_view(self):
        """ Disable UI when leaving view """
        self.ui.disable()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.ui.draw()
