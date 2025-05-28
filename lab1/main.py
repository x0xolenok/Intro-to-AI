import os

os.environ['SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS'] = '0'

import numpy as np
import pygame


DIE_COLOR = (255, 0, 0)
LIVE_COLOR = (0, 255, 0)
BG_COLOR = (47, 79, 79)
GRID_COLOR = (70, 130, 180)


def update_grid(surface: pygame, matrix: np.array, scale: int) -> np.array:

    new_matrix = np.zeros(matrix.shape)


    neighbor_count = (
            np.roll(matrix, 1, axis=0) + np.roll(matrix, -1, axis=0) +
            np.roll(matrix, 1, axis=1) + np.roll(matrix, -1, axis=1) +
            np.roll(np.roll(matrix, 1, axis=0), 1, axis=1) +
            np.roll(np.roll(matrix, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(matrix, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(matrix, -1, axis=0), -1, axis=1)
    )

    for i, j in np.ndindex(matrix.shape):
        live_neighbors = neighbor_count[i, j]

        if matrix[i, j] == 1:

            if live_neighbors < 2 or live_neighbors > 3:
                cell_color = DIE_COLOR
            else:
                new_matrix[i, j] = 1
                cell_color = LIVE_COLOR
        else:

            if live_neighbors == 3:
                new_matrix[i, j] = 1
                cell_color = LIVE_COLOR
            else:
                cell_color = BG_COLOR


        pygame.draw.rect(surface, cell_color, (j * scale, i * scale, scale - 1, scale - 1))

    return new_matrix


def initialize_grid(width: int, height: int) -> np.array:

    grid = np.zeros((height, width))


    patterns = {
        "block": np.array([
            [1, 1],
            [1, 1]
        ]),
        "blinker": np.array([
            [1, 1, 1]
        ]),
        "toad": np.array([
            [0, 1, 1, 1],
            [1, 1, 1, 0]
        ]),
        "glider": np.array([
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]),
        "beacon": np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ]),
        "lwss": np.array([
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ])
    }


    positions = {
        "block": (20, 2),
        "blinker": (0, 1),
        "toad": (2, 20),
        "glider": (10, 2),
        "beacon": (10, 10),
        "lwss": (60, 50)
    }


    for name, pat in patterns.items():
        pos = positions[name]
        ph, pw = pat.shape
        grid[pos[0]:pos[0] + ph, pos[1]:pos[1] + pw] = pat


    random_cells = (np.random.rand(height, width) < 0.10).astype(int)

    grid = np.maximum(grid, random_cells)

    return grid


def main():
    pygame.init()
    pygame.display.set_caption("Game of Life")


    width, height, scale = 115, 70, 10
    screen = pygame.display.set_mode((width * scale, height * scale))

    cells = initialize_grid(width, height)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill(GRID_COLOR)


        cells = update_grid(screen, cells, scale)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()