# FUNCTIONS

import random
import heapq
from constants import TILE_EMPTY, TILE_CRATE

# Create a grid with empty cells on odd row/column combinations
def _create_grid_with_cells(width, height):
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(TILE_EMPTY)
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(TILE_CRATE)
            else:
                grid[row].append(TILE_CRATE)
    return grid

# Create a maze using depth-first search algorithm
# The maze is created by walking through the grid and creating walls between cells
# The walls are created by setting the cell to TILE_EMPTY
def make_maze(maze_width, maze_height):
    maze = _create_grid_with_cells(maze_width, maze_height)

    w = (len(maze[0]) - 1) // 2
    h = (len(maze) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x: int, y: int):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = TILE_EMPTY
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = TILE_EMPTY

            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))

    # Don't create entrance and exit openings - keep walls intact
    # maze[1][0] = TILE_EMPTY  # Entrance (removed)
    # maze[maze_height - 2][maze_width - 1] = TILE_EMPTY  # Exit (removed)

    return maze

# Heuristic function
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* algorithm
def astar(maze, start, goal):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    close_set = set()
    open_set = {start}  # Track open nodes in a set for O(1) lookup
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        open_set.discard(current)
        
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            
            if 0 <= neighbor[0] < len(maze):
                if 0 <= neighbor[1] < len(maze[0]):
                    if maze[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in open_set:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
                open_set.add(neighbor)

    return False
