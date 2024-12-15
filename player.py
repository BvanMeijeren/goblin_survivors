import pyglet
import math
from bullet import Bullet

class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch, image_path, scale, xp, xp_upgrade_threshold):
        # Initialize the parent class
        image = pyglet.image.load(image_path)
        super().__init__(image, x=x, y=y, batch=batch)

        # scaling
        self.scale = scale

        # Player-specific attributes
        self.speed = 200
        self.health = 100
        self.time_since_last_shot = 0
        self.shot_cooldown = 0.4
        self.hitbox_width = self.width + 20  # Extend hitbox width
        self.hitbox_height = self.height + 20  # Extend hitbox height
        self.hitbox_padding = 10  # Padding around the hitbox
        self.xp = xp
        self.xp_upgrade_threshold = xp_upgrade_threshold 

    def collides_with(self, other):
        return (
            self.x - self.hitbox_padding < other.x + other.width * other.scale + self.hitbox_padding and
            self.x + self.width * self.scale + self.hitbox_padding > other.x - self.hitbox_padding and
            self.y - self.hitbox_padding < other.y + other.height * other.scale + self.hitbox_padding and
            self.y + self.height * self.scale + self.hitbox_padding > other.y - self.hitbox_padding
        )

    # Player WASD movement
    def move_up(self, dt):
        self.y += self.speed * dt

    def move_down(self, dt):
        self.y -= self.speed * dt

    def move_left(self, dt):
        self.x -= self.speed * dt

    def move_right(self, dt):
        self.x += self.speed * dt

    # other update player actions
    def update(self, dt, pressed_keys, bullets, weapon_range, bullet_speed, fire_interval):


        # Keep the player within window boundaries
        self.x = max(0, min(self.x, 800 - self.width))  # Adjust for window width
        self.y = max(0, min(self.y, 600 - self.height))  # Adjust for window height

        # Automatic firing logic
        self.time_since_last_shot += dt


    def is_enemy_in_range(self, enemy, range):
        distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
        return distance <= range


    def shoot(self, direction, bullets, bullet_speed):
        if self.time_since_last_shot < self.shot_cooldown:
            return  # Not enough time has passed since the last shot

        """Shoot a bullet in a specific direction."""
        # Determine velocity based on direction
        if direction == "up":
            bullet_dx, bullet_dy = 0, bullet_speed
        elif direction == "down":
            bullet_dx, bullet_dy = 0, -bullet_speed
        elif direction == "left":
            bullet_dx, bullet_dy = -bullet_speed, 0
        elif direction == "right":
            bullet_dx, bullet_dy = bullet_speed, 0
        else:
            return  # Invalid direction

        # Create and add the bullet
        bullet = Bullet(
            self.x + self.width // 2,  # Start bullet at player's center
            self.y + self.height // 2,
            bullet_dx,
            bullet_dy,
            self.batch,
            player=self
        )
        bullets.append(bullet)

       # Reset cooldown timer
        self.time_since_last_shot = 0

    #    def shoot(self, enemy, bullets, bullet_speed):
    #        dx, dy = enemy.x - self.x, enemy.y - self.y
    #        distance = math.sqrt(dx ** 2 + dy ** 2)
    #        bullet_dx, bullet_dy = (dx / distance) * bullet_speed, (dy / distance) * bullet_speed
    #        bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, bullet_dx, bullet_dy, self.batch, player=self)
    #        bullets.append(bullet)

    def increment_xp(self, enemy_xp):
        self.xp += enemy_xp
