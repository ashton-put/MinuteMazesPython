# CLASSES

import random
import arcade
import arcade.gui
from constants import (
    SPRITE_SCALING,
    SPRITE_SIZE,
    WINDOW_HEIGHT,
    TILE_EMPTY,
    TILE_CRATE,
    MERGE_SPRITES,
    MOVEMENT_SPEED,
    CAMERA_SPEED,
    CONGRATULATIONS_DELAY
)
from functions import make_maze, astar

# Global maze size setting (can be changed in settings)
MAZE_SIZE_SETTING = 51  # Default to large (options: 21, 31, 51)

# Global mouse color setting (can be changed in settings)
MOUSE_COLOR_SETTING = "white"  # Default to white (options: "white", "grey", "brown")

# Global volume setting (can be changed in settings)
VOLUME_SETTING = 0.5  # Default to 50% (range: 0.0 to 1.0)

# Main Menu View with GUI widgets
class MainMenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()
        
        # Create main layout
        root = arcade.gui.UIAnchorLayout()
        
        # Create vertical box for menu items
        menu_box = arcade.gui.UIBoxLayout(vertical=True, space_between=20)
        
        # Add title
        title = arcade.gui.UILabel(
            text="Minute Mazes",
            font_size=50,
            text_color=arcade.color.WHITE,
            bold=True
        )
        menu_box.add(title)
        
        # Add some space after title
        menu_box.add(arcade.gui.UISpace(height=30))
        
        # Create start button
        start_button = arcade.gui.UIFlatButton(
            text="Start Game",
            width=250,
            height=50,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(start_button)
        
        @start_button.event("on_click")
        def on_start_click(_):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        
        # Create settings button
        settings_button = arcade.gui.UIFlatButton(
            text="Settings",
            width=250,
            height=50,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(settings_button)
        
        @settings_button.event("on_click")
        def on_settings_click(_):
            settings_view = SettingsView(previous_view=None)
            self.window.show_view(settings_view)
        
        # Create quit button
        quit_button = arcade.gui.UIFlatButton(
            text="Quit",
            width=250,
            height=50,
            style=arcade.gui.UIFlatButton.STYLE_RED
        )
        menu_box.add(quit_button)
        
        @quit_button.event("on_click")
        def on_quit_click(_):
            arcade.close_window()
        
        # Add instructions at bottom
        menu_box.add(arcade.gui.UISpace(height=40))
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

# Settings Menu View with maze size options
class SettingsView(arcade.View):

    def __init__(self, previous_view=None):
        super().__init__()
        self.previous_view = previous_view  # Store the view that opened settings
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
        size_button_box = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        # Create horizontal box for size buttons to save vertical space
        size_button_box = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        
        small_button = arcade.gui.UIFlatButton(
            text="Small",
            width=75,
            height=40,
            style=arcade.gui.UIFlatButton.STYLE_BLUE if MAZE_SIZE_SETTING == 21 else None
        )
        size_button_box.add(small_button)
        
        @small_button.event("on_click")
        def on_small_click(_):
            global MAZE_SIZE_SETTING
            MAZE_SIZE_SETTING = 21
            self.window.show_view(SettingsView(previous_view=self.previous_view))  # Preserve previous view
        
        medium_button = arcade.gui.UIFlatButton(
            text="Medium",
            width=75,
            height=40,
            style=arcade.gui.UIFlatButton.STYLE_BLUE if MAZE_SIZE_SETTING == 31 else None
        )
        size_button_box.add(medium_button)
        
        @medium_button.event("on_click")
        def on_medium_click(_):
            global MAZE_SIZE_SETTING
            MAZE_SIZE_SETTING = 31
            self.window.show_view(SettingsView(previous_view=self.previous_view))  # Preserve previous view
        
        large_button = arcade.gui.UIFlatButton(
            text="Large",
            width=75,
            height=40,
            style=arcade.gui.UIFlatButton.STYLE_BLUE if MAZE_SIZE_SETTING == 51 else None
        )
        size_button_box.add(large_button)
        
        @large_button.event("on_click")
        def on_large_click(_):
            global MAZE_SIZE_SETTING
            MAZE_SIZE_SETTING = 51
            self.window.show_view(SettingsView(previous_view=self.previous_view))  # Preserve previous view
        
        menu_box.add(size_button_box)
        
        menu_box.add(arcade.gui.UISpace(height=15))

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
        mouse_button_box = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        
        white_button = arcade.gui.UIFlatButton(
            text="White",
            width=75,
            height=40,
            style=arcade.gui.UIFlatButton.STYLE_BLUE if MOUSE_COLOR_SETTING == "white" else None
        )
        mouse_button_box.add(white_button)
        
        @white_button.event("on_click")
        def on_white_click(_):
            global MOUSE_COLOR_SETTING
            MOUSE_COLOR_SETTING = "white"
            self.window.show_view(SettingsView(previous_view=self.previous_view))
        
        grey_button = arcade.gui.UIFlatButton(
            text="Grey",
            width=75,
            height=40,
            style=arcade.gui.UIFlatButton.STYLE_BLUE if MOUSE_COLOR_SETTING == "grey" else None
        )
        mouse_button_box.add(grey_button)
        
        @grey_button.event("on_click")
        def on_grey_click(_):
            global MOUSE_COLOR_SETTING
            MOUSE_COLOR_SETTING = "grey"
            self.window.show_view(SettingsView(previous_view=self.previous_view))
        
        brown_button = arcade.gui.UIFlatButton(
            text="Brown",
            width=75,
            height=40,
            style=arcade.gui.UIFlatButton.STYLE_BLUE if MOUSE_COLOR_SETTING == "brown" else None
        )
        mouse_button_box.add(brown_button)
        
        @brown_button.event("on_click")
        def on_brown_click(_):
            global MOUSE_COLOR_SETTING
            MOUSE_COLOR_SETTING = "brown"
            self.window.show_view(SettingsView(previous_view=self.previous_view))
        
        menu_box.add(mouse_button_box)
        
        menu_box.add(arcade.gui.UISpace(height=15))
        
        # Volume section - combine label and percentage
        volume_header_box = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        
        volume_label = arcade.gui.UILabel(
            text="Volume:",
            font_size=20,
            text_color=arcade.color.WHITE,
            bold=True
        )
        volume_header_box.add(volume_label)
        
        # Volume percentage display
        volume_percent = int(VOLUME_SETTING * 100)
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
            value=VOLUME_SETTING * 100,  # Convert to 0-100 range
            min_value=0,
            max_value=100,
            width=250,
            height=20
        )
        menu_box.add(volume_slider)
        
        @volume_slider.event("on_change")
        def on_slider_change(event):
            global VOLUME_SETTING
            VOLUME_SETTING = event.new_value / 100.0  # Convert back to 0.0-1.0
            # Update the volume display label
            volume_display.text = f"{int(event.new_value)}%"
        
        menu_box.add(arcade.gui.UISpace(height=15))
        
        # Back button - returns to previous view or main menu
        back_text = "Back" if self.previous_view else "Back to Main Menu"
        back_button = arcade.gui.UIFlatButton(
            text=back_text,
            width=250,
            height=45,
            style=arcade.gui.UIFlatButton.STYLE_RED
        )
        menu_box.add(back_button)
        
        @back_button.event("on_click")
        def on_back_click(_):
            if self.previous_view:
                # Return to the view that opened settings (e.g., InGameMenuView)
                self.window.show_view(self.previous_view)
            else:
                # No previous view, return to main menu
                main_menu = MainMenuView()
                self.window.show_view(main_menu)
        
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

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui = arcade.gui.UIManager()
        
        # Clear pathfinder when entering pause menu
        if hasattr(game_view, 'pathfinder_active') and game_view.pathfinder_active:
            black_tile = game_view.path_list[0] if len(game_view.path_list) > 0 else None
            game_view.path_list = arcade.SpriteList()
            if black_tile:
                game_view.path_list.append(black_tile)
            game_view.pathfinder_active = False
            game_view.pathfinder_timer = 0.0
        
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
            width=250,
            height=50,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(resume_button)
        
        @resume_button.event("on_click")
        def on_resume_click(_):
            self.window.show_view(self.game_view)
        
        # Create settings button
        settings_button = arcade.gui.UIFlatButton(
            text="Settings",
            width=250,
            height=50,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(settings_button)
        
        @settings_button.event("on_click")
        def on_settings_click(_):
            settings_view = SettingsView(previous_view=self)
            self.window.show_view(settings_view)
        
        # Create main menu button
        main_menu_button = arcade.gui.UIFlatButton(
            text="Main Menu",
            width=250,
            height=50,
            style=arcade.gui.UIFlatButton.STYLE_BLUE
        )
        menu_box.add(main_menu_button)
        
        @main_menu_button.event("on_click")
        def on_main_menu_click(_):
            main_menu_view = MainMenuView()
            self.window.show_view(main_menu_view)
        
        # Create quit button
        quit_button = arcade.gui.UIFlatButton(
            text="Quit",
            width=250,
            height=50,
            style=arcade.gui.UIFlatButton.STYLE_RED
        )
        menu_box.add(quit_button)
        
        @quit_button.event("on_click")
        def on_quit_click(_):
            arcade.close_window()
        
        # Add instructions at bottom
        menu_box.add(arcade.gui.UISpace(height=40))
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

    def __init__(self, game_view):
        super().__init__()
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
        
        content_box.add(arcade.gui.UISpace(height=20))
        
        # Add time label
        time_text = f"Time: {self.game_view.elapsed_time:.1f} seconds"
        time_label = arcade.gui.UILabel(
            text=time_text,
            font_size=24,
            text_color=arcade.color.LIGHT_GRAY
        )
        content_box.add(time_label)
        
        # Add best time if it exists
        if self.game_view.best_time is not None:
            if (self.game_view.elapsed_time < self.game_view.best_time):
                best_time_label = arcade.gui.UILabel(
                text=f"Best Time: {self.game_view.elapsed_time:.1f} seconds",
                font_size=20,
                text_color=arcade.color.YELLOW
            )
            else:
                best_time_label = arcade.gui.UILabel(
                text=f"Best Time: {self.game_view.best_time:.1f} seconds",
                font_size=20,
                text_color=arcade.color.YELLOW
            )
            content_box.add(best_time_label)
        
        # Add completed mazes count (add 1 since this maze was just completed)
        mazes_label = arcade.gui.UILabel(
            text=f"Mazes Completed: {self.game_view.completed_mazes + 1}",
            font_size=20,
            text_color=arcade.color.LIGHT_GRAY
        )
        content_box.add(mazes_label)
        
        content_box.add(arcade.gui.UISpace(height=30))
        
        # Create button row for actions
        button_row = arcade.gui.UIBoxLayout(vertical=False, space_between=15)
        
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
            main_menu_view = MainMenuView()
            self.window.show_view(main_menu_view)
        
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

# Main application class
class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.floor_list = None
        self.path_list = None  
        self.coin_list = None  
        self.exit_list = None 

        # Player info
        self.player_sprite = None
        self.score = 0
        self.grand_total_score = 0  # Cumulative score across all mazes

        # Physics engine
        self.physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        # Elapsed time
        self.elapsed_time = 0

        # Completed mazes counter
        self.completed_mazes = 0

        # Best time tracking
        self.best_time = None
        
        # Store initial player position for restart
        self.initial_player_x = SPRITE_SIZE + SPRITE_SIZE / 2
        self.initial_player_y = SPRITE_SIZE + SPRITE_SIZE / 2


    # Restart the current maze without regenerating it
    # deduct_score: If True, deduct collected coins from grand total (for mid-game restart).
                  # If False, keep grand total intact (for replay after completion).
    def restart_maze(self, deduct_score=True):
        # Deduct collected coins from grand total only if mid-game restart
        if deduct_score:
            self.grand_total_score -= self.score
        
        # Reset current maze score
        self.score = 0
        
        # Reset elapsed time
        self.elapsed_time = 0
        
        # Restore all coins to the maze
        for coin in self.coin_list:
            coin.visible = True
        
        # Reset player position to spawn point
        self.player_sprite.center_x = self.initial_player_x
        self.player_sprite.center_y = self.initial_player_y
        
        # Stop player movement
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
        # Clear pathfinder visualization
        if hasattr(self, 'pathfinder_active'):
            if self.pathfinder_active:
                black_tile = self.path_list[0] if len(self.path_list) > 0 else None
                self.path_list = arcade.SpriteList()
                if black_tile:
                    self.path_list.append(black_tile)
                self.pathfinder_active = False
                self.pathfinder_timer = 0.0
        
        # Reset camera to player
        self.camera_sprites.position = (self.player_sprite.center_x, self.player_sprite.center_y)


    # Set up the game and initialize the variables
    def setup(self):

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.path_list = arcade.SpriteList()  
        self.coin_list = arcade.SpriteList()  
        self.exit_list = arcade.SpriteList() 

        self.score = 0

        # Set camera zoom
        self.camera_sprites.zoom = 2.0

        # Load textures for left and right facing mouse based on setting
        mouse_filename = f"images/sprites/{MOUSE_COLOR_SETTING}_mouse.png"
        self.mouse_texture_right = arcade.load_texture(mouse_filename)
        self.mouse_texture_left = self.mouse_texture_right.flip_left_right()

        # Sound effects
        self.coin_sound = arcade.Sound("sounds/collect.wav")
        self.pathfinder_sound = arcade.Sound("sounds/pathfinder.wav")
        self.exit_sound = arcade.Sound("sounds/exit.wav")

        # Pathfinder power variables
        self.pathfinder_uses_remaining = 3  # Uses available
        self.pathfinder_max_uses = 3  # Maximum uses per maze
        self.pathfinder_active = False  # Is path currently shown?
        self.pathfinder_timer = 0.0  # Timer for auto-hide
        self.pathfinder_duration = 3.0  # How long path stays visible (seconds)
        self.pathfinder_max_tiles = 10  # Maximum path tiles to show

        # Create the maze using the current size setting
        maze = make_maze(MAZE_SIZE_SETTING, MAZE_SIZE_SETTING)
        self.maze = maze  # Store maze for pathfinding

        # Create sprites based on 2D grid
        if not MERGE_SPRITES:
            # This is the simple-to-understand method. Each grid location
            # is a sprite
            for row in range(MAZE_SIZE_SETTING):
                for column in range(MAZE_SIZE_SETTING):
                    if maze[row][column] == TILE_CRATE:
                        wall = arcade.Sprite(
                            "images/tiles/blankTile.png",
                            scale=SPRITE_SCALING,
                        )
                        wall.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                        wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                        self.wall_list.append(wall)
        else:
            # This uses new Arcade 1.3.1 features, that allow me to create a
            # larger sprite with a repeating texture. So if there are multiple
            # cells in a row with a wall, we merge them into one sprite, with a
            # repeating texture for each cell. This reduces our sprite count
            for row in range(MAZE_SIZE_SETTING):
                column = 0
                while column < len(maze):
                    while column < len(maze) and maze[row][column] == TILE_EMPTY:
                        column += 1
                    start_column = column
                    while column < len(maze) and maze[row][column] == TILE_CRATE:
                        column += 1
                    end_column = column - 1

                    column_count = end_column - start_column + 1
                    column_mid = (start_column + end_column) / 2
                    
                    # Set wall sprite
                    wall = arcade.Sprite(
                        "images/tiles/blankTile.png",
                        scale=SPRITE_SCALING,
                    )
                    wall.center_x = column_mid * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.width = SPRITE_SIZE * column_count

                    # SET MAZE WALL COLOR
                    wall.color = arcade.color.DODGER_BLUE

                    self.wall_list.append(wall)

        # Create floor tiles for all empty (walkable) spaces in the maze
        for row in range(MAZE_SIZE_SETTING):
            for column in range(MAZE_SIZE_SETTING):
                if maze[row][column] == TILE_EMPTY:
                    floor = arcade.Sprite(
                        "images/tiles/blankTile.png",
                        scale=SPRITE_SCALING,
                    )
                    floor.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                    floor.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    
                    # SET MAZE FLOOR COLOR
                    floor.color = arcade.color.DEEP_SKY_BLUE
                    
                    self.floor_list.append(floor)

        # Set up the player with left-facing texture
        self.player_sprite = arcade.Sprite(
            scale=SPRITE_SCALING)
        
        # Set up both textures - left at index 0, right at index 1
        self.player_sprite.textures = [self.mouse_texture_left, self.mouse_texture_right]
        self.player_sprite.texture = self.mouse_texture_right
        self.player_list.append(self.player_sprite)

        # Place the player one tile to the right of the left wall (inside the maze)
        self.player_sprite.center_x = SPRITE_SIZE + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE + SPRITE_SIZE / 2

        # Create black tile at exit position (will be drawn under the exit sign)
        black_tile = arcade.Sprite(
            "images/tiles/blankTile.png",
            scale=SPRITE_SCALING,
        )
        black_tile.center_x = (MAZE_SIZE_SETTING - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        black_tile.center_y = (MAZE_SIZE_SETTING - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        black_tile.color = arcade.color.BLACK
        self.path_list.append(black_tile)

        # Create exit sprite (will be drawn on top of black tile)
        exit_sprite = arcade.Sprite(
            "images/tiles/signExit.png",
            scale=SPRITE_SCALING,
        )
        exit_sprite.center_x = (MAZE_SIZE_SETTING - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        exit_sprite.center_y = (MAZE_SIZE_SETTING - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        self.exit_list.append(exit_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        self.background_color = arcade.color.TEAL

        # Randomly place coins in the maze
        # Only place on verified empty tiles, and avoid player/exit positions
        player_pos = (1, 1)
        exit_pos = (MAZE_SIZE_SETTING - 2, MAZE_SIZE_SETTING - 2)
        
        for row in range(1, MAZE_SIZE_SETTING - 1):
            for column in range(1, MAZE_SIZE_SETTING - 1):
                # Check if tile is empty, not player/exit position, and random chance
                if (maze[row][column] == TILE_EMPTY and 
                    (row, column) != player_pos and 
                    (row, column) != exit_pos and 
                    random.random() < 0.08):  # 8% chance to place a coin
                    coin = arcade.Sprite(
                        "images/items/cheese.png",
                        scale=SPRITE_SCALING,
                    )
                    coin.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                    coin.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    self.coin_list.append(coin)


    # Render the screen
    def on_draw(self):

        # This command has to happen before we start drawing
        self.clear()

        # Select the sprite camera for the game world
        self.camera_sprites.use()

        # Draw all the sprites
        self.floor_list.draw()
        self.wall_list.draw()
        self.path_list.draw()
        self.coin_list.draw()
        self.exit_list.draw()
        self.player_list.draw()

        # Select the GUI camera for the HUD
        self.camera_gui.use()

        # Draw the HUD (score, time, completed mazes, grand total)
        output = f"Total Cheese: {self.grand_total_score}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 20, arcade.color.YELLOW, 16)

        output = f"Cheese: {self.score}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 40, arcade.color.WHITE, 16)

        output = f"Time: {self.elapsed_time:.1f}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 60, arcade.color.WHITE, 16)

        output = f"Completed: {self.completed_mazes}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 80, arcade.color.WHITE, 16)

        # Draw pathfinder uses remaining
        output = f"Pathfinder: {self.pathfinder_uses_remaining}/{self.pathfinder_max_uses}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 100, arcade.color.LIGHT_BLUE, 16, bold=True)


    # Calculate speed based on the keys pressed
    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Normalize diagonal movement so speed is consistent in all directions
        if self.player_sprite.change_x != 0 and self.player_sprite.change_y != 0:
            # Moving diagonally, so normalize to maintain constant speed
            self.player_sprite.change_x *= 0.7071  # 1/sqrt(2)
            self.player_sprite.change_y *= 0.7071
        
        # Update sprite direction based on horizontal movement
        if self.player_sprite.change_x < 0:
            self.player_sprite.texture = self.player_sprite.textures[0]  # Face left
        elif self.player_sprite.change_x > 0:
            self.player_sprite.texture = self.player_sprite.textures[1]  # Face right


    # Called whenever a key is pressed
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ENTER, arcade.key.ESCAPE):
            in_game_menu_view = InGameMenuView(self)
            self.window.show_view(in_game_menu_view)
        elif key == arcade.key.R:
            # Restart current maze (preserves maze layout)
            self.restart_maze()

        # Pathfinder
        elif key == arcade.key.SPACE:
            # Check if player has uses remaining
            if self.pathfinder_uses_remaining > 0:
                # Clear any existing path first (keep black tile at exit)
                black_tile = self.path_list[0] if len(self.path_list) > 0 else None
                self.path_list = arcade.SpriteList()
                if black_tile:
                    self.path_list.append(black_tile)
                
                # Show pathfinder path
                self.pathfinder(self.maze)
                
                # Consume a use and start timer
                self.pathfinder_uses_remaining -= 1
                self.pathfinder_active = True
                self.pathfinder_timer = 0.0
                self.pathfinder_sound.play(volume=0.3 * VOLUME_SETTING, pan=0.0)


        elif key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
            self.update_player_speed()
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
            self.update_player_speed()
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
            self.update_player_speed()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
            self.update_player_speed()


    # Called when the user releases a key (important for movement)
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
            self.update_player_speed()
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
            self.update_player_speed()
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
            self.update_player_speed()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
            self.update_player_speed()


    # Movement and game logic
    def on_update(self, delta_time):

        # Call update on all sprites
        self.physics_engine.update()

        # Check for collisions between the player and coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            if coin.visible:  # Only collect visible coins
                coin.visible = False
                self.score += 1
                self.grand_total_score += 1
                self.coin_sound.play(volume=0.3 * VOLUME_SETTING)

        # Check if player reached the exit (player must be fully on the exit tile)
        exit_sprite = self.exit_list[0]
        
        # Check if player center is within the exit tile boundaries
        exit_tile_left = exit_sprite.center_x - SPRITE_SIZE / 2
        exit_tile_right = exit_sprite.center_x + SPRITE_SIZE / 2
        exit_tile_bottom = exit_sprite.center_y - SPRITE_SIZE / 2
        exit_tile_top = exit_sprite.center_y + SPRITE_SIZE / 2
        
        # Player must be fully contained within the exit tile
        if (self.player_sprite.center_x > exit_tile_left and 
            self.player_sprite.center_x < exit_tile_right and
            self.player_sprite.center_y > exit_tile_bottom and 
            self.player_sprite.center_y < exit_tile_top):
            self.exit_sound.play(volume=0.3 * VOLUME_SETTING)
            # Show congratulations view
            congratulations_view = CongratulationsView(self)
            self.window.show_view(congratulations_view)

        # Update the elapsed time
        self.elapsed_time += delta_time

        # Update pathfinder timer - auto-hide after duration
        if self.pathfinder_active:
            self.pathfinder_timer += delta_time
            if self.pathfinder_timer >= self.pathfinder_duration:
                # Time's up - clear the path
                black_tile = self.path_list[0] if len(self.path_list) > 0 else None
                self.path_list = arcade.SpriteList()
                if black_tile:
                    self.path_list.append(black_tile)
                self.pathfinder_active = False
                self.pathfinder_timer = 0.0

        # Scroll the screen to the player
        self.scroll_to_player()


    #  Scroll the window to the player.
        # if CAMERA_SPEED is 1, the camera will immediately move to the desired
        # position. Anything between 0 and 1 will have the camera move to the
        # location with a smoother pan.
    def scroll_to_player(self):
        position = (self.player_sprite.center_x, self.player_sprite.center_y)
        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position, position, CAMERA_SPEED
        )
    

    # Pathfinder function to draw a path with tiles from the players position to the exit
    # utilizes A* 
    def pathfinder(self, maze):
        # Convert player position from pixels to grid coordinates
        player_grid_x = int(self.player_sprite.center_x / SPRITE_SIZE)
        player_grid_y = int(self.player_sprite.center_y / SPRITE_SIZE)
        
        # A* expects (row, column) which is (y, x)
        start = (player_grid_y, player_grid_x)
        goal = (MAZE_SIZE_SETTING - 2, MAZE_SIZE_SETTING - 2)
        
        path = astar(maze, start, goal)
        
        if path:
            # Limit to first N tiles of the path (path is reversed: goal to start)
            # Use last N elements to get tiles closest to player
            limited_path = path[-self.pathfinder_max_tiles:] if len(path) > self.pathfinder_max_tiles else path
            
            for (row, column) in limited_path:
                path_sprite = arcade.Sprite(
                    "images/tiles/blankTile.png",
                    scale=SPRITE_SCALING,
                )
                # Convert grid coordinates back to pixel coordinates
                path_sprite.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                path_sprite.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                
                # SET PATH COLOR
                path_sprite.color = arcade.color.RED
                
                self.path_list.append(path_sprite)