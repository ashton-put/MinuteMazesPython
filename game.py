# GAME - Main gameplay view and logic

import random
import arcade
import constants
from constants import (
    SPRITE_SCALING,
    SPRITE_SIZE,
    WINDOW_HEIGHT,
    TILE_EMPTY,
    TILE_CRATE,
    MERGE_SPRITES,
    MOVEMENT_SPEED,
    DIAGONAL_MOVEMENT_FACTOR,
    CAMERA_SPEED,
    CAMERA_ZOOM,
    MUSIC_VOLUME_MULTIPLIER,
    SOUND_VOLUME_MULTIPLIER,
    STORY_MODE_MAZE_SEQUENCE,
    STORY_MODE_TOTAL_MAZES,
    PATHFINDER_DURATION,
    PATHFINDER_MAX_TILES,
    PATHFINDER_MAX_USES
)
from functions import make_maze, astar
from view_manager import GameMode

# Main application class
class GameView(arcade.View):

    def __init__(self, view_manager, game_mode=GameMode.FREE_PLAY, story_mouse_color="white"):
        super().__init__()

        self.view_manager = view_manager

        # Load gameplay music
        self.gameplay_music = arcade.load_sound("sounds/music.mp3")
        self.music_player = None
        self.music_is_paused = False

         # Game mode
        self.game_mode = game_mode
        self.story_mouse_color = story_mouse_color  # Locked mouse color for story mode
        
        # Story mode specific tracking
        self.story_maze_index = 0  # Current maze in the sequence (0-9)
        self.total_story_time = 0  # Total time across all story mazes

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
        
        # Pathfinder state
        self.pathfinder_active = False
        self.pathfinder_timer = 0.0

    # Handle playing background music when the game starts
    def on_show_view(self):
        if self.music_player:
            if self.music_is_paused:
                # Resume from pause
                self.music_player.play()
                self.music_is_paused = False
        elif not self.music_player:
            # First time showing view or player was destroyed - start fresh
            self.music_player = self.gameplay_music.play(volume=MUSIC_VOLUME_MULTIPLIER * constants.VOLUME_SETTING)
            self.music_player.push_handlers(on_eos=self.loop_gameplay_music)

    # Handle pausing background music when pause menu or congrats screen shows
    def on_hide_view(self):
        if self.music_player and self.music_player.playing:
            self.music_player.pause()
            self.music_is_paused = True

    # Handle looping the background music
    def loop_gameplay_music(self):
        if self.music_player:
            self.music_player.pop_handlers()
        self.music_player = self.gameplay_music.play(volume=MUSIC_VOLUME_MULTIPLIER * constants.VOLUME_SETTING)
        self.music_player.push_handlers(on_eos=self.loop_gameplay_music)
    
    # Clear the pathfinder path visualization, preserving the black exit tile
    def clear_pathfinder(self):
        if self.path_list and len(self.path_list) > 0:
            black_tile = self.path_list[0]  # First tile is always the black exit marker
            self.path_list = arcade.SpriteList()
            self.path_list.append(black_tile)
        self.pathfinder_active = False
        self.pathfinder_timer = 0.0
    
    # Create the black tile marker at the exit position
    def create_exit_black_tile(self):
        if self.game_mode == GameMode.STORY_MODE:
            current_maze_size = STORY_MODE_MAZE_SEQUENCE[self.story_maze_index]
        else:
            current_maze_size = constants.MAZE_SIZE_SETTING
        
        black_tile = arcade.Sprite("images/tiles/blankTile.png", scale=SPRITE_SCALING)
        black_tile.center_x = (current_maze_size - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        black_tile.center_y = (current_maze_size - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        black_tile.color = arcade.color.BLACK
        self.path_list.append(black_tile)
    
    # Return the current maze size based on game mode
    def get_current_maze_size(self):
        if self.game_mode == GameMode.STORY_MODE:
            return STORY_MODE_MAZE_SEQUENCE[self.story_maze_index]
        else:
            return constants.MAZE_SIZE_SETTING
    
    # Return the current mouse color based on game mode
    def get_current_mouse_color(self):
        if self.game_mode == GameMode.STORY_MODE:
            return self.story_mouse_color
        else:
            return constants.MOUSE_COLOR_SETTING
    
    # Create wall sprites from maze grid
    def create_maze_walls(self, maze, maze_size):
        if not MERGE_SPRITES:
            # Simple method: Each grid location is a sprite
            for row in range(maze_size):
                for column in range(maze_size):
                    if maze[row][column] == TILE_CRATE:
                        wall = arcade.Sprite("images/tiles/blankTile.png", scale=SPRITE_SCALING)
                        wall.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                        wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                        self.wall_list.append(wall)
        else:
            # Optimized: Merge consecutive walls into larger sprites
            for row in range(maze_size):
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
                    
                    wall = arcade.Sprite("images/tiles/blankTile.png", scale=SPRITE_SCALING)
                    wall.center_x = column_mid * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.width = SPRITE_SIZE * column_count
                    wall.color = arcade.color.DODGER_BLUE
                    self.wall_list.append(wall)
    
    # Create floor sprites for walkable areas
    def create_maze_floor(self, maze, maze_size):
        for row in range(maze_size):
            for column in range(maze_size):
                if maze[row][column] == TILE_EMPTY:
                    floor = arcade.Sprite("images/tiles/blankTile.png", scale=SPRITE_SCALING)
                    floor.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                    floor.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    floor.color = arcade.color.DEEP_SKY_BLUE
                    self.floor_list.append(floor)
    
    # Initialize player sprite with textures
    def setup_player(self, mouse_color):
        mouse_filename = f"images/sprites/{mouse_color}_mouse.png"
        self.mouse_texture_right = arcade.load_texture(mouse_filename)
        self.mouse_texture_left = self.mouse_texture_right.flip_left_right()
        
        self.player_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.player_sprite.textures = [self.mouse_texture_left, self.mouse_texture_right]
        self.player_sprite.texture = self.mouse_texture_right
        self.player_list.append(self.player_sprite)
        
        # Place player at spawn point
        self.player_sprite.center_x = SPRITE_SIZE + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE + SPRITE_SIZE / 2
    
    # Place coins randomly in walkable maze areas
    def place_coins(self, maze, maze_size):
        player_pos = (1, 1)
        exit_pos = (maze_size - 2, maze_size - 2)
        
        for row in range(1, maze_size - 1):
            for column in range(1, maze_size - 1):
                # Check if tile is empty, not player/exit position, and random chance
                if (maze[row][column] == TILE_EMPTY and 
                    (row, column) != player_pos and 
                    (row, column) != exit_pos and 
                    random.random() < 0.08):  # 8% chance to place a coin
                    coin = arcade.Sprite("images/items/cheese.png", scale=SPRITE_SCALING)
                    coin.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                    coin.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    self.coin_list.append(coin)

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
        self.clear_pathfinder()
        
        # Reset camera to player
        self.camera_sprites.position = (self.player_sprite.center_x, self.player_sprite.center_y)

    # Set up the game and initialize the variables
    def setup(self):
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.path_list = arcade.SpriteList()  
        self.coin_list = arcade.SpriteList()  
        self.exit_list = arcade.SpriteList() 

        self.score = 0
        self.camera_sprites.zoom = CAMERA_ZOOM

        # Get current configuration
        current_maze_size = self.get_current_maze_size()
        mouse_color = self.get_current_mouse_color()

        # Load sound effects
        self.coin_sound = arcade.Sound("sounds/collect.wav")
        self.pathfinder_sound = arcade.Sound("sounds/pathfinder.wav")
        self.exit_sound = arcade.Sound("sounds/exit.wav")

        # Initialize pathfinder variables
        self.pathfinder_uses_remaining = PATHFINDER_MAX_USES
        self.pathfinder_max_uses = PATHFINDER_MAX_USES
        self.pathfinder_active = False
        self.pathfinder_timer = 0.0
        self.pathfinder_duration = PATHFINDER_DURATION
        self.pathfinder_max_tiles = PATHFINDER_MAX_TILES
        
        # Generate maze
        maze = make_maze(current_maze_size, current_maze_size)
        self.maze = maze
        
        # Create maze sprites
        self.create_maze_walls(maze, current_maze_size)
        self.create_maze_floor(maze, current_maze_size)
        
        # Setup player
        self.setup_player(mouse_color)
        
        # Create exit marker and sign
        self.create_exit_black_tile()
        exit_sprite = arcade.Sprite("images/tiles/exitSign.png", scale=SPRITE_SCALING)
        exit_sprite.center_x = (current_maze_size - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        exit_sprite.center_y = (current_maze_size - 2) * SPRITE_SIZE + SPRITE_SIZE / 2
        self.exit_list.append(exit_sprite)
        
        # Setup physics
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        
        # Set background color
        self.background_color = arcade.color.TEAL
        
        # Place coins
        self.place_coins(maze, current_maze_size)
        
        # Start music if not playing
        if not self.music_player:
            self.music_player = self.gameplay_music.play(volume=MUSIC_VOLUME_MULTIPLIER * constants.VOLUME_SETTING)
            self.music_player.push_handlers(on_eos=self.loop_gameplay_music)

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

        output = f"Time: {self.elapsed_time:.3f} s"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 60, arcade.color.WHITE, 16)

        output = f"Completed: {self.completed_mazes}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 80, arcade.color.WHITE, 16)
        
        # Show maze size for current maze
        current_size = self.get_current_maze_size()
        size_name = "Small" if current_size == 21 else "Medium" if current_size == 31 else "Large"
        output = f"Maze Size: {size_name}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 100, arcade.color.WHITE, 16)

        # Draw pathfinder uses remaining
        output = f"Pathfinder: {self.pathfinder_uses_remaining}/{self.pathfinder_max_uses}"
        arcade.draw_text(output, 20, WINDOW_HEIGHT - 120, arcade.color.LIGHT_BLUE, 16, bold=True)

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
            self.player_sprite.change_x *= DIAGONAL_MOVEMENT_FACTOR
            self.player_sprite.change_y *= DIAGONAL_MOVEMENT_FACTOR
        
        # Update sprite direction based on horizontal movement
        if self.player_sprite.change_x < 0:
            self.player_sprite.texture = self.player_sprite.textures[0]  # Face left
        elif self.player_sprite.change_x > 0:
            self.player_sprite.texture = self.player_sprite.textures[1]  # Face right

    # Called whenever a key is pressed
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ENTER, arcade.key.ESCAPE):
            self.view_manager.show_in_game_menu(self)
        elif key == arcade.key.R:
            # Restart current maze (preserves maze layout)
            self.restart_maze()

        # Pathfinder
        elif key == arcade.key.SPACE:
            # Check if player has uses remaining
            if self.pathfinder_uses_remaining > 0:
                # Clear any existing path first
                self.clear_pathfinder()
                # Restore black tile after clearing
                if len(self.path_list) == 0:
                    self.create_exit_black_tile()
                
                # Show pathfinder path
                self.pathfinder(self.maze)
                
                # Consume a use and start timer
                self.pathfinder_uses_remaining -= 1
                self.pathfinder_active = True
                self.pathfinder_timer = 0.0
                self.pathfinder_sound.play(volume=SOUND_VOLUME_MULTIPLIER * constants.VOLUME_SETTING, pan=0.0)


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
                self.coin_sound.play(volume=SOUND_VOLUME_MULTIPLIER * constants.VOLUME_SETTING)

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

            self.exit_sound.play(volume=SOUND_VOLUME_MULTIPLIER * constants.VOLUME_SETTING)

            if self.game_mode == GameMode.STORY_MODE:
                # Track total time across all mazes
                self.total_story_time += self.elapsed_time
                
                # Check if this was the last maze
                if self.story_maze_index >= STORY_MODE_TOTAL_MAZES - 1:
                    # Story complete! Show victory screen
                    self.view_manager.show_story_victory(self)
                else:
                    # Move to next maze in story
                    self.story_maze_index += 1
                    self.elapsed_time = 0
                    self.completed_mazes += 1
                    self.setup()  # Generate next maze
                    # Note: No congratulations screen in story mode, seamless transition
            else:
                # Free play mode - show congratulations
                self.view_manager.show_congratulations(self)

        # Update the elapsed time
        self.elapsed_time += delta_time

        # Update pathfinder timer - auto-hide after duration
        if self.pathfinder_active:
            self.pathfinder_timer += delta_time
            if self.pathfinder_timer >= self.pathfinder_duration:
                # Time's up - clear the path
                self.clear_pathfinder()
                # Restore black tile
                if len(self.path_list) == 0:
                    self.create_exit_black_tile()

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

        # Determine current maze size
        current_maze_size = self.get_current_maze_size()
        
        # A* expects (row, column) which is (y, x)
        start = (player_grid_y, player_grid_x)
        goal = (current_maze_size - 2, current_maze_size - 2)
        
        path = astar(maze, start, goal)
        
        if path:
            # Limit to first N tiles of the path (path is reversed: goal to start)
            # Use last N elements to get tiles closest to player
            limited_path = path[-self.pathfinder_max_tiles:] if len(path) > self.pathfinder_max_tiles else path
            
            for (row, column) in limited_path:
                path_sprite = arcade.Sprite("images/tiles/blankTile.png", scale=SPRITE_SCALING)
                # Convert grid coordinates back to pixel coordinates
                path_sprite.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                path_sprite.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                path_sprite.color = arcade.color.RED
                self.path_list.append(path_sprite)