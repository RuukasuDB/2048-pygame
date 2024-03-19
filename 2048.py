import pygame
import random

# Konstanter
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 4
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    # 4096: (128, 0, 128)
}

# Tile class to represent each tile on the grid
class Tile:
    def __init__(self, x, y, value):
        self.x = x  # X-coordinate of the tile on the grid
        self.y = y  # Y-coordinate of the tile on the grid
        self.value = value  # Value of the tile

    # Method to draw the tile on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, TILE_COLORS[self.value], (self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10))
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.value), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2))
        screen.blit(text, text_rect)

# Game class to manage the game logic
class Game:
    # Initialize the game
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # Initialize the grid with zeros
        self.new_tile()  # Add initial tiles to the grid
        self.new_tile()

    # Method to add a new tile to the grid
    def new_tile(self):
        empty_cells = [(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if self.grid[y][x] == 0]  # Find empty cells on the grid
        if empty_cells:
            x, y = random.choice(empty_cells)  # Randomly choose an empty cell
            self.grid[y][x] = 2 if random.random() < 0.9 else 4  # Set the value of the new tile to 2 or 4 with certain probabilities

    # Method to draw the current state of the game on the screen
    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)  # Fill the screen with background color
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                value = self.grid[y][x]  # Get the value of the tile at position (x, y)
                if value:
                    tile = Tile(x, y, value)  # Create a Tile object
                    tile.draw(screen)  # Draw the tile on the screen
        pygame.display.flip()  # Update the display

    # Method to move tiles upwards
    def move_up(self):
        moved = False  # Flag to track if any tiles were moved
        for col in range(GRID_SIZE):
            for row in range(1, GRID_SIZE):
                if self.grid[row][col] != 0:
                    temp_row = row
                    while temp_row > 0 and self.grid[temp_row - 1][col] == 0:
                        self.grid[temp_row - 1][col] = self.grid[temp_row][col]
                        self.grid[temp_row][col] = 0
                        temp_row -= 1
                        moved = True
                    if temp_row > 0 and self.grid[temp_row - 1][col] == self.grid[temp_row][col]:
                        self.grid[temp_row - 1][col] *= 2
                        self.grid[temp_row][col] = 0
                        moved = True
        if moved:
            self.new_tile()
        elif not self.any_moves_possible():
            self.game_over()

    # Method to move tiles downwards
    def move_down(self):
        moved = False
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE - 2, -1, -1):
                if self.grid[row][col] != 0:
                    temp_row = row
                    while temp_row < GRID_SIZE - 1 and self.grid[temp_row + 1][col] == 0:
                        self.grid[temp_row + 1][col] = self.grid[temp_row][col]
                        self.grid[temp_row][col] = 0
                        temp_row += 1
                        moved = True
                    if temp_row < GRID_SIZE - 1 and self.grid[temp_row + 1][col] == self.grid[temp_row][col]:
                        self.grid[temp_row + 1][col] *= 2
                        self.grid[temp_row][col] = 0
                        moved = True
        if moved:
            self.new_tile()
        elif not self.any_moves_possible():
            self.game_over()

    # Method to move tiles to the left
    def move_left(self):
        moved = False
        for row in range(GRID_SIZE):
            for col in range(1, GRID_SIZE):
                if self.grid[row][col] != 0:
                    temp_col = col
                    while temp_col > 0 and self.grid[row][temp_col - 1] == 0:
                        self.grid[row][temp_col - 1] = self.grid[row][temp_col]
                        self.grid[row][temp_col] = 0
                        temp_col -= 1
                        moved = True
                    if temp_col > 0 and self.grid[row][temp_col - 1] == self.grid[row][temp_col]:
                        self.grid[row][temp_col - 1] *= 2
                        self.grid[row][temp_col] = 0
                        moved = True
        if moved:
            self.new_tile()
        elif not self.any_moves_possible():
            self.game_over()

    # Method to move tiles to the right
    def move_right(self):
        moved = False
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 2, -1, -1):
                if self.grid[row][col] != 0:
                    temp_col = col
                    while temp_col < GRID_SIZE - 1 and self.grid[row][temp_col + 1] == 0:
                        self.grid[row][temp_col + 1] = self.grid[row][temp_col]
                        self.grid[row][temp_col] = 0
                        temp_col += 1
                        moved = True
                    if temp_col < GRID_SIZE - 1 and self.grid[row][temp_col + 1] == self.grid[row][temp_col]:
                        self.grid[row][temp_col + 1] *= 2
                        self.grid[row][temp_col] = 0
                        moved = True
        if moved:
            self.new_tile()
        elif not self.any_moves_possible():
            self.game_over()

    # Method to handle game over
    def game_over(self):
        print("Game Over")
        self.reset_game()

    # Method to reset the game
    def reset_game(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # Reset the grid
        self.new_tile()  # Add initial tiles to the grid
        self.new_tile()

    # Method to check if any moves are possible
    def any_moves_possible(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 0:  # Check for empty cells
                    return True
                if col < GRID_SIZE - 1 and self.grid[row][col] == self.grid[row][col + 1]:  # Check for adjacent tiles with the same value horizontally
                    return True
                if row < GRID_SIZE - 1 and self.grid[row][col] == self.grid[row + 1][col]:  # Check for adjacent tiles with the same value vertically
                    return True
        return False

# Initialize Pygame
pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2048')

# Initialize the game
game = Game()

# Main game loop
running = True
while running:
    game.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()
            elif event.key == pygame.K_RIGHT:
                game.move_right()
            elif event.key == pygame.K_UP:
                game.move_up()
            elif event.key == pygame.K_DOWN:
                game.move_down()

pygame.quit()
