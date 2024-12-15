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
from room import Room

# Constants
ENEMY_SPAWN_RATE = 0.1
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

# Initialize player
player = Player(400, 300, batch, image_path="graphics/wizard.png", scale=0.1, xp=0, xp_upgrade_threshold=10)  # Pass batch here
enemies = []
bullets = []

# Initialize first room
current_room = Room(difficulty_level=1, max_enemies=5, batch=batch, window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT)

# Initialize upgrade menu 
upgrade_menu = UpgradePopup(batch, player, upgrades)

# Spawn enemies based on room 
def spawn_enemy(dt):
    """Spawn enemies in the current room."""
    current_room.spawn_enemy()

# Transition to a new room
def enter_new_room():
    """Simulate the player entering a new room."""
    global current_room
    print("Entering a new room...")
    
    # Create a new room with updated properties (e.g., increased difficulty)
    current_room = Room(
        difficulty_level=current_room.difficulty_level + 1,
        max_enemies=5 + current_room.difficulty_level,
        batch=batch,
        window_width=WINDOW_WIDTH,
        window_height=WINDOW_HEIGHT
    )

    # Reset player position to the starting point in the new room
    player.x = 50  # Start at the left edge
    player.y = WINDOW_HEIGHT // 2  # Center vertically
    pyglet.clock.schedule_interval(spawn_enemy, ENEMY_SPAWN_RATE)
    # Optionally, spawn enemies immediately in the new room
    #for _ in range(current_room.max_enemies):
    #    current_room.spawn_enemy()

def player_has_entered_new_room():
    """Check if the player can transition to the next room."""
    all_enemies_defeated = len(current_room.enemies) == 0
    in_exit_zone = player.x > WINDOW_WIDTH - 60
    return all_enemies_defeated and in_exit_zone

# Global update function
def update(dt):
    ## Gameplay ##
    if input_handler.game_mode == "gameplay":
        # Update player inputs
        input_handler.update_gameplay_inputs(dt, player)
        # Pass the pressed keys dictionary to the player
        player.update(dt, input_handler.pressed_keys, bullets, WEAPON_RANGE, BULLET_SPEED, FIRE_INTERVAL)

        # Check if enemies have reached max; stop spawning in this room
        if len(current_room.enemies) >= current_room.max_enemies:
            pyglet.clock.unschedule(spawn_enemy)
        
        # Player triggers room transition
        if player_has_entered_new_room():  # Define your condition
            enter_new_room()
            pyglet.clock.schedule_interval(spawn_enemy, 1.0)

        # shoot
        input_handler._handle_shoot_key_press(player=player, bullets=bullets, bullet_speed= BULLET_SPEED)

        # Update bullets
        for bullet in bullets[:]:
            if not bullet.update(dt, enemies):
                bullets.remove(bullet)

        # Update enemies
        for enemy in current_room.enemies[:]:  # Iterate over a copy of the list
            enemy.move_towards_player(player, dt)
            if math.hypot(player.x - enemy.x, player.y - enemy.y) < 20:
                player.health -= 1
                current_room.enemies.remove(enemy)
                player.increment_xp(enemy.xp)
        
        # Player death
        if player.health <= 0:
            pyglet.app.exit()
            print(f"Game Over! Final XP: {player.xp}")

    ## Level-up ##
    if player.xp >= player.xp_upgrade_threshold and input_handler.game_mode != "upgrade_menu":
        player.xp = 0  # Reset XP for next level
        input_handler.set_mode("upgrade_menu")
        upgrade_menu.pick_available_upgrades()
        upgrade_menu.show()

# Draw function
@window.event
def on_draw():
    window.clear()
    current_room.draw_room(WINDOW_WIDTH,WINDOW_HEIGHT)
    batch.draw()

    # Draw the UI menu stuff
    health_label = pyglet.text.Label(f'Health: {player.health}', x=10, y=570, color=(255, 255, 255, 255))
    xp_label = pyglet.text.Label(f'XP: {player.xp}', x=10, y=540, color=(255, 255, 255, 255))
    speed_label = pyglet.text.Label(f'Movement speed: {round(player.speed)}', x=10, y=510, color=(255, 255, 255, 255))
    shot_cooldown_label = pyglet.text.Label(f'Shot cooldown: {round(player.shot_cooldown,1)}', x=10, y=480, color=(255, 255, 255, 255))
    room_label = pyglet.text.Label(f'Room difficulty: {current_room.difficulty_level}', x=10, y=450, color=(255, 255, 255, 255))
    health_label.draw()
    xp_label.draw()
    speed_label.draw()
    shot_cooldown_label.draw()
    room_label.draw()

@window.event
def on_key_press(symbol, modifiers):
    input_handler.handle_key_press(
        symbol, 
        modifiers, 
        player=player, 
        upgrade_menu=upgrade_menu, 
        bullets=bullets, 
        bullet_speed=BULLET_SPEED
    )

@window.event
def on_key_release(symbol, modifiers):
    input_handler.handle_key_release(symbol, modifiers)

# Schedule functions
pyglet.clock.schedule_interval(update, 1/60)

# Run the app
pyglet.app.run()
