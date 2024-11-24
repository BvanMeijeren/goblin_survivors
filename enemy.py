import pyglet
import math

# Define Enemy Class
class Enemy(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, image_path=None):
        if image_path:
            image = pyglet.image.load(image_path)
        else:
            # Default image (green rectangle)
            image = pyglet.image.SolidColorImagePattern((0, 255, 0, 255)).create_image(30, 30)
        super().__init__(image, x, y, batch=batch)

        self.speed = 100
        self.health = 20

    def move_towards_player(self, player, dt):
        dx, dy = player.x - self.x, player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 5:  # Small threshold to stop jittering
            self.x += (dx / distance) * self.speed * dt
            self.y += (dy / distance) * self.speed * dt

    def hit(self, damage, enemies):
        self.health -= damage
        if self.health <= 0:
            enemies.remove(self)
            self.delete()

