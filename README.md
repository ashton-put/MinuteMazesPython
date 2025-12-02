![Minute Mazes](images/misc/example.png)

# Description: 
Minute mazes is a game where the player must navigate through a series of mazes. Each maze is generated with a depth-first search algorithm and is constructed with Python Arcade. The player can move up, down, left, and right. The player can collect cheese in the maze and their score is displayed on the screen along with elapsed time for each maze. The player has an ability called "Pathfinder" that reveals a portion of the shortest path to the exit for a limited time. The game includes sound effects for collecting cheese, using abilities, and reaching the exit. The player can customize the maze size, mouse color, and sound volume in the settings menu.

### Setup
```
git clone https://github.com/ashton-put/MinuteMazesPython.git
python -m venv <your environment name>
source .<your environment name>/bin/activate
pip install -r requirements.txt
python play.py
```

### Controls
- When ```play.py``` is run - the Main Menu screen buttons direct the player to choose either:
```
| Start Game |
|  Settings  |
|    Quit    |
```

- In the 'Settings' menu, the player can adjust the maze size, mouse color, and effects volume:
```
Maze Size:
| Small (21x21) | Medium (31x31) | Large (51x51) |

Mouse Color:
| White | Gray | Brown |

Sound Volume: 75%

|---------*---|

| Back to Main Menu |
```

- ```| Start Game |``` starts the game with the selected maze size and mouse color.

- During gameplay:

```
WASD / Arrow Keys = Move through maze
        R         = Reset current maze (elapsed time and current score)
    ESC / ENTER   = Pause menu
    SPACE BAR     = Pathfinder ability (shows 10 tiles of the shortest path to the exit for 3 seconds, 3 uses per maze)
```

  - In the pause menu the player can choose to resume the game, access settings, return to the main menu, or quit the game.

  ### Image Citations and Tools
  - https://www.photopea.com/ 
  - https://www.youtube.com/watch?v=dMGIkO3xh1U 
  - https://www.remove.bg/ 

  - https://www.freepik.com/icon/mouse_5511456
  - https://pngimg.com/image/25292 
  - https://www.freepik.com/icon/mouse-toy_2830550

  ![Minute Mazes Mouse](images/sprites/white_mouse.png)