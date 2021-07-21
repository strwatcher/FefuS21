import pygame as pg
import sys

pg.init()

args = sys.argv
args = list(args)[1:]
window_size = 0
cell_size = 0

if len(args) < 2:
    window_size = int(input("Enter window size:"))
    cell_size = int(input("Enter cell size:"))
else:
    window_size = int(args[0])
    cell_size = int(args[1])

if window_size % cell_size != 0:
    sys.exit(1)

size = window_size, window_size
main_color = pg.color.Color('black')
second_color = pg.color.Color('white')
screen = pg.display.set_mode(size)

for j in range(0, window_size, cell_size):
    for i in range(0, window_size, cell_size):
        pg.draw.rect(screen, main_color, (i, j, i + cell_size, j + cell_size))
        main_color, second_color = second_color, main_color
    if (window_size // cell_size) % 2 == 0:
        main_color, second_color = second_color, main_color

pg.display.flip()

while pg.event.wait().type != pg.QUIT:
    pass

pg.quit()
