import pyglet
import math

# Define Bullet Class
class Bullet(pyglet.sprite.Sprite):
    def __init__(self, x, y, dx, dy, batch, player):
        super().__init__(pyglet.image.SolidColorImagePattern((255, 255, 0, 255)).create_image(10, 10), x, y, batch=batch)
        self.dx = dx
        self.dy = dy
        self.damage = 10
        self.player = player

    def update(self, dt, enemies):
        # Move the bullet
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Check for collision with enemies
        for enemy in enemies:
            if math.hypot(enemy.x - self.x, enemy.y - self.y) < 35:
                enemy.hit(self.damage, enemies, self.player)
                return

        # Remove bullet if it goes off screen
        if not (0 <= self.x <= 800 and 0 <= self.y <= 600):  # Adjust for window dimensions
            self.delete()
            return False
        return True
