# Ablak beállítások
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Játék konstansok
MAP_SIZE = 32
CELL_SIZE = 64
WALL_HEIGHT = 64

# Játékos beállítások
PLAYER_SIZE = 5
PLAYER_SPEED = 200  # pixel/másodperc
TURN_SPEED = 2.0    # radián/másodperc

# Raycasting beállítások
FOV = 60  # Field of view fokokban
NUM_RAYS = WINDOW_WIDTH  # Egy sugár minden pixelre
MAX_DEPTH = MAP_SIZE * CELL_SIZE

# Színek
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)      # Falak
BROWN = (139, 69, 19)    # Talaj
BLUE = (135, 206, 235)   # Plafon
RED = (255, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Gombok színei
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_CLICK_COLOR = (200, 200, 200)

# Font méret
FONT_SIZE = 36
SMALL_FONT_SIZE = 24
