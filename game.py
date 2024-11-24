import pyglet
from player import Player
from enemy import Enemy
from bullet import Bullet
import random
import math
from image_scaler import scale_image

# Constants
ENEMY_SPAWN_RATE = 1.0
FIRE_INTERVAL = 0.5
WEAPON_RANGE = 200
BULLET_SPEED = 300
CREATURE_HEIGHT = 30
CREATURE_WIDTH = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Initialize game
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
batch = pyglet.graphics.Batch()  # Centralized batch for rendering
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

# Load the background image
background_image = pyglet.image.load("graphics/terrain/forest/grass_background.png")

# Create a sprite for the background
background = pyglet.sprite.Sprite(background_image, x=0, y=0)

# Scale the background to fit the window
background.scale_x = WINDOW_WIDTH / background.width
background.scale_y = WINDOW_HEIGHT / background.height

# Initialize player
player = Player(400, 300, batch, image_path="graphics/wizard.png")  # Pass batch here
player.scale = 0.1
enemies = []
bullets = []
player_health = 100
player_xp = 0

# Enemy spawn function
def spawn_enemy(dt):
    x = random.choice([0, 800])
    y = random.choice([0, 600])
    enemy = Enemy(x, y, batch, image_path="graphics/goblin.png")
    enemy.scale = 0.1
    enemies.append(enemy)  # Pass batch here

# Update function
def update(dt):
    global player_health, player_xp
    player.update(dt, keys, bullets, enemies, WEAPON_RANGE, BULLET_SPEED, FIRE_INTERVAL)

    # Update bullets
    for bullet in bullets[:]:
        if not bullet.update(dt, enemies):
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies[:]:
        enemy.move_towards_player(player, dt)
        if math.hypot(player.x - enemy.x, player.y - enemy.y) < 20:  # Collision
            player_health -= 1
            enemies.remove(enemy)
            enemy.delete()

    # End game condition
    if player_health <= 0:
        pyglet.app.exit()
        print(f"Game Over! Final XP: {player_xp}")

# Draw function
@window.event
def on_draw():
    window.clear()

    # Draw the background first
    background.draw()

    batch.draw()  # Render all sprites in the batch

    # Draw health and XP
    health_label = pyglet.text.Label(f'Health: {player_health}', x=10, y=570, color=(255, 255, 255, 255))
    xp_label = pyglet.text.Label(f'XP: {player_xp}', x=10, y=540, color=(255, 255, 255, 255))
    health_label.draw()
    xp_label.draw()

# Schedule functions
pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(spawn_enemy, ENEMY_SPAWN_RATE)

pyglet.app.run()
