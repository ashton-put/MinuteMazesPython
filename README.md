![Minute Mazes](images/random/example.png)

# Description: 
Minute mazes is a basic game where the player has to navigate through a maze to reach the exit. The maze is generated with a depth-first search algorithm and constructed with Python Arcade 3.3.3. The player can move up, down, left, and right. The player can collect cheese in the maze and their score is displayed on the screen along with elapsed time for each maze.

# Game Story (rough draft):
The year is 2052. You are just one of many bio-engineered lab mice that have been created to test newly developed brain enhancements before they are approved and made available to the public. While countless mice in the past have solved mazes with the promise of cheese at the end as a reward; you have been engineered, bred, and cybernetically enhanced to be focused on just one thing: solving mazes as quickly as possible and with as high a cheese score as possible.

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

- ```| Start Game |``` starts the game with the selected maze size.

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