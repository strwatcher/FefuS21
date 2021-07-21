import pygame.event
from random import randrange


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[-2] * width for _ in range(height)]
        self.gen_bombs()

        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.window_size = (width * self.cell_size + self.left * 2, height * self.cell_size + self.top * 2)

    def gen_bombs(self):
        for k in range(randrange(1, self.width)):
            i = randrange(self.height - 1)
            j = randrange(self.width - 1)
            self.board[i][j] = -1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.window_size = (self.width * self.cell_size, self.height * self.cell_size)

    def count_bombs(self, j, i):
        if self.board[j][i] == -1:
            return

        self.board[j][i] = 0
        try:
            self.board[j][i] += int(self.board[j - 1][i] == -1)
        except IndexError:
            pass
        try:
            self.board[j][i] += int(self.board[j][i - 1] == -1)
        except IndexError:
            pass
        try:
            self.board[j][i] += int(self.board[j - 1][i - 1] == -1)
        except IndexError:
            pass
        try:
            self.board[j][i] += int(self.board[j - 1][i + 1] == -1)
        except IndexError:
            pass
        try:
            self.board[j][i] += int(self.board[j + 1][i - 1] == -1)
        except IndexError:
            pass
        try:
            self.board[j][i] += int(self.board[j + 1][i + 1] == -1)
        except IndexError:
            pass
        try:
            self.board[j][i] += int(self.board[j][i + 1] == -1)
        except IndexError:
            pass
        try:
            self.board[j][i] += int(self.board[j + 1][i] == -1)
        except IndexError:
            pass

    def is_point_in_cell(self, cell, point):
        i, j = cell
        x, y = point
        cell_x = i * self.cell_size
        cell_y = j * self.cell_size
        cell_x1 = cell_x + self.cell_size
        cell_y1 = cell_y + self.cell_size

        return cell_x < x < cell_x1 and cell_y < y < cell_y1

    def click_handler(self, point):
        for j, line in enumerate(self.board):
            for i in range(len(line)):
                if self.is_point_in_cell((i, j), point):
                    self.count_bombs(j, i)
                    return

    def render(self, surface: pygame.Surface):
        for j, line in enumerate(self.board):
            for i, cell in enumerate(line):
                if cell == -1:
                    pygame.draw.rect(surface, pygame.Color('red'), (i * self.cell_size + self.left,
                                                                    j * self.cell_size + self.top,
                                                                    self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(surface, pygame.Color('white'), (i * self.cell_size + self.left,
                                                                      j * self.cell_size + self.top,
                                                                      self.cell_size, self.cell_size), 1)

                    if cell >= 0:
                        font = pygame.font.Font(None, 32)
                        text = font.render(str(cell), True, pygame.Color('grey'))
                        text_x = i * self.cell_size + self.left + (self.cell_size // 2 - text.get_width() // 2)
                        text_y = j * self.cell_size + self.top + (self.cell_size // 2 - text.get_height() // 2)
                        surface.blit(text, (text_x, text_y))


pygame.init()
board = Board(10, 10)
screen = pygame.display.set_mode(board.window_size)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            board.click_handler(event.pos)

    screen.fill(pygame.Color('black'))
    board.render(screen)
    pygame.display.flip()

pygame.quit()
