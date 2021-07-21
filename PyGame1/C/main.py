import pygame

pygame.init()

size = width, height = 400, 400

screen = pygame.display.set_mode(size)

running = True
drawing = False  # режим рисования выключен
x1, y1, w, h = 0, 0, 0, 0

history = [screen]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            x1, y1 = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            cur_screen = pygame.Surface(screen.get_size())
            cur_screen.blit(screen, (0, 0))
            history.append(cur_screen)
            drawing = False

        if event.type == pygame.MOUSEMOTION:
            w, h = event.pos[0] - x1, event.pos[1] - y1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if len(history) > 1:
                    history.pop()

    screen.fill(pygame.Color('black'))
    cur_screen = history[-1]
    screen.blit(cur_screen, (0, 0))

    if drawing:
        pygame.draw.rect(screen, (0, 0, 255), ((x1, y1), (w, h)), 5)
    pygame.display.flip()


pygame.quit()
