# MAIN FUNCTION

import arcade
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from classes import MainMenuView

def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)

    # Start the arcade game loop
    arcade.run()

# Run the main function
if __name__ == "__main__":
    main()