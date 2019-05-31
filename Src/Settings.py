# game options/settings
TITLE = "Noodle Doodle"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HIGHSCORE = "highscore.txt"

# Player properties
PLAYER_GRAVITY = 0.3
PLAYER_ACC = 0.40
PLAYER_FRICTION = -0.09
PlAYER_JUMP = 22.5

# Starting platforms
PLATFORM_LIST = [(WIDTH/2 - 40, HEIGHT - 40), (0, HEIGHT / 2),
                 (WIDTH/3, HEIGHT / 3), (WIDTH/2 + 40, HEIGHT / 4 - 15),
                 (WIDTH/4, HEIGHT / 5), (WIDTH/1.5, HEIGHT / 1.5), (WIDTH/1.25, HEIGHT / 1.25)]

PLATFORM_AMOUNT = 15

# Spring
BOOST = 30
SPRING_POSSIBILITY = 10

# Monsters
MONSTER_POSSIBILITY = 9000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (201, 103, 50)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# Images
BACKGROUND = "../resources/background.png"
BACKGROUND_SKIES = "../resources/background_skies.png"
START = "../resources/intro0.png"
DOODLE_LEFT = "../resources/Doodle_left.png"
DOODLE_UP = "../resources/Doodle_upward.png"
DOODLE_RIGHT = "../resources/Doodle_right.png"
PLATFORM_GREEN = "../resources/p-green.png"
PLATFORM_BLUE = "../resources/p-blue.png"
PLATFORM_BLUE = "../resources/p-blue.png"
PLATFORM_BROWN_1 = "../resources/p-brown-1.png"
PLATFORM_BROWN_2 = "../resources/p-brown-2.png"
PLATFORM_BROWN_3 = "../resources/p-brown-3.png"
PLATFORM_BROWN_4 = "../resources/p-brown-4.png"
PLATFORM_BROWN_5 = "../resources/p-brown-5.png"
PLATFORM_BROWN_6 = "../resources/p-brown-6.png"
GAMEOVER = "../resources/gameover.png"
SPRING_ON = "../resources/spring.png"
SPRING_OFF = "../resources/spring_comp.png"
MONSTER_UP = "../resources/bat1.png"
MONSTER_DOWN = "../resources/bat3.png"
BULLET = "../resources/bullet.png"


