# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16sIrzE9Z5SwJvUIUPzkD-ADiK2Qk8HZW
"""

import random
import numpy as np

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.move_count = 0

    def add_new_tile(self):
        self.move_count += 1
        empty_cells = list(zip(*np.where(self.grid == 0)))
        if empty_cells:
            if (0, 3) in empty_cells:
                x, y = 0, 3  # Try to add at (0, 3) if possible
            else:
                x, y = empty_cells[0]  # Add at the first empty cell
            self.grid[x][y] = 2  # Always add a '2' for consistency

    def compress(self, grid):
        new_grid = np.zeros((4, 4), dtype=int)
        for i in range(4):
            pos = 0
            for j in range(4):
                if grid[i][j] != 0:
                    new_grid[i][pos] = grid[i][j]
                    pos += 1
        return new_grid

    def merge(self, grid):
        for i in range(4):
            for j in range(3):
                if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    self.score += grid[i][j]
                    grid[i][j + 1] = 0
        return grid

    def reverse(self, grid):
        return np.flip(grid, axis=1)

    def transpose(self, grid):
        return np.transpose(grid)

    def move_left(self):
        original_grid = np.copy(self.grid)
        self.grid = self.compress(self.grid)
        self.grid = self.merge(self.grid)
        self.grid = self.compress(self.grid)
        return not np.array_equal(original_grid, self.grid)

    def move_right(self):
        original_grid = np.copy(self.grid)
        self.grid = self.reverse(self.grid)
        self.grid = self.compress(self.grid)
        self.grid = self.merge(self.grid)
        self.grid = self.compress(self.grid)
        self.grid = self.reverse(self.grid)
        return not np.array_equal(original_grid, self.grid)

    def move_up(self):
        original_grid = np.copy(self.grid)
        self.grid = self.transpose(self.grid)
        # Reverse to process from bottom to top
        self.grid = self.reverse(self.grid)
        self.grid = self.compress(self.grid)
        self.grid = self.merge(self.grid)
        self.grid = self.compress(self.grid)
        # Reverse back to original order
        self.grid = self.reverse(self.grid)
        self.grid = self.transpose(self.grid)
        return not np.array_equal(original_grid, self.grid)

    def move_down(self):
        original_grid = np.copy(self.grid)
        self.grid = self.transpose(self.grid)
        # Reverse to process from top to bottom
        self.grid = self.reverse(self.grid)
        self.grid = self.compress(self.grid)
        self.grid = self.merge(self.grid)
        self.grid = self.compress(self.grid)
        # Reverse back to original order
        self.grid = self.reverse(self.grid)
        self.grid = self.transpose(self.grid)
        return not np.array_equal(original_grid, self.grid)

    def is_game_over(self):
        if np.any(self.grid == 0):
            return False
        for move in ['move_left', 'move_up', 'move_down', 'move_right']:
            temp_game = Game2048()
            temp_game.grid = np.copy(self.grid)
            temp_game.score = self.score
            changed = getattr(temp_game, move)()
            if changed:
                return False
        return True

    def get_available_moves(self):
        moves = []
        for move in ['left', 'up', 'down', 'right']:
            temp_game = Game2048()
            temp_game.grid = np.copy(self.grid)
            temp_game.score = self.score
            moved = getattr(temp_game, f'move_{move}')()
            if moved:
                moves.append(move)
        return moves

class AI2048:
    def __init__(self, game):
        self.game = game

    def get_best_move(self):
        moves = self.game.get_available_moves()
        # Prioritize 'left' and 'up' moves
        if 'left' in moves:
            return 'left'
        elif 'up' in moves:
            return 'up'
        elif 'down' in moves:
            return 'down'
        elif 'right' in moves:
            return 'right'
        return None

def main():
    random.seed(42)
    np.random.seed(42)

    game = Game2048()
    game.grid = np.array([
        [16, 8, 0, 0],
        [8, 16, 8, 4],
        [128, 32, 8, 4],
        [128, 64, 32, 16]
    ])

    ai = AI2048(game)

    print("State after move but before adding new tile:")
    print(game.grid)

    game.add_new_tile()
    print("State after adding new tile:")
    print(game.grid)

    while True:
        move = ai.get_best_move()
        if move:
            print(f"AI chooses to move: {move}")
            moved = getattr(game, f'move_{move}')()
            if not moved:
                continue

            print("State after move but before adding new tile:")
            print(game.grid)

            # Check for the maximum tile before adding a new tile
            max_tile = np.max(game.grid)
            if max_tile >= 256:
                print(f"Congratulations! You have reached {max_tile}!")
                print(game.grid)
                print("Game Over!")
                break

            game.add_new_tile()
            print("State after adding new tile:")
            print(game.grid)
        else:
            print("Game Over!")
            break

if __name__ == "__main__":
    main()

