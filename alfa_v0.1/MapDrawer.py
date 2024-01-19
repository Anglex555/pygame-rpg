import pygame
import sys

class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.draw_mode = 1
        self.board = [[0] * width for _ in range(height)]
        self.colors = [
            (0, 50, 180),    # DEEP_WATER_COLOR
            (0, 191, 255),  # SHELF_COLOR
            (0, 255, 255),  # SHALLOW_WATER_COLOR
            (245, 222, 179), # SAND_COLOR
            (139, 69, 19),
            (144, 238, 144), # SOIL_COLOR
            (0, 128, 0),     # FOREST_FLOOR_COLOR
            (128, 128, 128)
        ]
        self.key_colors = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
            pygame.K_6: 5,
            pygame.K_7: 6,
            pygame.K_8: 7,
        }
        self.current_color_index = 0

        pygame.init()

        self.window_size = ((width + 2) * cell_size, (height + 2) * cell_size)

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Map Creator")

        self.drawing_color = 0
        self.init_board()

    def change_color_around(self, row, col, size):
        for i in range(row - size, row + size):
            for j in range(col - size, col + size):
                if 0 <= i < self.height and 0 <= j < self.width:
                    self.toggle_cell(i, j)

    def init_board(self):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = 0

    def draw(self):
        for row in range(self.height):
            for col in range(self.width):
                x = (col + 1) * self.cell_size
                y = (row + 1) * self.cell_size 

                color = self.colors[self.board[row][col]]
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)

        pygame.display.flip()

    def toggle_cell(self, row, col):
        self.board[row][col] = self.drawing_color

    def handle_mouse_click_R(self, x, y):
        row = (y - self.cell_size) // self.cell_size
        col = (x - self.cell_size) // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            self.toggle_cell(row, col)
            self.change_color_around(row, col, (self.draw_mode - 1) * 2)
        #     print(f"({row}, {col})")
        # else:
        #     print("None")

    def handle_mouse_click(self, x, y):
        row = (y - self.cell_size) // self.cell_size
        col = (x - self.cell_size) // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            self.toggle_cell(row, col)
        #     print(f"({row}, {col})")
        # else:
        #     print("None")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for row in self.board:
                file.write(' '.join(map(str, row)) + '\n')

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for row, line in enumerate(lines):
                values = list(map(int, line.strip().split()))
                self.board[row][:len(values)] = values

    def run_game(self):
        zoom_factor = 1.0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.draw_mode += 1
                    if self.draw_mode == 8:
                        self.draw_mode = 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    self.handle_mouse_click(x, y)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.drawing_color = (self.drawing_color + 1) % len(self.colors)
                    print(self.drawing_color)
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = event.pos
                        if self.draw_mode == 1:
                            self.handle_mouse_click(x, y)
                        elif self.draw_mode != 1:
                            self.handle_mouse_click_R(x, y)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.save_to_file('map.txt')
                    print("Сохранено в map.txt")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    self.load_from_file('map.txt')
                    print("Загружено из map.txt")
                elif event.type == pygame.KEYDOWN and event.key in self.key_colors:
                    self.drawing_color = self.key_colors[event.key]
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    # Обработка увеличения масштаба колесиком мыши (кнопка 4)
                    zoom_factor += 0.1
                    zoom_factor = min(zoom_factor, 2.0)
                    self.cell_size = int(self.cell_size * zoom_factor)
                    self.window_size = ((self.width + 2) * self.cell_size, (self.height + 2) * self.cell_size)
                    self.screen = pygame.display.set_mode(self.window_size)
                    pygame.display.set_caption("Создатель карты")
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    # Обработка уменьшения масштаба колесиком мыши (кнопка 5)
                    zoom_factor -= 0.1
                    zoom_factor = max(zoom_factor, 0.1)
                    self.cell_size = int(self.cell_size * zoom_factor)
                    self.window_size = ((self.width + 2) * self.cell_size, (self.height + 2) * self.cell_size)
                    self.screen = pygame.display.set_mode(self.window_size)
                    pygame.display.set_caption("Создатель карты")

            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    width, height = 350, 200
    cell_size = 5
    chess_board = Board(width, height, cell_size)
    chess_board.run_game()