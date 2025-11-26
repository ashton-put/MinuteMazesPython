# CLASSES

from imports import *
from constants import *
from functions import *


class MainMenuView(arcade.View):
    """ Main Menu View """

    def __init__(self):
        super().__init__()
        self.camera_gui = arcade.Camera2D()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        # Use GUI camera for menu
        self.camera_gui.use()
        arcade.draw_text("Minute Mazes", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press ENTER to Start", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Quit", self.window.width / 2, self.window.height / 2 - 30,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """ Handle key presses. """
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class InGameMenuView(arcade.View):
    """ In-Game Menu View """

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.camera_gui = arcade.Camera2D()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        # Use GUI camera for pause menu
        self.camera_gui.use()
        arcade.draw_text("In-Game Menu", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press ENTER to Resume", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press SPACE for Main Menu", self.window.width / 2, self.window.height / 2 - 30,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Quit", self.window.width / 2, self.window.height / 2 - 60,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """ Handle key presses. """
        if key == arcade.key.ENTER:
            self.window.show_view(self.game_view)
        elif key == arcade.key.SPACE:
            main_menu_view = MainMenuView()
            self.window.show_view(main_menu_view)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class CongratulationsView(arcade.View):
    """ Congratulations View """

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.display_timer = 0
        self.camera_gui = arcade.Camera2D()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.GOLDEN_YELLOW)
        self.display_timer = 0

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        # Use GUI camera for congratulations screen
        self.camera_gui.use()
        arcade.draw_text("Congratulations!", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center", bold=True)
        arcade.draw_text("Maze Completed!", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text(f"Time: {self.game_view.elapsed_time:.1f} seconds", self.window.width / 2, self.window.height / 2 - 40,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_update(self, delta_time):
        """ Update the view """
        self.display_timer += delta_time
        if self.display_timer >= 3.0:  # After 3 seconds
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
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.path_list = None  
        self.coin_list = None  
        self.exit_list = None 

        # Player info
        self.player_sprite = None
        self.score = 0

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


    # Set up the game and initialize the variables
    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.path_list = arcade.SpriteList()  
        self.coin_list = arcade.SpriteList()  
        self.exit_list = arcade.SpriteList() 

        self.score = 0
        # Don't reset elapsed_time here - it's reset in CongratulationsView
        # Don't reset completed_mazes - we want to keep the count

        # Create the maze
        maze = make_maze(MAZE_WIDTH, MAZE_HEIGHT)

        # Create sprites based on 2D grid
        if not MERGE_SPRITES:
            # This is the simple-to-understand method. Each grid location
            # is a sprite
            for row in range(MAZE_HEIGHT):
                for column in range(MAZE_WIDTH):
                    if maze[row][column] == TILE_CRATE:
                        wall = arcade.Sprite(
                            ":resources:images/tiles/grassCenter.png",
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
            for row in range(MAZE_HEIGHT):
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
                        ":resources:images/tiles/stoneCenter.png",
                        scale=SPRITE_SCALING,
                    )
                    wall.center_x = column_mid * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.width = SPRITE_SIZE * column_count
                    self.wall_list.append(wall)

        # Set up the player
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_person/malePerson_idle.png",
            scale=SPRITE_SCALING)
        self.player_list.append(self.player_sprite)

        # Place the player one tile to the right of the left wall (inside the maze)
        self.player_sprite.center_x = SPRITE_SIZE + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE + SPRITE_SIZE / 2

        # Create exit sprite
        exit_sprite = arcade.Sprite(
            ":resources:images/tiles/signExit.png",
            scale=SPRITE_SCALING,
        )
        exit_sprite.center_x = (MAZE_WIDTH - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        exit_sprite.center_y = (MAZE_HEIGHT - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        self.exit_list.append(exit_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        self.background_color = arcade.color.AMAZON

        # Find path from entrance to exit
        start = (1, 1)
        goal = (MAZE_HEIGHT - 2, MAZE_WIDTH - 2)
        path = astar(maze, start, goal)

        # Draw the path
        if path:
            for (row, column) in path:
                path_sprite = arcade.Sprite(
                    ":resources:images/tiles/grassCenter.png",
                    scale=SPRITE_SCALING,
                )
                path_sprite.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                path_sprite.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                self.path_list.append(path_sprite)  # Add path sprites to path_list

        # Randomly place coins in the maze
        for row in range(1, MAZE_HEIGHT, 2):
            for column in range(1, MAZE_WIDTH, 2):
                if maze[row][column] == TILE_EMPTY and random.random() < 0.15:  # 15% chance to place a coin
                    coin = arcade.Sprite(
                        ":resources:images/items/coinGold.png",
                        scale=SPRITE_SCALING,
                    )
                    coin.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                    coin.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    self.coin_list.append(coin)


    # Render the screen
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the sprite camera for the game world
        self.camera_sprites.use()

        # Draw all the sprites
        self.wall_list.draw()
        self.path_list.draw()
        self.coin_list.draw()
        self.exit_list.draw()
        self.player_list.draw()

        # Select the GUI camera for the HUD
        self.camera_gui.use()

        # Draw the HUD (score, time, completed mazes)
        output = f"Coins: {self.score}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 20, arcade.color.WHITE, 16)

        output = f"Time: {self.elapsed_time:.1f}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 40, arcade.color.WHITE, 16)

        output = f"Completed: {self.completed_mazes}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 60, arcade.color.WHITE, 16)


    def update_player_speed(self):
        """ Calculate speed based on the keys pressed """
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

    # Called whenever a key is pressed
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ENTER:
            in_game_menu_view = InGameMenuView(self)
            self.window.show_view(in_game_menu_view)
        elif key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()


    # Called when the user releases a key
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()


    # Movement and game logic
    def on_update(self, delta_time):
        """ Movement and game logic """

        start_time = timeit.default_timer()

        # Call update on all sprites (The sprites don't do much in this
        # example though)
        self.physics_engine.update()

        # Check for collisions between the player and coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Check if player reached the exit
        exit_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.exit_list)
        if len(exit_hit_list) > 0:
            # Show congratulations view
            congratulations_view = CongratulationsView(self)
            self.window.show_view(congratulations_view)

        # Update the elapsed time
        self.elapsed_time += delta_time

        # Scroll the screen to the player
        self.scroll_to_player()


    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired
        position. Anything between 0 and 1 will have the camera move to the
        location with a smoother pan.
        """
        position = (self.player_sprite.center_x, self.player_sprite.center_y)
        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position, position, CAMERA_SPEED
        )