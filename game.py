import pyglet
from player import Player
from enemy import Enemy
from bullet import Bullet
import random
import math
from image_scaler import scale_image
from upgrade_menu import UpgradePopup 
from upgrades import upgrades
from input_handler import InputHandler

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

# Game Mode Manager
input_handler = InputHandler()

# Load the background image
background_image = pyglet.image.load("graphics/terrain/forest/grass_background.png")

# Create a sprite for the background
background = pyglet.sprite.Sprite(background_image, x=0, y=0)

# Scale the background to fit the window
background.scale_x = WINDOW_WIDTH / background.width
background.scale_y = WINDOW_HEIGHT / background.height

# Initialize player
player = Player(400, 300, batch, image_path="graphics/wizard.png", scale=0.1, xp=0, xp_upgrade_threshold=10)  # Pass batch here
enemies = []
bullets = []

# Initialize upgrade menu 
upgrade_menu = UpgradePopup(batch, player, upgrades)

# Enemy spawn function
def spawn_enemy(dt):
    x = random.choice([0, 800])
    y = random.choice([0, 600])
    enemy = Enemy(x, y, batch, image_path="graphics/goblin.png",scale=0.1)
    enemies.append(enemy)  # Pass batch here

# Global update function
def update(dt):
    ## Gameplay ##
    if input_handler.game_mode == "gameplay":
        # Update player inputs
        input_handler.update_gameplay_inputs(dt, player)
        # Pass the pressed keys dictionary to the player
        player.update(dt, input_handler.pressed_keys, bullets, enemies, WEAPON_RANGE, BULLET_SPEED, FIRE_INTERVAL)

        # Update bullets
        for bullet in bullets[:]:
            if not bullet.update(dt, enemies):
                bullets.remove(bullet)

        # Update enemies
        for enemy in enemies[:]:
            enemy.move_towards_player(player, dt)
            if math.hypot(player.x - enemy.x, player.y - enemy.y) < 20:
                player.health -= 1
                enemies.remove(enemy)
                player.increment_xp(enemy.xp)
        
        # Player death
        if player.health <= 0:
            pyglet.app.exit()
            print(f"Game Over! Final XP: {player.xp}")

    ## Level-up ##
    if player.xp >= player.xp_upgrade_threshold and input_handler.game_mode != "upgrade_menu":
        player.xp = 0  # Reset XP for next level
        input_handler.set_mode("upgrade_menu")
        upgrade_menu.show()

# Draw function
@window.event
def on_draw():
    window.clear()
    background.draw()
    batch.draw()

    health_label = pyglet.text.Label(f'Health: {player.health}', x=10, y=570, color=(255, 255, 255, 255))
    xp_label = pyglet.text.Label(f'XP: {player.xp}', x=10, y=540, color=(255, 255, 255, 255))
    health_label.draw()
    xp_label.draw()

@window.event
def on_key_press(symbol, modifiers):
    input_handler.handle_key_press(symbol, modifiers, player=player, upgrade_menu=upgrade_menu)

@window.event
def on_key_release(symbol, modifiers):
    input_handler.handle_key_release(symbol, modifiers)

# Schedule functions
pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(spawn_enemy, ENEMY_SPAWN_RATE)

pyglet.app.run()
