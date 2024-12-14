# Upgrades available to the player when leveling up

class Upgrade():
    def __init__(self, name, logic):
        #self.batch = batch
        self.name = name
        self.logic = logic

    def apply(self, player):
        """Apply the upgrade logic to the player """
        self.logic(player)


# Upgrade logic
def upgrade_health(player):
    player.health += 25
    print(f"Player health increased to {player.health}")

def upgrade_movement_speed(player):
    player.speed *= 1.1
    print(f"Player speed increased to {player.speed}")

# List of all upgrades
upgrades = [
    Upgrade(
        name = "Upgrade Health",
        logic = upgrade_health
    ),
    Upgrade(
        name = "Upgrade Movement Speed",
        logic = upgrade_movement_speed 
    )
]


