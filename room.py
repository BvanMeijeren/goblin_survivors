from enemy import Enemy
import pyglet
import random 



class Room:
    def __init__(self, difficulty_level, max_enemies, batch, window_width, window_height):
        self.difficulty_level = difficulty_level
        self.max_enemies = max_enemies
        self.enemies = []
        self.batch = batch
        self.window_width = window_width
        self.window_height = window_height

    def spawn_enemy(self):
        x = random.choice([0, self.window_width])
        y = random.choice([0, self.window_height])
        enemy = Enemy(x, y, self.batch, image_path="graphics/goblin.png", scale=0.1)
        self.enemies.append(enemy)

    def draw_room(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        # Load the background image
        background_image = pyglet.image.load("graphics/terrain/forest/grass_background.png")

        # Create a sprite for the background
        background = pyglet.sprite.Sprite(background_image, x=0, y=0)

        # Scale the background to fit the window
        background.scale_x = WINDOW_WIDTH / background.width
        background.scale_y = WINDOW_HEIGHT / background.height

        background.draw()
