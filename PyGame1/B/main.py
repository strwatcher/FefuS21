import pygame

SIZE = WIDTH, HEIGHT = 300, 300
running = True
moving = False
pygame.init()

rect = pygame.Rect(0, 0, 30, 30)
x = 0
y = 0
surface = pygame.display.set_mode(SIZE)

pygame.draw.rect(surface, pygame.Color('red'), rect)
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if rect.x < x < rect.x + rect.width and rect.y < y < rect.y + rect.height:
                moving = True

        if event.type == pygame.MOUSEBUTTONUP and moving:
            moving = False
            rect.x, rect.y = event.pos[0] - rect.width//2, event.pos[1] - rect.width//2

        if event.type == pygame.MOUSEMOTION:
            if moving:
                rect.x, rect.y = event.pos[0] - rect.width//2, event.pos[1] - rect.width//2

    surface.fill(pygame.Color('black'))
    pygame.draw.rect(surface, pygame.Color('red'), rect)
    pygame.display.flip()

pygame.quit()
