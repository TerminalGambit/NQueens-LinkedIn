import pygame

class Cell:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.contains_queen = False


class Grid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[Cell(row, col, 0) for col in range(grid_size)] for row in range(grid_size)]
        self.queen_positions = []
        self.history = []

    def is_safe(self, row, col):
        """Check if placing a queen at (row, col) is valid."""
        for r, c in self.queen_positions:
            # Check row and column
            if r == row or c == col:
                return False
            # Check "king's movement" restriction (8 surrounding squares)
            if abs(row - r) <= 1 and abs(col - c) <= 1:
                return False
            # Check color conflict
            if self.grid[r][c].color == self.grid[row][col].color:
                return False
        return True

    def solve(self):
        """Solve the N-Queens problem using backtracking."""
        def backtrack(row, queen_positions, placed_regions):
            if row == self.grid_size:
                return queen_positions

            for col in range(self.grid_size):
                cell = self.grid[row][col]
                if self.is_safe(row, col) and cell.color not in placed_regions:
                    queen_positions.append((row, col))
                    placed_regions.add(cell.color)

                    if backtrack(row + 1, queen_positions, placed_regions):
                        return queen_positions

                    queen_positions.pop()
                    placed_regions.remove(cell.color)

            return None

        self.queen_positions = backtrack(0, [], set())
        if not self.queen_positions:
            print("No solution found!")
        else:
            for row, col in self.queen_positions:
                self.grid[row][col].contains_queen = True

    def reset(self):
        """Reset the grid by removing all queens."""
        self.queen_positions = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.grid[row][col].contains_queen = False

    def undo(self):
        """Undo the last action."""
        if self.history:
            row, col, prev_color = self.history.pop()
            self.grid[row][col].color = prev_color


def main():
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 900, 1000
    GRID_SIZE = 11
    CELL_SIZE = WIDTH // GRID_SIZE
    PALETTE_HEIGHT = 100

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    COLORS = [
        (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255),
        (75, 0, 130), (148, 0, 211), (255, 105, 180), (64, 224, 208), (139, 69, 19)
    ]
    while len(COLORS) < GRID_SIZE + 1:
        COLORS.append((len(COLORS) * 15 % 256, len(COLORS) * 50 % 256, len(COLORS) * 90 % 256))

    # Initialize screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("N-Queens Menu")

    # Fonts
    font = pygame.font.SysFont("Arial Unicode MS", 30)
    grid_font = pygame.font.SysFont("Arial Unicode MS", CELL_SIZE // 2)

    # Create the grid
    grid = Grid(GRID_SIZE)
    selected_color = 1

    # Define buttons
    buttons = [
        {"text": "Solve", "x": 50, "y": HEIGHT - PALETTE_HEIGHT - 60, "action": grid.solve},
        {"text": "Reset", "x": 250, "y": HEIGHT - PALETTE_HEIGHT - 60, "action": grid.reset},
        {"text": "Undo", "x": 450, "y": HEIGHT - PALETTE_HEIGHT - 60, "action": grid.undo},
        {"text": "Exit", "x": 650, "y": HEIGHT - PALETTE_HEIGHT - 60, "action": pygame.quit},
    ]

    def draw_grid():
        """Draw the grid and queens."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_color = COLORS[grid.grid[row][col].color]
                pygame.draw.rect(screen, cell_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

                # Draw queens
                if grid.grid[row][col].contains_queen:
                    queen_text = grid_font.render("♕", True, BLACK)
                    text_rect = queen_text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(queen_text, text_rect)

    def draw_palette():
        """Draw the color palette."""
        palette_width = WIDTH // len(COLORS)
        for i, color in enumerate(COLORS):
            x = i * palette_width
            pygame.draw.rect(screen, color, (x, HEIGHT - PALETTE_HEIGHT, palette_width, PALETTE_HEIGHT))
            pygame.draw.rect(screen, BLACK, (x, HEIGHT - PALETTE_HEIGHT, palette_width, PALETTE_HEIGHT), 2)

            # Highlight selected color
            if i == selected_color:
                pygame.draw.rect(screen, BLACK, (x + 2, HEIGHT - PALETTE_HEIGHT + 2, palette_width - 4, PALETTE_HEIGHT - 4), 3)

    def draw_buttons():
        """Draw menu buttons."""
        for button in buttons:
            text = font.render(button["text"], True, WHITE)
            pygame.draw.rect(screen, BLACK, (button["x"], button["y"], 150, 50))
            screen.blit(text, (button["x"] + 20, button["y"] + 10))

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_palette()
        draw_buttons()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y >= HEIGHT - PALETTE_HEIGHT:
                    palette_width = WIDTH // len(COLORS)
                    selected_color = x // palette_width
                elif HEIGHT - PALETTE_HEIGHT - 60 <= y < HEIGHT - PALETTE_HEIGHT:
                    for button in buttons:
                        if button["x"] <= x <= button["x"] + 150 and button["y"] <= y <= button["y"] + 50:
                            button["action"]()
                else:
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    grid.grid[row][col].color = selected_color

    pygame.quit()


if __name__ == "__main__":
    main()
