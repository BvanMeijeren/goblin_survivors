import pyglet
import math

# Define Enemy Class
class Enemy(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, image_path, scale):
        image = pyglet.image.load(image_path)
        super().__init__(image, x, y, batch=batch)
        
        # xp given to palyer upon killing the enemy 
        self.xp = 1

        # scaling
        self.scale = scale

        self.speed = 100
        self.health = 20
        # Enemy initialization
        self.hitbox_offset = 15  # Extend the enemy's hitbox
        self.hitbox_padding = 10  # Padding around the hitbox

    def collides_with(self, other):
        return (
            self.x - self.hitbox_padding < other.x + other.width * other.scale + self.hitbox_padding and
            self.x + self.width * self.scale + self.hitbox_padding > other.x - self.hitbox_padding and
            self.y - self.hitbox_padding < other.y + other.height * other.scale + self.hitbox_padding and
            self.y + self.height * self.scale + self.hitbox_padding > other.y - self.hitbox_padding
        )

    def move_towards_player(self, player, dt):
        dx, dy = player.x - self.x, player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 5:  # Small threshold to stop jittering
            self.x += (dx / distance) * self.speed * dt
            self.y += (dy / distance) * self.speed * dt

    def hit(self, damage, enemies, player):
        self.health -= damage
        print(self.health)
        
        # enemy death
        if self.health <= 0:
            enemies.remove(self)
            self.delete()
            player.increment_xp(self.xp)
