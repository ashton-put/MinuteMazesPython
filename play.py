# MAIN FUNCTION

import arcade
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from view_manager import ViewManager

def main():
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    view_manager = ViewManager(window)
    view_manager.show_main_menu()

    # Start the arcade game loop
    arcade.run()

# Run the main function
if __name__ == "__main__":
    main()