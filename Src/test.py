import pygame
import time

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dudl shoodle')

clock = pygame.time.Clock()
hero_left = pygame.image.load('../resources/Doodle_left.png')
hero_right = pygame.image.load('../resources/Doodle_left.png')
hero_width = 40
hero_height = 40


def car(x, y):
    gameDisplay.blit(hero_left, (x, y))


def text_objects(text, largeText):
    textSurface = largeText.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1)

    main_loop()

def crash():
    message_display("You crashed!")


def main_loop():
    gameExit = False
    x = (display_width * 0.45)
    y = (display_height * 0.5)
    x_change = 0
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    x_change = 0

        x += x_change

        gameDisplay.fill((255, 255, 255))
        car(x, y)
        if x > display_width - hero_width or x < 0:
            crash()

        pygame.display.flip()
        clock.tick(120)


main_loop()
pygame.quit()
quit()
