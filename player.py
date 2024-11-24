import pyglet
import math
from bullet import Bullet

# Define Player Class
class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, image_path=None):
        if image_path:
            image = pyglet.image.load(image_path)
        else:
            # Default image (green rectangle)
            image = pyglet.image.SolidColorImagePattern((0, 255, 0, 255)).create_image(30, 30)
        super().__init__(image, x, y, batch=batch)

        self.speed = 200
        self.health = 100
        self.time_since_last_shot = 0

    def update(self, dt, keys, bullets, enemies, weapon_range, bullet_speed, fire_interval):
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
        self.x = max(0, min(self.x, 800 - self.width))  # Adjust for window width
        self.y = max(0, min(self.y, 600 - self.height))  # Adjust for window height

        # Automatic firing logic
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= fire_interval:
            for enemy in enemies:
                if self.is_enemy_in_range(enemy, weapon_range):
                    self.shoot(enemy, bullets, bullet_speed)
                    self.time_since_last_shot = 0
                    break

    def is_enemy_in_range(self, enemy, range):
        distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
        return distance <= range

    def shoot(self, enemy, bullets, bullet_speed):
        dx, dy = enemy.x - self.x, enemy.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        bullet_dx, bullet_dy = (dx / distance) * bullet_speed, (dy / distance) * bullet_speed
        bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, bullet_dx, bullet_dy, self.batch)
        bullets.append(bullet)
