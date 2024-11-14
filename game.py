import pyglet
import random
import math

# Set up the game window and batch
window = pyglet.window.Window(800, 600)
batch = pyglet.graphics.Batch()

# Constants for the game
PLAYER_SPEED = 200
ENEMY_SPEED = 100
ENEMY_SPAWN_RATE = 1.0  # seconds
FIRE_INTERVAL = 0.5  # Time in seconds between shots
WEAPON_RANGE = 200  # Range within which the player can shoot
BULLET_SPEED = 300
PLAYER_HEALTH = 100

# Game state
enemies = []
bullets = []
player_health = PLAYER_HEALTH
player_xp = 0  # New XP counter
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

# Define Player Class
class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(pyglet.image.SolidColorImagePattern((0, 255, 0, 255)).create_image(30, 30), x, y, batch=batch)
        self.speed = PLAYER_SPEED
        self.health = player_health
        self.time_since_last_shot = 0

    def update(self, dt):
        # WASD movement
        if keys[pyglet.window.key.W]:
            self.y += self.speed * dt
        if keys[pyglet.window.key.S]:
            self.y -= self.speed * dt
        if keys[pyglet.window.key.A]:
            self.x -= self.speed * dt
        if keys[pyglet.window.key.D]:
            self.x += self.speed * dt
        # Keep the player within window boundaries
        self.x = max(0, min(self.x, window.width - self.width))
        self.y = max(0, min(self.y, window.height - self.height))

        # Check for enemies in range and shoot if possible
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= FIRE_INTERVAL:
            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    self.shoot(enemy)
                    self.time_since_last_shot = 0
                    break

    def is_enemy_in_range(self, enemy):
        distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
        return distance <= WEAPON_RANGE

    def shoot(self, enemy):
        dx, dy = enemy.x - self.x, enemy.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        bullet_dx, bullet_dy = (dx / distance) * BULLET_SPEED, (dy / distance) * BULLET_SPEED
        bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, bullet_dx, bullet_dy)
        bullets.append(bullet)

# Define Enemy Class
class Enemy(pyglet.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(20, 20), x, y, batch=batch)
        self.speed = ENEMY_SPEED
        self.health = 20

    def move_towards_player(self, player, dt):
        dx, dy = player.x - self.x, player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 5:  # Small threshold to stop jittering
            self.x += (dx / distance) * self.speed * dt
            self.y += (dy / distance) * self.speed * dt

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            global player_xp
            player_xp += 1  # Increment XP counter when an enemy is defeated
            enemies.remove(self)
            self.delete()

# Define Bullet Class
class Bullet(pyglet.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__(pyglet.image.SolidColorImagePattern((255, 255, 0, 255)).create_image(10, 10), x, y, batch=batch)
        self.dx = dx
        self.dy = dy
        self.damage = 10

    def update(self, dt):
        # Move the bullet
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Check for collision with enemies
        for enemy in enemies:
            if math.hypot(enemy.x - self.x, enemy.y - self.y) < 15:
                enemy.hit(self.damage)
                bullets.remove(self)
                self.delete()
                return

        # Remove bullet if it goes off screen
        if not (0 <= self.x <= window.width and 0 <= self.y <= window.height):
            bullets.remove(self)
            self.delete()

# Initialize player
player = Player(window.width // 2, window.height // 2)

# Enemy spawn function
def spawn_enemy(dt):
    spawn_x = random.choice([0, window.width])
    spawn_y = random.choice([0, window.height])
    enemy = Enemy(spawn_x, spawn_y)
    enemies.append(enemy)

# Update function
def update(dt):
    global player_health
    player.update(dt)
    for bullet in bullets:
        bullet.update(dt)
    for enemy in enemies:
        enemy.move_towards_player(player, dt)
        # Check for collision with player (simple distance-based check)
        if math.hypot(enemy.x - player.x, enemy.y - player.y) < 20:
            player_health -= 1  # Reduce player health on collision
            enemies.remove(enemy)  # Remove enemy after it collides with player
            enemy.delete()
    # End game if health reaches zero
    if player_health <= 0:
        pyglet.app.exit()
        print("Game Over!")

# Draw function
@window.event
def on_draw():
    window.clear()
    batch.draw()
    # Draw player health and XP on screen
    health_label = pyglet.text.Label(f'Health: {player_health}',
                                     font_name='Arial',
                                     font_size=18,
                                     x=10, y=window.height - 30,
                                     color=(255, 255, 255, 255))
    health_label.draw()
    
    xp_label = pyglet.text.Label(f'XP: {player_xp}',  # Display XP
                                 font_name='Arial',
                                 font_size=18,
                                 x=10, y=window.height - 60,
                                 color=(255, 255, 255, 255))
    xp_label.draw()

# Schedule updates and enemy spawning
pyglet.clock.schedule_interval(update, 1/60.0)  # 60 FPS
pyglet.clock.schedule_interval(spawn_enemy, ENEMY_SPAWN_RATE)  # Spawn an enemy every second

# Run the game
pyglet.app.run()
